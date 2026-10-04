# Path Planning Assignment

## Overview

This project implements a simple geometric path planning solution for an autonomous racing car using detected track cones.

The car receives:

* Its current position and heading.
* The detected cones around the car.
* The color of each cone.

Blue cones represent the **left side** of the track, while yellow cones represent the **right side**.

The planner receives the car pose and detected cones and returns a sequence of path points in world coordinates.

## Approach

The solution uses the color of the cones to determine the track boundaries.

When both blue and yellow cones are detected, blue cones are paired with the closest yellow cones. The midpoint of each pair is used as an approximation of the track center.

When only blue cones are available, the blue cones are treated as the left boundary. The planner estimates the track center by shifting the boundary toward the inside of the track.

When only yellow cones are available, the same idea is applied in the opposite direction.

When no cones are detected, the planner generates a straight path using the current vehicle heading.

The generated path is approximately 8 meters long with points spaced by 0.4 meters.

## Part 2

For the case where three cones are detected on the same side, the available cones are treated as multiple observations of the same track boundary.

The boundary direction is estimated from the detected cones and the path is shifted toward the expected center of the track.

Two additional scenarios were added:

- Scenario 21: three blue cones
- Scenario 22: three yellow cones

## Assumptions

The implementation uses the following assumptions:

1. Blue cones represent the left boundary.
2. Yellow cones represent the right boundary.
3. The approximate track width is 3 meters.
4. The center of the track is therefore approximately 1.5 meters from a single detected boundary.
5. The car should initially follow its current heading when insufficient cone information is available.
6. The detected cones are reliable and do not contain significant measurement noise.

## Limitations

This solution is intentionally simple and geometric.

It does not implement SLAM, dynamic obstacle avoidance, vehicle dynamics, global map planning, or advanced curve fitting.

When only one side of the track is visible, the planner relies on the assumed track width. If the real track width changes significantly, the generated centerline may not be accurate.

Highly curved tracks or noisy cone detections could also require a more advanced method such as spline fitting or filtering.

## Running the Project

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1