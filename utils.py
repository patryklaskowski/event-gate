import numpy as np
import cv2


def imshow(window_name: str, img: np.ndarray) -> None:
    cv2.imshow(window_name, img)
    cv2.waitKey(1)


def clean_up() -> None:
    cv2.destroyAllWindows()


def create_window(window_name: str) -> None:
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)


def create_trackbars(trackbars_settings) -> None:
    for settings in trackbars_settings:
        cv2.createTrackbar(*settings)


def create_image_2d(width: int, height: int) -> np.ndarray:
    return np.zeros(shape=(height, width), dtype=np.uint8) + 255


def draw_size(img: np.ndarray, inplace=True) -> np.ndarray:
    if not inplace:
        img = img.copy()
    width, height, *_ = img.shape
    pos_x = int(0 + width * 0.02)
    pos_y = int(0 + height * 0.02)

    cv2.putText(img, f'({width}x{height})', (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    return img


def draw_params(img: np.ndarray, line, inplace=True) -> np.ndarray:
    if not inplace:
        img = img.copy()
    width, height, *_ = img.shape
    pos_x = int(0 + width * 0.02)
    pos_y = int(0 + height * 0.04)

    cv2.putText(img, str(line), (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    return img


def draw_line(img: np.ndarray, point_a: tuple[int, int], point_b: tuple[int, int], inplace=False) -> np.ndarray:
    if not inplace:
        img = img.copy()
    img = img.copy()
    cv2.line(img, point_a, point_b, (0, 0, 0), thickness=5)

    return img


def draw_point(img: np.ndarray, point: tuple[int, int], inplace=False, draw_text=True) -> np.ndarray:
    if not inplace:
        img = img.copy()
    x, y = point
    cv2.circle(img, (x, y), 5, (0, 0, 0), -1)
    margin = 5
    if draw_text:
        cv2.putText(img, f'({x}, {y})', (x+margin, y-margin), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)

    return img


def draw_grid(img: np.ndarray, func=None, n=25, inplace=False, draw_text=False):
    if not inplace:
        img = img.copy()

    height, width, *_ = img.shape

    x_grid = np.linspace(0, width-1, n, dtype=int)
    y_grid = np.linspace(0, height-1, n, dtype=int)

    xx, yy = np.meshgrid(x_grid, y_grid)

    for x, y in np.dstack((xx, yy)).reshape(-1, 2):
        if callable(func) and func((x, y)):
            img = draw_point(img, (x, y), draw_text=draw_text, inplace=inplace)
        elif func is None:
            img = draw_point(img, (x, y), draw_text=draw_text, inplace=inplace)

    return img