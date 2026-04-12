import math
import numpy as np
from .rational_quadratic_bezier_curve import rational_quadratic_bezier_curve

def bezier_curve(P0, P1, P2, num_points=3):
    curve = []
    for t in np.linspace(0, 1, num_points):
        point = (1 - t)**2 * np.array(P0) + 2 * (1 - t) * t * np.array(P1) + t**2 * np.array(P2)
        curve.append(point.tolist())
    return curve

def get_intermediate_quadratic_bezier_curve_points(waypoints):
    quadratic_bezier_curve_points = []
    num_intermediate = 1
    if len(waypoints) < 2:
        return list(waypoints)
    expanded_path = [waypoints[0]]
    for i in range(len(waypoints) - 1):
        start_point = waypoints[i]
        end_point = waypoints[i + 1]
        for j in range(1, num_intermediate + 1):
            fraction = j / (num_intermediate + 1)
            intermediate_x = start_point[0] + (end_point[0] - start_point[0]) * fraction
            intermediate_y = start_point[1] + (end_point[1] - start_point[1]) * fraction
            expanded_path.append([intermediate_x, intermediate_y])
        expanded_path.append(end_point)

    if len(expanded_path) < 3:
        return expanded_path

    final_path = [expanded_path[0]]  # Start with the first point
    final_path_rational_quadratic_bezier_curve = [expanded_path[0]]
    i = 1
    while i < len(expanded_path) - 1:
        prev_point = expanded_path[i - 1]
        current_point = expanded_path[i]
        next_point = expanded_path[i + 1]

        # Calculate vectors from previous to current and current to next points
        vector1 = (current_point[0] - prev_point[0], current_point[1] - prev_point[1])
        vector2 = (next_point[0] - current_point[0], next_point[1] - current_point[1])

        # Calculate dot product and cross product for angle and rotation direction
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        # Calculate vector magnitudes
        magnitude1 = (vector1[0] ** 2 + vector1[1] ** 2) ** 0.5
        magnitude2 = (vector2[0] ** 2 + vector2[1] ** 2) ** 0.5

        # Calculate angle between vectors
        if magnitude1 == 0 or magnitude2 == 0:
            cosine_angle = -2  # Handle potential division by zero
        else:
            cosine_angle = dot_product / (magnitude1 * magnitude2)

        angle_degrees = round(math.degrees(math.acos(np.clip(cosine_angle, -1.0, 1.0))), 1) # Clip cosine_angle

        if 0 < angle_degrees < 180:
            bezier_points = bezier_curve(prev_point, current_point, next_point)
            rational_quadratic_bezier_points = rational_quadratic_bezier_curve(prev_point, current_point, next_point)
            final_path.extend(bezier_points[:-1]) # Add all bezier points except the last one (which is the next control point)
            final_path_rational_quadratic_bezier_curve.extend(rational_quadratic_bezier_points[:-1])
            i += 1 # Skip the 'current_point' as it's now part of the bezier curve
        else:
            final_path.append(current_point)
            final_path_rational_quadratic_bezier_curve.append(current_point)
        i += 1

    final_path.append(expanded_path[-1]) # Add the last point
    final_path_rational_quadratic_bezier_curve.append(expanded_path[-1])
    return final_path, final_path_rational_quadratic_bezier_curve
