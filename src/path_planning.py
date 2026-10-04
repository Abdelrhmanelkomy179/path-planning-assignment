from __future__ import annotations

from typing import List
import math

from src.models import CarPose, Cone, Path2D


class PathPlanning:
    """Student-implemented path planner."""

    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        """Generate a drivable center path from detected track cones."""

        # ------------------------------------------------------------
        # Configuration
        # ------------------------------------------------------------
        STEP = 0.4
        PATH_LENGTH = 8.0
        HALF_TRACK_WIDTH = 1.5

        num_points = int(PATH_LENGTH / STEP)

        cx = self.car_pose.x
        cy = self.car_pose.y
        yaw = self.car_pose.yaw

        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        def forward_projection(point):
            """Distance of a point in the car's forward direction."""
            dx = point[0] - cx
            dy = point[1] - cy
            return dx * cos_yaw + dy * sin_yaw

        def distance(a, b):
            return math.hypot(a[0] - b[0], a[1] - b[1])

        def boundary_center_points(boundary):
            """
            Estimate centerline points from a single boundary.

            The center is estimated by shifting the boundary inward
            by HALF_TRACK_WIDTH.
            """
            if not boundary:
                return []

            boundary = sorted(boundary, key=forward_projection)

            if len(boundary) == 1:
                p = boundary[0]

                # Use vehicle heading as the local boundary direction.
                dx = cos_yaw
                dy = sin_yaw
            else:
                p1 = boundary[0]
                p2 = boundary[-1]

                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]

                length = math.hypot(dx, dy)

                if length < 1e-6:
                    dx = cos_yaw
                    dy = sin_yaw
                else:
                    dx /= length
                    dy /= length

            # Two possible normals.
            n1 = (-dy, dx)
            n2 = (dy, -dx)

            # Choose the normal pointing approximately toward the car.
            bx = sum(p[0] for p in boundary) / len(boundary)
            by = sum(p[1] for p in boundary) / len(boundary)

            to_car_x = cx - bx
            to_car_y = cy - by

            dot1 = n1[0] * to_car_x + n1[1] * to_car_y
            dot2 = n2[0] * to_car_x + n2[1] * to_car_y

            normal = n1 if dot1 >= dot2 else n2

            return [
                (
                    p[0] + normal[0] * HALF_TRACK_WIDTH,
                    p[1] + normal[1] * HALF_TRACK_WIDTH,
                )
                for p in boundary
            ]

        def make_polyline_path(anchors):
            """
            Create equally spaced path points along a polyline.
            """
            if len(anchors) == 0:
                anchors = [
                    (cx, cy),
                    (
                        cx + cos_yaw * PATH_LENGTH,
                        cy + sin_yaw * PATH_LENGTH,
                    ),
                ]

            # Remove duplicate consecutive points.
            clean = [anchors[0]]

            for p in anchors[1:]:
                if distance(clean[-1], p) > 1e-6:
                    clean.append(p)

            if len(clean) == 1:
                clean.append(
                    (
                        clean[0][0] + cos_yaw * PATH_LENGTH,
                        clean[0][1] + sin_yaw * PATH_LENGTH,
                    )
                )

            # Build cumulative distances.
            cumulative = [0.0]

            for i in range(1, len(clean)):
                cumulative.append(
                    cumulative[-1] + distance(clean[i - 1], clean[i])
                )

            total = cumulative[-1]

            # Extend the final direction so we always have an 8 m path.
            if len(clean) >= 2:
                last = clean[-1]
                previous = clean[-2]

                dx = last[0] - previous[0]
                dy = last[1] - previous[1]

                length = math.hypot(dx, dy)

                if length < 1e-6:
                    dx = cos_yaw
                    dy = sin_yaw
                else:
                    dx /= length
                    dy /= length

                extension = PATH_LENGTH + 2.0

                clean.append(
                    (
                        last[0] + dx * extension,
                        last[1] + dy * extension,
                    )
                )

                cumulative = [0.0]

                for i in range(1, len(clean)):
                    cumulative.append(
                        cumulative[-1] + distance(clean[i - 1], clean[i])
                    )

                total = cumulative[-1]

            # Sample points every STEP meters.
            path = []

            for k in range(1, num_points + 1):
                target = min(k * STEP, PATH_LENGTH)

                # Find segment.
                segment = 0

                while (
                    segment < len(cumulative) - 1
                    and cumulative[segment + 1] < target
                ):
                    segment += 1

                d0 = cumulative[segment]
                d1 = cumulative[segment + 1]

                if d1 - d0 < 1e-9:
                    ratio = 0.0
                else:
                    ratio = (target - d0) / (d1 - d0)

                x = (
                    clean[segment][0]
                    + ratio
                    * (clean[segment + 1][0] - clean[segment][0])
                )

                y = (
                    clean[segment][1]
                    + ratio
                    * (clean[segment + 1][1] - clean[segment][1])
                )

                path.append((x, y))

            return path

        # ------------------------------------------------------------
        # Separate cones by color
        # ------------------------------------------------------------
        blue = [(cone.x, cone.y) for cone in self.cones if cone.color == 1]
        yellow = [(cone.x, cone.y) for cone in self.cones if cone.color == 0]

        # ------------------------------------------------------------
        # CASE 1: No cones
        # ------------------------------------------------------------
        if not blue and not yellow:
            anchors = [
                (cx, cy),
                (
                    cx + cos_yaw * PATH_LENGTH,
                    cy + sin_yaw * PATH_LENGTH,
                ),
            ]

            return make_polyline_path(anchors)

        # ------------------------------------------------------------
        # CASE 2: Both sides detected
        # ------------------------------------------------------------
        if blue and yellow:
            pairs = []
            remaining_yellow = yellow.copy()

            # Pair each blue cone with its closest yellow cone.
            for b in blue:
                if not remaining_yellow:
                    break

                closest = min(
                    remaining_yellow,
                    key=lambda y: distance(b, y),
                )

                remaining_yellow.remove(closest)

                midpoint = (
                    (b[0] + closest[0]) / 2.0,
                    (b[1] + closest[1]) / 2.0,
                )

                pairs.append(midpoint)

            # Keep only center points that are in front of the car.
            forward_pairs = [
                p for p in pairs
                if forward_projection(p) > -0.5
            ]

            if forward_pairs:
                forward_pairs.sort(key=forward_projection)

                anchors = [(cx, cy)] + forward_pairs

                return make_polyline_path(anchors)

            # If detected boundaries are behind the car,
            # use the car heading as a safe fallback.
            anchors = [
                (cx, cy),
                (
                    cx + cos_yaw * PATH_LENGTH,
                    cy + sin_yaw * PATH_LENGTH,
                ),
            ]

            return make_polyline_path(anchors)

        # ------------------------------------------------------------
        # CASE 3: Only blue cones
        # Blue = left boundary.
        # Shift inward toward the right.
        # ------------------------------------------------------------
        if blue:
            center_points = boundary_center_points(blue)

            forward_points = [
                p for p in center_points
                if forward_projection(p) > -0.5
            ]

            if forward_points:
                forward_points.sort(key=forward_projection)
                return make_polyline_path(
                    [(cx, cy)] + forward_points
                )

            return make_polyline_path(
                [
                    (cx, cy),
                    (
                        cx + cos_yaw * PATH_LENGTH,
                        cy + sin_yaw * PATH_LENGTH,
                    ),
                ]
            )

        # ------------------------------------------------------------
        # CASE 4: Only yellow cones
        # Yellow = right boundary.
        # Shift inward toward the left.
        # ------------------------------------------------------------
        center_points = boundary_center_points(yellow)

        forward_points = [
            p for p in center_points
            if forward_projection(p) > -0.5
        ]

        if forward_points:
            forward_points.sort(key=forward_projection)
            return make_polyline_path(
                [(cx, cy)] + forward_points
            )

        return make_polyline_path(
            [
                (cx, cy),
                (
                    cx + cos_yaw * PATH_LENGTH,
                    cy + sin_yaw * PATH_LENGTH,
                ),
            ]
        )