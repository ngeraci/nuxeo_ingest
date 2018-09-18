import os

def get_file_paths(directory, file_types):
    """Takes path to directory and list of file extensions.
    Returns (recursive) list of file paths with those extensions in that directory.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.startswith("."):
                extension = extension[1:]
            if extension in file_types:
                filepath = os.path.join(root, file)
                # remove first segment of path
                filepath = splitall(filepath)
                filepath.pop(0)
                # append to list
                file_paths.append(os.path.join(*filepath))

    return file_paths


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
