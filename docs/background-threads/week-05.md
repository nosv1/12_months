# Week 5 20260926 - 20261003 — STL and idiom

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260926 1716 - 1835 (1.32 hours -- week 5 started early, same sitting as week 4's close. labs/w05-sensor-processing/: design talk, no buffer yet. IMU chosen; accel integration + drift as the Processor/Statistics story. Dropped the Reading base class (no interface to name); vector<vector<double>> considered and rejected; build IMUBuffer first, generalize to SensorBuffer<T> when TempReading arrives (this week). Slicing reasoned out, not yet run. Headers: time_t -> steady_clock time_point, mps2/rad_s units, gyro added. Builds and runs. Stopped on decision fatigue)

20260927 0725 - 0824 (0.98 hours -- oral explain-backs from the car, voice-to-text. 10 textbook questions across entries 02-26, concept only. Ideas solid; vocabulary slips (leak vs dangling, "points to" vs "refers to", what std::move returns). explicit / implicit conversion was the one real gap, closed on the second pass)

20260927 1721 - 1835 (1.23 hours -- break, not sign-off. Start is my first `date` of the session. Sunday review: textbook 27 stranded on the aerospace branch, build log sections empty weeks 2-5, bench kit due wk 6. IMUBuffer v1 reviewed (public vector, off-by-one on capacity, erase(begin), const u_long member, always-0 int return). Taught: gtest + library/exe/test layout, struct vs class, public vs private, static constexpr / template N / runtime capacity. Ring buffer derived: shifting is the O(N) cost, linked list rejected on allocation/cache, mod for wrap, head + tail; chose capacity via constructor. Open: head == tail ambiguity)
