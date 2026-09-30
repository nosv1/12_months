# Week 5 20260926 - 20261003 — STL and idiom

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260926 1716 - 1835 (1.32 hours -- week 5 started early, same sitting as week 4's close. labs/w05-sensor-processing/: design talk, no buffer yet. IMU chosen; accel integration + drift as the Processor/Statistics story. Dropped the Reading base class (no interface to name); vector<vector<double>> considered and rejected; build IMUBuffer first, generalize to SensorBuffer<T> when TempReading arrives (this week). Slicing reasoned out, not yet run. Headers: time_t -> steady_clock time_point, mps2/rad_s units, gyro added. Builds and runs. Stopped on decision fatigue)

20260927 0725 - 0824 (0.98 hours -- oral explain-backs from the car, voice-to-text. 10 textbook questions across entries 02-26, concept only. Ideas solid; vocabulary slips (leak vs dangling, "points to" vs "refers to", what std::move returns). explicit / implicit conversion was the one real gap, closed on the second pass)

20260927 1721 - 1835 (1.23 hours -- break, not sign-off. Start is my first `date` of the session. Sunday review: textbook 27 stranded on the aerospace branch, build log sections empty weeks 2-5, bench kit due wk 6. IMUBuffer v1 reviewed (public vector, off-by-one on capacity, erase(begin), const u_long member, always-0 int return). Taught: gtest + library/exe/test layout, struct vs class, public vs private, static constexpr / template N / runtime capacity. Ring buffer derived: shifting is the O(N) cost, linked list rejected on allocation/cache, mod for wrap, head + tail; chose capacity via constructor. Open: head == tail ambiguity)

20260927 2030 - 2119 (0.82 hours -- start his, "came back at 2030". Ring: why head (reading oldest->newest), tail + count with count = size(); first ring overwrote the wrong slot (tail_idx meant "next" in the push_back branch, "last written" in the overwrite branch), fixed by trace, not yet by test. Map and pre-fill considered; stayed with grow-then-overwrite. gtest wired via FetchContent, no tests yet, no library split. Committed 8e540a6. Stopped tired. Textbook 28, 29)

20260928 1631 - 1829 (1.97 hours -- bench kit: Pi 5 dropped for his Pi 4 4GB (verified over ssh), cart reviewed (motor variant/encoder, DRV8825 needs >8.2 V -> 12 V adapter, IMU + MAX31855 from Adafruit/SparkFun, soldering iron?), not yet ordered. Week-5 end state set. Templates vs abstract classes taught. add_library done; ASan undefined refs -> link flag INTERFACE. Capacity + order tests green; operator== needed const this; operator<< declared in header. get_ordered_readings under-full bug found by review, untested. Textbook 30, 31)

20260929 1800 - 1933 (1.55 hours -- fixtures (TEST_F, fixed timestamps). Under-full test aborted on operator[] `__n < size()`; prints failed (abort doesn't flush cout), gdb backtrace found it in get_ordered_readings, not add_reading. Fixed with a branch, then his cleaner `% size()`. Empty, exactly-N, 7-into-3 tests. IMUBuffer -> SensorBuffer<T> header-only; bodies written per-type twice before 'once, in T'. TemperatureReading added (TempReading read as 'temporary'). 7 tests green, all committed by him. Textbook 32, 33)
