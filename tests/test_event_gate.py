import unittest
from event_gate import EventGate, OutOfRangeError


class TestEventGate(unittest.TestCase):

    def test_horizontal_line_segment_edge_points_evaluation(self):
        line = EventGate(5, 5, 10, 0)
        (a_x, a_y), (b_x, b_y) = line.get_edge_points_coordinates()
        self.assertEqual((a_x, a_y), (0, 5))
        self.assertEqual((b_x, b_y), (10, 5))

    def test_straight_line_equation_parameters_estimation(self):
        line = EventGate(5, 5, 10, 0)
        slope, bias = line.get_line_coefficients()
        self.assertEqual(slope, 0)
        self.assertEqual(bias, 5)

    def test_alpha_upper_value_constraints(self):
        with self.assertRaises(OutOfRangeError):
            EventGate(5, 5, 10, alpha=90)

        with self.assertRaises(OutOfRangeError):
            EventGate(5, 5, 10, alpha=-1)

    def test_point_above_the_line_detection(self):
        gate = EventGate(500, 250, 200, 0)
        points = (
            (499, 124),
            (249, 249),
            (888, 221),
            (0, 0),
        )
        for point in points:
            self.assertTrue(gate.is_point_above_the_line(point)), f'Error for {point}'

    def test_point_not_above_the_line_detection(self):
        gate = EventGate(500, 250, 200, 0)
        points = (
            (12, 250),
            (249, 550),
            (888, 900),
            (0, 250),
            (0, 251),
        )
        for point in points:
            self.assertFalse(gate.is_point_above_the_line(point)), f'Error for {point}'


if __name__ == '__main__':
    unittest.main(verbosity=2)
