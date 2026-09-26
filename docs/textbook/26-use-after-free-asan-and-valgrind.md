# 26 — Use-after-free: the pointer still looks fine

**Week 4.** Syllabus items: *Dangling references, use-after-free, and how they present*; *Debug
with `gdb`, `valgrind`, and sanitizers*. Completes both, with gdb from week 3
([22](22-parsing-input-that-fights-back.md)) and ASan from [24](24-raii-and-ownership.md).

Prompted by `cpp_memory/`, exercise 4: a raw pointer borrowed from a `unique_ptr` that outlives
it. Run under ASan, then under valgrind, then with no tool at all. The three runs printed
different things.

Follows [25 — Move semantics](25-move-semantics.md), where the only dangling pointer seen so far
was a null one.

---

## The bug

```cpp
int* borrowed;
{
  std::unique_ptr<int> p(new int(7));   // line 32
  borrowed = p.get();
}                                       // line 37
std::cout << "*borrowed = " << *borrowed;  // line 39
```

## The mental model: freeing changes the memory, not the pointer

Two predictions on record, both natural and both wrong:

- *"Out of scope, borrowed doesn't have a value yet."* It does. `p.get()` returned an address,
  and that number was **copied** into `borrowed`. Nothing afterwards changes it.
- *"p's address gets deconstructed, the int is still there."* Half right. `p`, the `unique_ptr`
  object, is on the stack and is destroyed at the `}`. But destroying it means **running its
  destructor**, and `unique_ptr`'s destructor calls `delete` on the heap `int`. That's the RAII
  class from [24](24-raii-and-ownership.md), done for you.

So after line 37, `borrowed` holds exactly the same number it did before, and that number now
names memory the program no longer owns. **Nothing resets other people's copies of a pointer.**
That's the whole danger. A dangling pointer is indistinguishable from a good one by looking at it.

Contrast with [25](25-move-semantics.md): a *moved-from* `unique_ptr` is explicitly set to null,
so dereferencing it faults at `0x0`, which is loud and obvious. A borrowed raw pointer gets no such
treatment. It keeps a real, plausible heap address.

## A side trap: `*borrowed;` reads nothing

The first version ended with a bare `*borrowed;`. GCC warns *"value computed is not used"* and
emits no load. **No read means no bug for ASan to see**: exit 0, silent. If a test deliberately
triggers UB, make sure the result is *used* (print it, return it). Read the warnings; this one
said exactly what was wrong.

## How it presents: three tools, three outputs

**ASan** (compiled in, `-fsanitize=address`):

```text
ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000010
READ of size 4 ...          main.cpp:39   ← the bad read (4 = sizeof(int))
freed by thread T0 here:    main.cpp:37   ← the }, via ~unique_ptr → default_delete
previously allocated by:    main.cpp:32   ← new int(7)
```

Aborts on the spot. It names the bug by its **history** (heap, used after free), because it
tracked the allocation and the free.

**Valgrind** (unmodified binary, `valgrind ./mem`):

```text
Invalid read of size 4        at main (main.cpp:39)
 Address 0x4e1f080 is 0 bytes inside a block of size 4 free'd
   ... ~unique_ptr() ... main (main.cpp:37)
 Block was alloc'd at         main (main.cpp:32)
*borrowed = 7
```

Same three stacks, different vocabulary: it names **what the instruction did** ("invalid read")
and then explains *why* it was invalid. It reports and **keeps running**, so the `7` prints.

**No tool** (`./build/mem`): prints a garbage number, not 7. Checked in session: 7 under valgrind,
something else without it.

### Why the value differs

Prediction on record: *"7 will print, unless something literally changed those bytes after the
freeing."* That "unless" is exactly what happened, and the thing that changed them is the
**allocator itself**.

- **glibc's `free`** puts the block on a free list and stores its own bookkeeping (a pointer to
  the next free block) **inside the freed block**, in its first bytes. Freed memory is the
  allocator's scratch space. The `7` was overwritten the instant `delete` ran.
- **Valgrind replaces `new`/`delete`** with its own allocator. It doesn't write into freed blocks,
  and it holds them in a queue instead of reusing them immediately, so that a later access can
  still be recognised as "inside a block free'd". So the old `7` survives.

This is what undefined behavior means in practice: the result depends on the allocator's
internals, and **the tool changed the answer**. A use-after-free can print the right value under
one tool and garbage under another, or fine in debug and wrong in release. Never treat
"it printed the right number" as evidence that memory access is valid.

### Why `p.get()` appears in no stack

`p.get()` copies an address out of `p`. It doesn't touch the heap `int`. Both tools record
**memory events**: allocate, free, access. Copying a pointer isn't one of them, so the moment the
dangerous alias was created leaves no trace. In real code, that's why use-after-free is hard to
find: the report tells you where it was freed and where it was used, and you have to work out who
kept a copy.

## ASan vs valgrind

| | ASan | Valgrind (Memcheck) |
| --- | --- | --- |
| How | Compiler inserts a check before every access | Runs the binary on a simulated CPU; replaces `malloc`/`free`/`new`/`delete` |
| Rebuild? | Yes, `-fsanitize=address` on compile **and** link | No. Any binary, including ones you didn't build |
| Speed | ~2x slower | Much slower (tens of times) |
| On error | Aborts at the first | Reports and continues; many errors per run |
| Together? | No. Both hook the allocator. Build without ASan to use valgrind | |

Rule of thumb: **ASan in debug builds and CI**, because it's cheap enough to leave on. Use
**valgrind** when you can't rebuild (a vendor `.so`, a driver) or want every error from one run.
Either way, **keep `-g`**, or the stacks have addresses instead of `main.cpp:39`.

## The rules

- **A raw pointer from `.get()` is a borrow, never ownership.** It must not outlive the owner.
- **Freeing doesn't null anyone's pointer.** Only the owner's own pointer is reset (and only by a
  move or `reset`).
- **A plausible address and the right value prove nothing.** Only a tool can tell you the access
  is valid.
- **Make sure the UB you're testing is actually executed.** Unused expressions get dropped.
- **Read below frame `#0`.** The top frame is the tool's own `operator new`/`delete`. Your code
  is the first `main.cpp` frame under it.

## Open questions

- Which line in *real* code decides how long a borrowed pointer may live? Nothing in the type
  says. (Some languages check lifetimes at compile time; C++ doesn't.)
- **Dangling references** (`int& r = *p;`) present the same way. What about a reference to a
  local returned from a function? The compiler warns about some of these. Which ones?
- `shared_ptr` + `weak_ptr` is the standard fix when a borrower may outlive the owner. How does
  `weak_ptr::lock()` know the object is gone?

## Where this returns

ROS 2 callbacks receive messages as `shared_ptr` precisely so a callback can't be left holding a
freed message. Week 6 threads make this bug much worse: another thread frees the memory, and the
use-after-free happens only on some runs. ASan's sibling, ThreadSanitizer, is the tool there.
