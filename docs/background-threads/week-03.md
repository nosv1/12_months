# Week 3 20260922 - 20260928 — C++ that compiles

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260922 1737 - 1940 (2.05 hours -- C++ week 3 night 1: preprocessor/compile/assemble/link walked stage by stage on hello.cpp (36,588 -> 67 lines); three-file Reading build by hand with -c and manual link; ODR bug diagnosed (reading.cpp redefined the struct instead of including the header); all three ODR failure modes produced deliberately incl. the file-scope `static` that hid one; CMakeLists + out-of-source build; destructors, LIFO destruction order, and a visible leak from `new` with no delete; unique_ptr explained; textbook 20)

### Estimated Task Times

