import time


def _mouseEvent(posx, posy, typeString):
    pyatspi.Registry.generateMouseEvent(posx, posy, typeString)
    time.sleep(0.5)

def mouseMove(window, object,handle=None):
    grab_focus(window)
    if handle == None:
        result = getObject(window, object)
    else:
        result = getObject(window, object)
        result['handle'] = handle
    if result['handle'].get_child_count() > 0:
        for each in range(0,result['handle'].get_child_count()):
            if result['handle'].getChildAtIndex(each).name == result['name'] :
                result['handle'] = result['handle'].getChildAtIndex(each)
                break
    size = result['handle'].queryComponent().getSize()
    pos = result['handle'].queryComponent().getPosition(pyatspi.DESKTOP_COORDS)
    try:
        _mouseEvent(pos[0] + size[0] / 2, pos[1] + size[1] / 2, 'abs')
        return True
    except BaseException:
        return False


def mouseClick(window, object,handle=None):
    grab_focus(window)
    if handle == None:
        result = getObject(window, object)
        if isinstance(result,list):
            handle = result[1]['return']['handle']
        else:
            handle = result['handle']
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
