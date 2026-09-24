# Week 4 20260924 - 20261001 — Memory and ownership

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260924 1720 - 1808 (0.80 hours -- start time his estimate, "probably 1720". Boss Fight #1 closed as a pass with gaps; weeks 1-3 ticked. cpp_memory/: leak that looked fine -> LeakSanitizer naming the line (after hitting undefined __asan_ refs: flag needed on link too) -> throw skipping the delete -> RAII class (first without a destructor, still leaked) -> clean on the throwing path -> "b is just renaming a" -> double free -> copy ctor = delete -> unique_ptr's identical deleted-copy error. 38 min vs his 1h estimate. Textbook 24)
