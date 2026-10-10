# Stealth goal seeker (idea, 2026-10-10)

From his grad robotics class, about three years ago. Never finished because the class ended.

## The problem

- **Blue robot**: reach a goal.
- **Two or three red robots**: move along **predetermined paths**, each with a detection cone.
- Map of the space built with SLAM beforehand.

## What the class already had working

- Route planning to the goal, without detectors.
- Proportional navigation to avoid the detector robots.

## The open problem, in his words

"How do you avoid the red robot and also stay optimal to getting to the goal."

## Status

He wants it **in the curriculum**, maybe as the project that the reshape is built around. Next step:
he brings the original project details (assignment, code if he still has it). Design is his.
Flight-instructor terms apply.

## The original code (found 10-10)

Course: **ME5501 Robotics, Fall 2022**, ROS 2 (`rclpy`) + Gazebo + TurtleBot3.

- [seagraves_unmanned_systems_pkg](https://github.com/nosv1/seagraves_unmanned_systems_pkg):
  ROS 2 package. `TagYoureIt/pursuer.py` and `evader.py` (pursuit-evasion between two TurtleBots),
  `support_module/PN.py` (proportional navigation), `PID.py`, `DetectedObject.py` (lidar object
  detection), `PathFollower/`, `multi_bots.py`, `post_processing/LogPlotter.py`.
- [seagraves_unmanned_systems](https://github.com/nosv1/seagraves_unmanned_systems): homeworks.
  `SearchAlgorithms/` has Dijkstra, A*, RRT, Dubins testing, and a GA for TSP, with JSON scenarios.
  `Exam2/` has TagYoureIt videos, A* TSP, and a Gazebo world. `HW6/` is the PN write-up.
- **The detector-cone scenario itself isn't in either repo.** The class ended before it was built.
