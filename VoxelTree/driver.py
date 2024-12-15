# Thomas Safago
# 11/17/2024

from Point import Point
from VoxelTreePointCloud import VoxelTreePointCloud

from random import uniform, randint
import time


# def main():
#     points_amount = 10
#     radius = .1
#     points_list = [None] * points_amount
#
#     for i in range(points_amount):
#         points_list[i] = Point(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
#
#     print(f"\nStarting r={radius} search on Voxel Point Cloud (n={points_amount})...")
#     st = time.time()
#     voxelpc1 = VoxelTreePointCloud(points_list)
#     voxelpc1.radius_search(Point(0, 0, 0), radius)
#     et = time.time()
#     print(f"Search finished! Time elapsed: {et - st} seconds.")
#     point_values = [print(point.x, point.y, point.z) for point in points_list]

def main():
    # Number of points to generate
    points_amount = 1000
    radius = .1
    print(f"Generating {points_amount} random points...")

    # Generate points
    points_list = [None] * points_amount

    for i in range(points_amount):
        points_list[i] = Point(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))

    # Create the voxel tree
    print("\nBuilding the VoxelTreePointCloud...")
    voxel_tree = VoxelTreePointCloud(points_list)

    # Test searching for points
    test_point = points_list[randint(0, len(points_list) - 1)]  # Get a random point
    result = voxel_tree.search_voxel((test_point.x, test_point.y, test_point.z))

    if result:
        print(f"Point found in voxel with bounds: {result}")
    else:
        print("Point not found in any voxel.")

    # Test a point outside the range
    out_of_bounds_point = Point(2, 2, 2)
    print(f"\nSearching for a point outside the range: {out_of_bounds_point}...")
    result = voxel_tree.search_voxel((out_of_bounds_point.x, out_of_bounds_point.y, out_of_bounds_point.z))

    if result:
        print(f"Point found in voxel with bounds: {result}")
    else:
        print("Point not found in any voxel.")

    print("\nTesting completed.")

if __name__ == '__main__':
    main()
