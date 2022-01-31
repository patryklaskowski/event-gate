from event_gate import EventGate
import utils

if __name__ == '__main__':

    IMG_WIDTH = 1000
    IMG_HEIGHT = 500
    WINDOW_NAME = 'DISPLAY'
    N = 10

    class Global:
        DRAW_GRID = True
        DRAW_SHADOW = True
        DRAW_GRIDLINES = False

    line = EventGate(x=500, y=250, width=200, alpha=0)

    TRACKBARS_SETTINGS = (
        ('X', WINDOW_NAME, line.x, IMG_WIDTH, lambda val: setattr(line, 'x', val)),
        ('Y', WINDOW_NAME, line.y, IMG_HEIGHT, lambda val: setattr(line, 'y', val)),
        ('Width', WINDOW_NAME, line.width, max(IMG_WIDTH, IMG_HEIGHT), lambda val: setattr(line, 'width', val)),
        ('Alpha', WINDOW_NAME, line.alpha, line.ALPHA_UPPER_BOUND, lambda val: setattr(line, 'alpha', val)),
        ('Grid', WINDOW_NAME, int(Global.DRAW_GRID), 1, lambda val: setattr(Global, 'DRAW_GRID', bool(val))),
        ('Shadow', WINDOW_NAME, int(Global.DRAW_SHADOW), 1, lambda val: setattr(Global, 'DRAW_SHADOW', bool(val))),
    )

    points = []

    utils.create_window(WINDOW_NAME)
    utils.create_trackbars(TRACKBARS_SETTINGS)
    utils.create_mouse_callback(WINDOW_NAME, utils.handle_points_callback, points)

    try:
        while True:
            image = utils.create_image_2d(IMG_WIDTH, IMG_HEIGHT)

            (a_x, a_y), (b_x, b_y) = line.get_edge_points_coordinates()

            image = utils.draw_point(image, (a_x, a_y), inplace=True)  # A
            image = utils.draw_point(image, (b_x, b_y), inplace=True)  # B
            image = utils.draw_point(image, line.get_center(), inplace=True)  # center

            image = utils.draw_size(image, inplace=True)
            image = utils.draw_line_attributes(image, line, inplace=True)

            if Global.DRAW_GRID:
                image = utils.draw_grid(img=image, func=line.is_point_above_the_line, n=N, inplace=True, draw_text=False)

            if Global.DRAW_SHADOW:
                image = utils.draw_shadow(image, points, inplace=True)

            image = utils.draw_line(image, (a_x, a_y), (b_x, b_y), inplace=True)

            utils.imshow(WINDOW_NAME, image)
    finally:
        utils.clean_up()
