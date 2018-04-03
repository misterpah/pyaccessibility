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
    pyatspi.Registry._set_registry("None")
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
    similarityIndex = 0
    similarityObject = None
    for each in data:
        if each['name'] == "":
            continue
        else:
            cur_name = each['name'].replace("*","")
            if similar(windowName,cur_name) > 0.5:
                if similar(windowName,cur_name) > similarityIndex:
                    similarityIndex = similar(windowName,cur_name)
                    similarityObject = each
    if ret == None:
        ret = similarityObject
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

def getObject(windowName,objectName):
    ret = None
    exact_search = getObject_exact(windowName,objectName)
    if exact_search == None:
        similar_search = getObject_similar(windowName,objectName)
        ret = similar_search
    else:
        ret = exact_search
    return ret

def getObject_exact(windowName,objectName):
    data = getObjectList(windowName)
    ret = None
    similarIndex = 0
    similarObject = None
    for each in data:
        if each[0]['name'] == "":
            continue
        elif each[0]['name'] == objectName:
            ret = each
    return ret
    

def getObject_similar(windowName, objectName):
    data = getObjectList(windowName)
    ret = None
    similarIndex = 0
    similarObject = None
    for each in data:
        if each[0]['name'] == "":
            continue
        else:
            if similar(objectName,each[0]['name']) > 0.5:
                if similar(objectName,each[0]['name']) > similarIndex:
                    similarIndex = similar(objectName,each[0]['name'])
                    similarObject = each[0]
    if ret == None:
        ret = [None,{'return':similarObject,'similarity':similarIndex}]
    return ret
    
def similar(a, b):
    return jellyfish.jaro_distance(unicode(a,"utf-8"),unicode(b,"utf-8"))

def grab_focus(windowName):
    windowName = getWindow(windowName)['name']
    try:
        windowlist = subprocess.check_output(['wmctrl','-l'])
        windowID = -1
        for each in windowlist.split("\n"):
            if each.find(windowName) != -1:
                windowID = each.split(" ")[0]
                break
        if windowID != -1:
            os.system("wmctrl -i -a {}".format(windowID))
    except:
        raise OSError ("Linux program wmctrl is missing. Please install wmctrl.")
