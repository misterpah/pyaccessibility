import pyatspi

SHOW_HIDDEN = False


def standard_name_reference(name, role, handle):
    ret = {}
    ret['name'] = name
    ret['role'] = role
    ret['handle'] = handle
    return ret


def objectIsVisible(handle):
    ret = False
    if handle.getState().contains(pyatspi.STATE_SHOWING):
        ret = True
    if SHOW_HIDDEN:
        ret = True
    return ret


def getDesktop():
    return pyatspi.Registry.getDesktop(0)


def getWindowList():
    ret = []
    for each in getDesktop():
        for i in range(0, each.getChildCount()):
            cur_child = each.getChildAtIndex(i)
            if objectIsVisible(cur_child) is False:
                continue
            ret.append(
                standard_name_reference(
                    cur_child.name,
                    cur_child.getRoleName(),
                    cur_child))
    return ret


def getWindow(windowName):
    data = getWindowList()
    ret = None
    for each in data:
        if each['name'] == "":
            continue    
        if windowName.find(each['name']) != -1:
            ret = each
    return ret


def getObjectList(window):
    handle = getWindow(window)['handle']
    def getChild(handle):
        ret = []
        for i in range(0, handle.getChildCount()):
            cur_child = handle.getChildAtIndex(i)
            if cur_child is None:
                continue
            if objectIsVisible(cur_child) is False:
                continue
            key = standard_name_reference(
                cur_child.name, cur_child.getRoleName(), cur_child)
            ret.append([key, cur_child])
        return ret

    # feed in one seed for recursive search
    ret = []
    children_not_checked = []
    ret += getChild(handle)
    children_not_checked += ret

    # search all object using breadth first algorithm
    loop = True
    while loop:
        if len(children_not_checked) == 0:
            loop = False
            continue
        cur_child = children_not_checked.pop()
        try:
            data = getChild(cur_child[1])
            ret += data
            children_not_checked += data
        except BaseException:
            pass
    return ret


def getObject(windowName, objectName):
    data = getObjectList(windowName)
    ret = None
    for each in data:
        if each[0]['name'] == "":
            continue
        if objectName.find(each[0]['name']) != -1:
            ret = each[0]
        else:
            if similar(each[0]['name'],objectName) > 0.8:
                ret = each[0]
    return ret
    
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
