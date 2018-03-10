import time


def _mouseEvent(posx, posy, typeString):
    pyatspi.Registry.generateMouseEvent(posx, posy, typeString)
    time.sleep(0.5)


def mouseMove(window, object):
    handle = getObject(window, object)['handle']
    size = handle.queryComponent().getSize()
    pos = handle.queryComponent().getPosition(pyatspi.DESKTOP_COORDS)
    try:
        _mouseEvent(pos[0] + size[0] / 2, pos[1] + size[1] / 2, 'abs')
        return True
    except BaseException:
        return False


def mouseClick(window, object):
    handle = getObject(window, object)['handle']
    size = handle.queryComponent().getSize()
    pos = handle.queryComponent().getPosition(pyatspi.DESKTOP_COORDS)
    try:
        _mouseEvent(
            pos[0] + size[0] / 2,
            pos[1] + size[1] / 2,
            pyatspi.MOUSE_B1P)
        _mouseEvent(
            pos[0] + size[0] / 2,
            pos[1] + size[1] / 2,
            pyatspi.MOUSE_B1R)
        return True
    except BaseException:
        return False
