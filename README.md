# Path Planning Assignment

## 1. Project Overview

This project implements a simple geometric path planning solution for an autonomous racing car using detected track cones.

The car is given:

* Its current position and heading.
* The detected cones around the car.
* The color of each cone.

Blue cones represent the left side of the track, while yellow cones represent the right side.

The planner uses the cone positions and the current vehicle heading to generate a sequence of `(x, y)` points representing the desired path of the car.

---

## 2. Path Planning Approach

The implemented solution uses a geometric approach based on the available cone detections.

### Both Blue and Yellow Cones

When cones from both sides are available, the planner estimates the center of the track using the detected cones.

When the number of cones on both sides is equal, the cones are paired according to their position along the vehicle's forward direction, and the midpoint between each pair is used as a center point.

When one side contains more cones than the other, the available cones are matched as reasonably as possible and the remaining cones are shifted toward the expected center of the track.

### Only Blue Cones

When only blue cones are detected, they are treated as the left boundary of the track.

The direction of the boundary is estimated from the detected cones. The planner then shifts the boundary toward the inside of the track to estimate the centerline.

### Only Yellow Cones

When only yellow cones are detected, they are treated as the right boundary of the track.

The same approach is used, but the boundary is shifted toward the left side of the track to estimate the centerline.

### No Cones

If no cones are detected, the planner generates a path using the current heading of the car.

This provides a fallback when there is not enough information to estimate the track boundaries.

---

## 3. Path Generation

The generated path is approximately:

* 8 meters long.
* 0.4 meters between consecutive path points.
* 20 path points.

The path is generated in the global/world coordinate frame.

The planner starts from the current vehicle position and initially follows the current vehicle heading before following the estimated track direction.

---

## 4. Handling Unequal Cone Counts

The planner was extended to handle situations where the number of detected cones is different on each side of the track.

For example, the planner can handle a situation where three cones are detected on one side and only one cone is detected on the other side.

The additional scenarios are:

### Scenario 21

Three blue cones are detected on the left side of the track and one yellow cone is detected on the right side.

### Scenario 22

Three yellow cones are detected on the right side of the track and one blue cone is detected on the left side.

These scenarios are used to test the planner when the cone detections are not balanced between the two sides.

---

## 5. Assumptions

The implementation uses the following assumptions:

* Blue cones represent the left side of the track.
* Yellow cones represent the right side of the track.
* The approximate track width is 3 meters.
* When only one boundary is visible, the centerline is estimated approximately 1.5 meters from that boundary.
* Cone coordinates are expressed in meters.
* The car heading (`yaw`) is expressed in radians.
* `yaw = 0` means the car is facing along the positive X-axis.
* `yaw = π/2` means the car is facing along the positive Y-axis.
* The detected cone positions are assumed to be reasonably accurate.
* The path is generated approximately 8 meters ahead of the vehicle.

---

## 6. Limitations

This implementation intentionally uses a simple geometric method rather than a complex path planning algorithm.

Some limitations include:

* The assumed track width may not exactly match the real track width.
* Pairing cones based on their position may not always produce the ideal centerline on highly irregular tracks.
* Noisy or incorrect cone detections may affect the generated path.
* Very sharp curves may require a more advanced curve-fitting approach.
* The solution does not include vehicle dynamics or dynamic obstacle avoidance.

A more advanced implementation could use spline fitting, filtering, clustering, or model-based path planning to improve robustness.

---

## 7. Test Scenarios

The project contains 22 predefined scenarios covering different cone configurations.

The scenarios include:

* No detected cones.
* A single detected cone.
* Cones on one side only.
* Cones on both sides.
* Different vehicle headings.
* Different cone positions.
* Unequal numbers of blue and yellow cones.
* Three cones on one side and one cone on the other side.

The generated paths can be visually inspected using the provided visualizer.

---

## 8. Project Structure

```text
Path Planning Task/
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── path_planning.py
│   ├── scenarios.py
│   ├── run.py
│   └── tester.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Main Files

**models.py**

Defines the data structures for cones, the car pose, and the generated 2D path.

**path_planning.py**

Contains the main `PathPlanning` class and the `generatePath()` implementation.

**scenarios.py**

Contains the predefined test scenarios, including the additional scenarios for the three-cone cases.

**run.py**

Runs the visualizer for a selected scenario.

**tester.py**

Provides the visualization and testing functionality for the path planner.

---

## 9. How to Run

### 1. Open the project

Open the project folder in VS Code and open a PowerShell terminal.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

### 4. Install the required dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run a scenario

Run any scenario by specifying its number:

```powershell
python -m src.run --scenario 1
```

For example:

```powershell
python -m src.run --scenario 3
```

### 6. Run Scenario 21

Scenario 21 contains three blue cones and one yellow cone:

```powershell
python -m src.run --scenario 21
```

### 7. Run Scenario 22

Scenario 22 contains three yellow cones and one blue cone:

```powershell
python -m src.run --scenario 22
```

The visualizer displays:

* The detected cones.
* The car position.
* The car heading.
* The generated path.

### 8. Deactivate the virtual environment

When finished, the virtual environment can be deactivated using:

```powershell
deactivate
```

---

## 10. Conclusion

The final implementation provides a simple and understandable geometric path planner that handles the main cases required by the assignment.

It supports:

* No detected cones.
* One-sided cone detection.
* Both blue and yellow boundaries.
* Unequal numbers of cones on the two sides.
* Three-cone test cases.
* Generation of a continuous path with approximately 0.4 meter spacing.
* A fallback path based on the current vehicle heading when there is insufficient cone information.

The solution focuses on simplicity, clear assumptions, and handling the different cone configurations included in the test scenarios.
