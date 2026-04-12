import numpy as np

from data.demo_grids import grid_data, src_points, dest_points
from classical_planners.AStar import a_star_search
from stages.VLoSPS import VLoSPS
from stages.DAPPA import DAPPA
from stages.BCPA import BCPA
from stages.OLoSPR import OLoSPR
from utils.path_processing import densify_path
from utils.path_metrics import calculate_path_length
from smoothing.bezier_curve import get_intermediate_quadratic_bezier_curve_points
from smoothing.bspline_smooth import bspline_smooth

def run_pipeline(grid_index: int = 1):
    grid = np.array(grid_data[grid_index])
    start = tuple(src_points[grid_index])
    goal = tuple(dest_points[grid_index])

    raw_path = a_star_search(grid, start, goal)
    vlosps_path = VLoSPS(grid, raw_path)
    dappa_path = DAPPA(vlosps_path, grid)
    bcpa_path = BCPA(grid_data[grid_index], dappa_path)
    olospr_path = OLoSPR(grid_data[grid_index], bcpa_path)

    dense_path = densify_path(olospr_path, 1)
    quadratic_path, rational_quadratic_path = get_intermediate_quadratic_bezier_curve_points(dense_path)
    bspline_path = bspline_smooth(vlosps_path, degree=3, smoothing=5, num=50, periodic=False)

    outputs = {
        "grid_index": grid_index,
        "start": start,
        "goal": goal,
        "raw_path": raw_path,
        "vlosps_path": vlosps_path,
        "dappa_path": dappa_path,
        "bcpa_path": bcpa_path,
        "olospr_path": olospr_path,
        "quadratic_path": quadratic_path,
        "rational_quadratic_path": rational_quadratic_path,
        "bspline_path": bspline_path,
    }

    print(f"Grid index: {grid_index}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    for key in ["raw_path", "vlosps_path", "dappa_path", "bcpa_path", "olospr_path", "quadratic_path"]:
        value = outputs[key]
        print(f"{key:<24} length = {calculate_path_length(value):.3f}   points = {len(value)}")

    return outputs

if __name__ == "__main__":
    run_pipeline(grid_index=1)
