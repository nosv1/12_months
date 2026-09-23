# Week 3 20260922 - 20260928 — C++ that compiles

## **Built:** what exists now that didn't before  

## **Broke:** what went wrong, and the actual root cause  

## **Learned:** the thing you'd tell past-you  

## **Stuck on:** open questions carried forward  

## **Hours:** actual, not aspirational  

20260922 1737 - 1940 (2.05 hours -- C++ week 3 night 1: preprocessor/compile/assemble/link walked stage by stage on hello.cpp (36,588 -> 67 lines); three-file Reading build by hand with -c and manual link; ODR bug diagnosed (reading.cpp redefined the struct instead of including the header); all three ODR failure modes produced deliberately incl. the file-scope `static` that hid one; CMakeLists + out-of-source build; destructors, LIFO destruction order, and a visible leak from `new` with no delete; unique_ptr explained; textbook 20)

20260923 0832 - 0937 (1.08 hours -- week 3 step 5: copy constructors made visible; value/reference/const-reference passing; aliasing; dangling reference returned from a function, caught by -Wreturn-local-addr and segfaulting because GCC emitted a null reference; references cannot be rebound; const member functions and the hidden `this`. Week 3 checklist complete. cpp_telemetry/SPEC.md written; textbook 21)

20260923 1058 - 1307 (2.15 hours -- cpp_telemetry started: CMake, Reading struct with member initializer list, to_string via ostringstream, CSV read into vector<vector<string>>, strong types (Timestamp/RobotID/Velocity/Battery/Temperature) adopted unprompted. Hit and diagnosed: most vexing parse, uncaught std::invalid_argument found with gdb `catch throw`, segfault from unchecked operator[] on a truncated row. clang-format + format-on-save configured. Textbook 22)

### Estimated Task Times

