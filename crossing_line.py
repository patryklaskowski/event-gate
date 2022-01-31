from sklearn.linear_model import LinearRegression
import numpy as np
import cv2
from itertools import zip_longest
import random
from collections import deque

import utils


class IntersectSegmentsAlgorithm:
    """
    @Author: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    """

    @staticmethod
    def _are_points_counterclockwise_order(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> bool:
        """
        Solution involves determining if three points are listed in a counterclockwise order.
        So say you have three points A, B and C.
        If the slope of the line AB is less than the slope of the line AC then
         the three points are listed in a counterclockwise order.
        """
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    @classmethod
    def are_segments_intercept(cls, a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int])\
            -> bool:
        """
        are_segments_intersect?

        Think of two line segments AB, and CD.
        These intersect if and only if points A and B are separated by segment CD and
         points C and D are separated by segment AB.
        If points A and B are separated by segment CD then
         ACD and BCD should have opposite orientation meaning either ACD or BCD is counterclockwise but not both.
        """
        return cls._are_points_counterclockwise_order(a, c, d) != \
               cls._are_points_counterclockwise_order(b, c, d) and \
               cls._are_points_counterclockwise_order(a, b, c) != \
               cls._are_points_counterclockwise_order(a, b, d)


class Shadow:

    def __init__(self, points: list[tuple, ...], max_len: int = 10):
        self.points = deque(points, max_len)

    def __str__(self):
        values = '->'.join([f'({x}, {y})' for x, y in self.points])
        return f'<Shadow {values}>'

    def get_edge_points(self) -> tuple[tuple, tuple]:
        """
        * Assuming that points are ordered by time

        :returns (start, end)
        """
        if len(self.points) == 0:
            raise IndexError('Points collection is empty!')
        return self.points[0], self.points[-1]

    def add_point(self, point: tuple[int, int]):
        """
        Add new point
        """
        self.points.append(point)


def generate_random_points_for_regression(height: int, width: int, n: int = 10, noise: float = 0.2) \
        -> tuple[np.array, np.array]:
    """
    A

    :returns x, y
    """
    margin = 0.3
    random.seed(13)

    # Generate Initial Values
    x = np.linspace(0 + width * margin, width - width * margin, n, dtype=int)
    y = np.linspace(0 + height * margin, height - height * margin, n, dtype=int)

    # Add Noise
    random.shuffle(x)
    random.shuffle(y)

    x = np.array([val + random.randint(0, int(val * noise)) if random.choice([0, 1]) else
                  val - random.randint(0, int(val * noise))
                  for val in x])
    y = np.array([val + random.randint(0, int(val * noise)) if random.choice([0, 1]) else
                  val - random.randint(0, int(val * noise)) for val in y])

    return x, y


def draw_points(img: np.ndarray, points: list[tuple], inplace: bool = False, draw_text: bool = False) -> np.ndarray:
    if not inplace:
        img = img.copy()
    for point in points:
        img = utils.draw_point(img, point, inplace, draw_text)

    return img


def draw_gridlines(img, every_n=100, inplace=False):
    if not inplace:
        img = img.copy()

    height, width, *_ = img.shape

    x_ticks = np.linspace(0, width, int(width / every_n), dtype=int)
    y_ticks = np.linspace(0, height, int(height / every_n), dtype=int)

    for x_tick, y_tick in zip_longest(x_ticks, y_ticks, fillvalue=False):
        x_tick and cv2.line(img, (x_tick, 0), (x_tick, height), (0, 0, 0), thickness=1)
        y_tick and cv2.line(img, (0, y_tick), (width, y_tick), (0, 0, 0), thickness=1)

    return img


def get_edge_points(x_values: list, y_values: list) -> tuple[tuple, tuple]:
    a_x, a_y = min(x_values), min(y_values)
    b_x, b_y = max(x_values), max(y_values)

    return (a_x, a_y), (b_x, b_y)


if __name__ == '__main__':

    IMG_WIDTH = 1000
    IMG_HEIGHT = 500
    WINDOW_NAME = 'Line Segment Intersection'
    N = 10
    NOISE = 0.1

    X_VALUES, Y_VALUES = generate_random_points_for_regression(IMG_HEIGHT, IMG_WIDTH, n=N, noise=NOISE)
    A, B = get_edge_points(X_VALUES, Y_VALUES)

    are_segments_intersect = IntersectSegmentsAlgorithm.are_segments_intercept

    reg = LinearRegression()
    reg.fit(X_VALUES.reshape(-1, 1), Y_VALUES)
    print(reg.coef_, reg.intercept_)
    x = 4
    HOLDER = np.array([[x]])
    y_hat = reg.predict(HOLDER)
    print(f'Val: {y_hat} for id: {id(HOLDER)}')

    HOLDER[0][0] = 100
    y_hat = reg.predict(HOLDER)
    print(f'Val: {y_hat} for id: {id(HOLDER)}')

    try:
        while True:
            image = utils.create_image_2d(IMG_WIDTH, IMG_HEIGHT)

            image = utils.draw_size(image, inplace=True)
            image = draw_points(image, zip(X_VALUES, Y_VALUES), inplace=True)
            image = draw_gridlines(image, every_n=50, inplace=True)
            image = draw_points(image, [A, B], inplace=True, draw_text=True)

            utils.imshow(WINDOW_NAME, image)
    finally:
        utils.clean_up()
