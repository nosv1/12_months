# Week 5 20260926 - 20261003 — STL and idiom

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260926 1716 - 1835 (1.32 hours -- week 5 started early, same sitting as week 4's close. labs/w05-sensor-processing/: design talk, no buffer yet. IMU chosen; accel integration + drift as the Processor/Statistics story. Dropped the Reading base class (no interface to name); vector<vector<double>> considered and rejected; build IMUBuffer first, generalize to SensorBuffer<T> when TempReading arrives (this week). Slicing reasoned out, not yet run. Headers: time_t -> steady_clock time_point, mps2/rad_s units, gyro added. Builds and runs. Stopped on decision fatigue)
