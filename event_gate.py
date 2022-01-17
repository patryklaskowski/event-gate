import math


class OutOfRangeError(Exception):
    """Value exceeds its range"""


class EquationError(Exception):
    """Function equation cannot be evaluated"""


class EventGate:
    """
    Event gate is line segment determined by two points on the Cartesian plane

    Points are calculated based on central point, line width, and alpha value.
    Where alpha is a tilt angle to x-axis.
    """

    ALPHA_LOWER_BOUND = 0
    ALPHA_UPPER_BOUND = 89
    _is_initialized = False

    def __init__(self, x: int, y: int, width: int, alpha: int = 0):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.alpha = int(alpha)
        self._slope, self._bias = self.get_line_coefficients()
        self._is_initialized = True

    def __str__(self):
        return f'<x={self.x}, y={self.y}, width={self.width}, alpha={self.alpha}>'

    def get_edge_points_coordinates(self) -> tuple[int, int, int, int]:
        """
        Calc line start and end coordinates based on right triangle trigonometry.

            hypotenuse = 1/2 * width
            adjacent = cos alpha * hypotenuse
            opposite = sin alpha * hypotenuse

        :returns ((a_x, a_y), (b_x, b_y)) Where a and b are edge points
        """
        alpha_radians = math.radians(self.alpha)
        hypotenuse = 0.5 * self.width
        adjacent = math.cos(alpha_radians) * hypotenuse
        opposite = math.sin(alpha_radians) * hypotenuse

        a_x = int(self.x - adjacent)
        a_y = int(self.y - opposite)

        b_x = int(self.x + adjacent)
        b_y = int(self.y + opposite)

        return (a_x, a_y), (b_x, b_y)

    def set_edge_points_coordinates(self, *args, **kwargs) -> None:
        """Symmetric method"""
        raise NotImplementedError('Edge points setter not implemented.')

    def get_line_coefficients(self) -> tuple[float, float]:
        """
        Find the slope and bias for equation of a line given two points.

        :returns (slope, bias)
        """
        (a_x, a_y), (b_x, b_y) = self.get_edge_points_coordinates()

        if a_x == b_x:
            raise EquationError(f'Equation of vertical line. This is not a function (x=`{a_x}`).')

        change_in_y = (a_y - b_y)
        change_in_x = (a_x - b_x)
        slope = change_in_y / change_in_x
        bias = a_y - slope * a_x

        return round(slope, 2), round(bias, 2)

    def set_line_coefficients(self, *args, **kwargs) -> None:
        """Symmetric method"""
        raise NotImplementedError('Line coefficients setter not implemented.')

    def __setattr__(self, name: str, value: object) -> None:
        """
        Used to automatically update line coefficients (slope and bias) when some attributes are changed.

        * Other way would be to use explicit setters with update_coefs flag.
        """
        if self._is_initialized and name in ['x', 'y', 'width', 'alpha']:
            self._slope, self._bias = self.get_line_coefficients()
        super().__setattr__(name, value)

    def is_point_above_the_line(self, a: tuple[int, int]) -> bool:  # possibly to be implemented using __gt__()
        """
        ! Valid for OpenCv axis system where yaxis increases downwards !

        Determine is point strictly above the line.
        Returns false if point lays on the line or below
        """
        a_x, a_y = a
        return a_y < self._slope * a_x + self._bias

    @property
    def alpha(self) -> None:
        """
        Alpha getter

        :returns alpha
        """
        return self._alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        """
        Alpha setter forces constraints

        :parameter value
        """
        value = int(value)
        if not self.ALPHA_LOWER_BOUND <= value <= self.ALPHA_UPPER_BOUND:
            raise OutOfRangeError(f'Alpha value `{value}` must be in range '
                                  f'[{self.ALPHA_LOWER_BOUND}, {self.ALPHA_UPPER_BOUND}]!')
        self._alpha = value

    def get_center(self) -> tuple[int, int]:
        """
        Center point getter

        :returns (x, y)
        """
        return self.x, self.y

    def set_center(self, x: int, y: int) -> None:
        """
        Center point setter

        :parameter x
        :parameter y
        """
        self.x = int(x)
        self.y = int(y)
