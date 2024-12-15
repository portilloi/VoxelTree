from math import ceil


class VoxelTreeNode:
    # Instance Variables
    __vertices = None
    __left = None
    __right = None

    # Constructor
    def __init__(self, vertices):
        self.set_vertices(vertices)
        self.set_left(None)
        self.set_right(None)

    # Getters
    def get_vertices(self):
        return self.__vertices

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    # Setters
    def set_vertices(self, vertices):
        self.__vertices = vertices

    def set_left(self, left):
        self.__left = left

    def set_right(self, right):
        self.__right = right


class VoxelTreePointCloud:
    # Instance Variables
    __root = None
    __points = None
    __voxel_side_length = -1
    __num_voxels = -1

    # Constructor
    def __init__(self, points, points_cube_side=2):
        self.set_points(points)
        self.set_voxel_side_length(
            (.1 * 2) ** .5)  # side length for a cube that fits exactly within the radius of the circle
        self.set_num_voxels(ceil(points_cube_side / self.get_voxel_side_length()))
        self.set_root(self.__build_tree(self.get_points()))

    # Helpers
    # Builds voxel tree
    def __build_tree(self, points):
        if len(points) == 0:  # Base case: No points
            return None

        # Hard-coded bounds
        min_x, min_y, min_z = (-1, -1, -1)
        max_x, max_y, max_z = (1, 1, 1)

        return self.__create_voxels(min_x, min_y, min_z, max_x, max_y, max_z, self.get_num_voxels())

    # Divide spaces based on the voxel count
    def __create_voxels(self, min_x, min_y, min_z, max_x, max_y, max_z, num_voxels):
        if num_voxels <= 1:  # Base case
            # Create a leaf node for the voxel
            vertices = self.__get_voxel_bounds((min_x, min_y, min_z), (max_x, max_y, max_z))
            return VoxelTreeNode(vertices=vertices)

        # Calculate the midpoints for splitting the voxel
        midpoint_x = min_x + self.get_voxel_side_length() * (num_voxels // 2)
        midpoint_y = min_y + self.get_voxel_side_length() * (num_voxels // 2)
        midpoint_z = min_z + self.get_voxel_side_length() * (num_voxels // 2)

        # Create children
        left_child = self.__create_voxels(
            min_x, min_y, min_z, midpoint_x, midpoint_y, midpoint_z, num_voxels // 2
        )
        right_child = self.__create_voxels(
            midpoint_x, midpoint_y, midpoint_z, max_x, max_y, max_z, num_voxels - num_voxels // 2
        )

        # Create a parent node and assign its children
        parent_node = VoxelTreeNode(vertices=None)
        parent_node.set_left(left_child)
        parent_node.set_right(right_child)

        return parent_node

    # Search for which voxel a point lies in
    def search_voxel(self, point):
        current_node = self.get_root()
        while current_node:
            # Return vertices when a leaf node is reached
            if current_node.get_left() is None and current_node.get_right() is None:
                voxel_bounds = current_node.get_vertices()
                if self.__point_in_voxel(point, voxel_bounds):
                    return voxel_bounds
                else:
                    return None

            # Decide which child to search
            voxel_bounds = self.__get_voxel_bounds((-1, -1, -1), (1, 1, 1))
            midpoint_x = (voxel_bounds[0][0] + voxel_bounds[6][0]) / 2
            midpoint_y = (voxel_bounds[0][1] + voxel_bounds[6][1]) / 2
            midpoint_z = (voxel_bounds[0][2] + voxel_bounds[6][2]) / 2

            if point[0] <= midpoint_x and point[1] <= midpoint_y and point[2] <= midpoint_z:
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()

        return None  # Point was not found in any voxel

    # Checks if a point is inside a voxel
    def __point_in_voxel(self, point, voxel_bounds):
        x, y, z = point
        min_x, min_y, min_z = voxel_bounds[0]
        max_x, max_y, max_z = voxel_bounds[6]

        return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z

    # Returns the vertices of a voxel given opposite vertices
    def __get_voxel_bounds(self, vertex_1, vertex_2):
        x1, y1, z1 = vertex_1
        x2, y2, z2 = vertex_2
        vertices = [(x1, y1, z1),
                    (x1, y1, z2),
                    (x1, y2, z1),
                    (x1, y2, z2),
                    (x2, y1, z1),
                    (x2, y1, z2),
                    (x2, y2, z1),
                    (x2, y2, z2)
                    ]
        return vertices

    # Getters
    def get_root(self):
        return self.__root

    def get_points(self):
        return self.__points

    # Set side length in units
    def get_voxel_side_length(self):
        return self.__voxel_side_length

    def get_num_voxels(self):
        return self.__num_voxels

    # Setters
    def set_root(self, root):
        self.__root = root

    def set_points(self, points):
        self.__points = points

    def set_voxel_side_length(self, voxel_side_length):
        self.__voxel_side_length = voxel_side_length

    def set_num_voxels(self, num_voxels):
        self.__num_voxels = num_voxels
