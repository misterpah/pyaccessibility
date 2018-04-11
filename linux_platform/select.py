def comboboxListOptions(window_struct, object_struct,handle=None):
    if handle == None:
        result = getObject(window_struct,object_struct)
        handle =  result['handle']
    list_options=[]
    if handle.getChildCount() > 0:
        for childlvl_1 in range(0,handle.getChildCount()):
            cur_handle_childlvl_1 = handle.getChildAtIndex(childlvl_1)
            for childlvl_2 in range(0,cur_handle_childlvl_1.getChildCount()):
                cur_handle_childlvl_2 = cur_handle_childlvl_1.getChildAtIndex(childlvl_2)
                list_options.append(cur_handle_childlvl_2.name)
    return list_options

def comboboxGetSelected(window_struct, object_struct,handle=None):
    if handle == None:
        result = getObject(window_struct,object_struct)
        handle =  result['handle']
    list_options=[]
    return handle.name
