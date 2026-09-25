# Week 4 20260924 - 20261001 — Memory and ownership

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260924 1720 - 1808 (0.80 hours -- start time his estimate, "probably 1720". Boss Fight #1 closed as a pass with gaps; weeks 1-3 ticked. cpp_memory/: leak that looked fine -> LeakSanitizer naming the line (after hitting undefined __asan_ refs: flag needed on link too) -> throw skipping the delete -> RAII class (first without a destructor, still leaked) -> clean on the throwing path -> "b is just renaming a" -> double free -> copy ctor = delete -> unique_ptr's identical deleted-copy error. 38 min vs his 1h estimate. Textbook 24)

20260925 1703 - 1824 (1.35 hours -- break, not sign-off. Move semantics: moved-from unique_ptr is null (predicted the int itself moves; addresses showed it doesn't) -> *a aborts via _GLIBCXX_ASSERTIONS, SEGV at 0x0 under ASan alone -> Tracer copy/move ctors (first attempt delegated to itself) -> 5/6 predictions right; push_back(move(b)) moved, plus a reallocation move -> drop noexcept, relocation becomes copy -> drop move ctor, std::move runs a copy -> std::move is a cast (4 guesses, then told). shared_ptr: use_count through copy/scope/move/reset, dtor at last owner; unique_ptr by default. Noisy location. Textbook 25)
