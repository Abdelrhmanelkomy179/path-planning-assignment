# Path Planning Assignment


## 1. Project Overview

This project implements a simple geometric path planning solution for an autonomous racing car using detected track cones.

The car receives:

* Its current position and heading.
* The detected cones around the car.
* The color of each cone.

Blue cones represent the **left side** of the track, while yellow cones represent the **right side**.

The planner generates a sequence of `(x, y)` points representing the desired path of the car.

---

## 2. Path Planning Approach

The implemented solution uses a simple geometric approach.

### Case 1: Both Blue and Yellow Cones Are Available

When cones from both sides are detected, each blue cone is paired with the closest yellow cone.

The midpoint between the two cones is calculated and used as an approximation of the center of the track.

These center points are then connected to generate the vehicle path.

### Case 2: Only Blue Cones Are Available

When only blue cones are detected, they are treated as the left boundary of the track.

The direction of the boundary is estimated from the detected cones. The planner then shifts the boundary approximately **1.5 meters toward the inside of the track** to estimate the centerline.

### Case 3: Only Yellow Cones Are Available

The same approach is used when only yellow cones are detected.

The yellow cones are treated as the right boundary, and the estimated centerline is generated approximately 1.5 meters toward the inside of the track.

### Case 4: No Cones Are Available

If no cones are detected, the planner generates a straight path using the current heading of the car.

This provides a reasonable fallback when there is not enough information to estimate the track boundaries.

---

## 3. Path Generation

The generated path is approximately:

* **8 meters long**
* **0.4 meters between consecutive points**
* **20 path points**

The path is generated in the global/world coordinate frame.

The planner also starts the path from the current car position and follows the estimated direction of the track.

---

## 4. Handling Three Cones on One Side

For Part 2 of the assignment, the planner was extended to handle multiple cones detected on the same side.

When three cones are detected on one side, they are considered multiple observations of the same track boundary.

The planner:

1. Sorts the detected boundary cones according to their position in front of the vehicle.
2. Estimates the direction of the boundary.
3. Determines the inward direction toward the expected track center.
4. Shifts the boundary points by the assumed half track width.
5. Uses the resulting points to generate the path.

Two additional test scenarios were added:

* **Scenario 21:** Three blue cones.
* **Scenario 22:** Three yellow cones.

---

## 5. Assumptions

The implementation uses the following assumptions:

1. Blue cones represent the left side of the track.
2. Yellow cones represent the right side of the track.
3. The approximate track width is 3 meters.
4. Therefore, when only one boundary is visible, the centerline is estimated approximately 1.5 meters from that boundary.
5. The detected cones are assumed to be reasonably accurate.
6. The car initially follows its current heading when there is insufficient information.
7. The path is generated for approximately 8 meters ahead of the vehicle.

---

## 6. Limitations

This solution intentionally uses a simple geometric method rather than a complex path planning algorithm.

Possible limitations include:

* The assumed track width may not match the real track width.
* Pairing each blue cone with the closest yellow cone may not always produce the correct pair on highly irregular tracks.
* Noisy or incorrect cone detections may affect the generated path.
* Very sharp curves may require a more advanced curve-fitting method.
* The solution does not include dynamic obstacle avoidance or vehicle dynamics.

A more advanced implementation could use spline fitting, filtering, clustering, or model-based path planning to improve robustness.

---

## 7. Test Scenarios

The original test scenarios provided with the assignment were used to evaluate the implementation.

Additional scenarios were added for the three-cone case:

### Scenario 21

Three blue cones are detected on the left side of the track.

### Scenario 22

Three yellow cones are detected on the right side of the track.

The generated paths were visually inspected using the provided project visualizer.

---

## 8. Project Structure

```text
Path Planning Task/
│
├── README.md
├── requirements.txt
├── .gitignore
│
└── src/
    ├── __init__.py
    ├── models.py
    ├── path_planning.py
    ├── scenarios.py
    ├── run.py
    └── tester.py
```

### Main Files

**`models.py`**
Defines the data structures for cones, car pose, and the generated 2D path.

**`path_planning.py`**
Contains the main `PathPlanning` class and the `generatePath()` implementation.

**`scenarios.py`**
Contains the provided test scenarios and the additional scenarios for Part 2.

**`run.py`**
Runs the visualizer for a selected scenario.

**`tester.py`**
Provides testing functionality for the path planner.

---

## 9. How to Run

Create and activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run a scenario:

```powershell
python -m src.run --scenario 1
```

For example:

```powershell
python -m src.run --scenario 3
```

Three-cone test cases:

```powershell
python -m src.run --scenario 21
python -m src.run --scenario 22
```

---

## 10. Conclusion

The final implementation provides a simple and understandable geometric path planner that handles the main cases required by the assignment.

It supports:

* No detected cones.
* One-sided cone detection.
* Both blue and yellow boundaries.
* Multiple cones on one side.
* Generation of a continuous path with a maximum point spacing below 0.5 meters.
* Additional test scenarios for the three-cone case.

The solution focuses on simplicity and clear assumptions, as requested in the assignment.

## GitHub Repository

The complete project, source code, test scenarios, and documentation are provided in the public GitHub repository.

**Repository:**
[PASTE YOUR PUBLIC GITHUB REPOSITORY LINK HERE]
