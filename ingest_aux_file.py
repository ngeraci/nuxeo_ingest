import os

def aux_path(main_file, aux_ext):
    """takes path to a main file and the extension of its aux file.
    returns aux file path

    Example:
    >>> aux_path("box_016/curivsc_146_016_1583-a.tif", "jpg")
    'box_016/curivsc_146_016_1583-a.jpg'
    """
    aux_path = ".".join([os.path.splitext(main_file)[0], aux_ext])

    return aux_path


def extrafile(main_file, aux_file, local_directory, nuxeo_path):
    """nx extrafile command. return stdout as string

    """
    source_file = os.path.join(local_directory, aux_file)
    destination_doc = "/".join([nuxeo_path, main_file])

    upload = subprocess.run(["nx", "extrafile", source_file, destination_doc])

    return upload
