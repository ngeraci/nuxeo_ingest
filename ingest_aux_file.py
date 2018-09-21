#!/usr/bin/python3
"""Bulk loading auxiliary (extrafile) objects to Nuxeo.

"""
import os
import sys
import logging
import datetime
import argparse
import subprocess
from local_utils import get_file_paths

def main(args=None):
    """Main loop, parse command line argument.

    """
    parser = argparse.ArgumentParser(
        description='''bulk-upload simple objects to Nuxeo.''')
    parser.add_argument(
        "nuxeo_dir", nargs=1, help='''path to target directory in Nuxeo.
                                      be sure to enclose it in quotation
                                      marks if it contains whitespace.

                                      Example: "/asset-library/UCR/University Archives/Highlander"''')
    parser.add_argument(
        "local_directory", nargs=1, help='''path to local directory containing the files you
                                            want to upload.''')
    parser.add_argument(
        "main_type", nargs=1, help='''file extension for main files. Example: jpg''')

    parser.add_argument(
        "aux_type", nargs=1, help='''file extension for auxiliary/extra files. Example: tif''')


    # print help if no args given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # parse
    if args is None:
        args = parser.parse_args()

    # TODO: make logfile name more granular to allow logging simultaneous processes
    logfile = "nuxeo-aux-ingest_" + datetime.date.today().isoformat() + ".log"
    logging.basicConfig(filename=logfile, level=logging.INFO)

    nuxeo_dir = args.nuxeo_dir[0]
    local_directory = args.local_directory[0]
    aux_paths = get_file_paths(local_directory, args.aux_type[0].strip())

    for aux in aux_paths:
        logging.info(nx_upload(aux, main_path(aux, "jpg"), local_directory, nuxeo_dir))
        break

def main_path(aux_file, main_ext):
    """takes path to an aux file and the extension of its main file.
    returns main file path

    Example:
    >>> aux_to_main_path("box_016/curivsc_146_016_1583-a.tif", "jpg")
    'box_016/curivsc_146_016_1583-a.jpg'
    """
    aux_path = ".".join([os.path.splitext(aux_file)[0], main_ext])

    return aux_path

def extrafile(aux_file, main_file, local_directory, nuxeo_dir):
    """nx extrafile command. return stdout as string

    """
    source_file = os.path.join(local_directory, aux_file)
    destination_doc = "/".join([nuxeo_dir, main_file])

    upload = subprocess.run(["nx", "extrafile", source_file, destination_doc],
                             stdout=subprocess.PIPE).stdout.decode("utf-8")

    return upload


def nx_upload(aux_file, main_file, local_directory, nuxeo_dir):
    """Upload single file. Retry up to three times if 500 error.

    """
    attempts = 0
    while attempts <= 3:
        upload = extrafile(aux_file, main_file, local_directory, nuxeo_dir)
        attempts += 1
        if file_status(upload) == 500:
            upload = extrafile(aux_file, main_file, local_directory, nuxeo_dir)
        else:
            break

    return upload

def file_status(output):
    """ Parse stdout to get upload status.
    """
    status_code = int(output.split("\n", 1)[1][145:156].split(": ")[1])

    return status_code

if __name__ == "__main__":
    main()
