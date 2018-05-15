SHOW_HIDDEN = False
lowest_similarity_tolerance = 0.8

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

def getObject(window_struct,object_struct):
    ret = None
    exact_search = getObject_exact(window_struct,object_struct)
    if exact_search == None:
        similar_search = getObject_similar(window_struct,object_struct)
        ret = similar_search
    else:
        ret = exact_search
    result = None
    if isinstance(ret,list):
        if ret[0] == None:
            result = ret[1]['return']
        else:
            result = ret[0]
    return result

def getObject_exact(window_struct,object_struct):
    data = getObjectList(window_struct['name'])
    ret = None
    similarIndex = 0
    similarObject = None
    for each in data:
        if each[0]['name'] == "":
            continue
        elif each[0]['name'] == object_struct['name']:
            if each[0]['role'] == object_struct['role']:
                ret = each
    return ret
    

def getObject_similar(window_struct,object_struct):
    data = getObjectList(window_struct['name'])
    ret = None
    similarIndex = 0
    similarObject = None
    for each in data:
        if each[0]['name'] == "":
            continue
        else:
            if similar(object_struct['name'],each[0]['name']) > lowest_similarity_tolerance:
                if similar(object_struct['name'],each[0]['name']) > similarIndex:
                    if object_struct['role'] == "unknown":
                        similarIndex = similar(object_struct['name'],each[0]['name'])
                        similarObject = each[0]
                    else:
                        if object_struct['role'] == each[0]['role']:
                            similarIndex = similar(object_struct['name'],each[0]['name'])
                            similarObject = each[0]
                    
    if ret == None:
        ret = [None,{'return':similarObject,'similarity':similarIndex}]
    return ret
    
def similar(a, b):
    return jellyfish.jaro_distance(unicode(a,"utf-8"),unicode(b,"utf-8"))

def grab_focus(windowObj):

    windowName = windowObj['name']
    try:
        windowName = getWindow(windowName)['name']
    except TypeError:
        return False
    try:
        windowlist = subprocess.check_output(['wmctrl','-l'])
        windowID = -1
        for each in windowlist.split("\n"):
            if each.find(windowName) != -1:
                windowID = each.split(" ")[0]
                break
        if windowID != -1:
            os.system("wmctrl -i -a {}".format(windowID))
            time.sleep(1)
    except:
        raise OSError ("Linux program wmctrl is missing. Please install wmctrl.")

def getActiveWindow():
    try:
        # get active window ID
        windowID = subprocess.check_output(['xprop','-root','_NET_ACTIVE_WINDOW']).split(" ")[-1].split("\n")[0]
    except:
        windowID = None
    if windowID == None:
        raise OSError("linux program xprop is required.")

    windowID_int = int(windowID,16)

    ret = {}
    #get window name from window ID
    windowlist = subprocess.check_output(['wmctrl','-l'])
    for each in windowlist.split("\n"):
        cur_windowID = each.split(" ")[0]
        cur_windowID = cur_windowID.replace("0x0","0x")
        if (windowID == cur_windowID):
            regex = r"0x[\d?]*[\w*?]*\s*\d\s*\w*-?\/?\w*\s(.*)"
            ret['name'] = re.findall(regex,each)[0]
            ret['windowID'] = windowID.replace("0x","0x0")
    return ret

def getObjectRect(handle):
    rect = {"x":[-1,-1],"y":[-1,-1]}
    try :
        size = handle.queryComponent().getSize()
        pos = handle.queryComponent().getPosition(pyatspi.DESKTOP_COORDS)
        min_x = pos[0]
        max_x = pos[0] + size[0]
        min_y = pos[1]
        max_y = pos[1] + size[1]
        rect = {"x":[min_x,max_x],"y":[min_y,max_y]}
    except:
        pass
    return rect


def getObjectState(handle):
    return handle.getState().getStates()

def checkObjectState(handle,state_to_check):
    states = getObjectState(handle)
    ret = False
    for each in states:
        if each == state_to_check:
            ret = True
    return ret