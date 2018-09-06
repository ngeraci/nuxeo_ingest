import os

def splitall(path):
    """ Split apart all parts of path, return list
    Reference:
    https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch04s16.html

    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts