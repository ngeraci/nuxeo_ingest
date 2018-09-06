#!/usr/bin/python3
"""Bulk loading simple objects to Nuxeo.

"""
import os
import sys
import logging
import datetime
import argparse
import subprocess
from local_utils import splitall

def main(args=None):
    """Main loop, parse command line argument.

    """
    parser = argparse.ArgumentParser(
        description='''bulk-upload simple objects to Nuxeo.''')
    parser.add_argument(
        "nuxeo_path", nargs=1, help='''path to target folder in Nuxeo.
                                      be sure to enclose it in quotation
                                      marks if it contains whitespace.

                                      Example: "/asset-library/UCR/University Archives/Highlander"''')
    parser.add_argument(
        "local_directory", nargs=1, help='''path to local directory containing the files you
                                            want to upload. if no value is given,
                                            it defaults to your current working directory.''')
    parser.add_argument(
        "file_type", nargs=1, help='''one or more types of files (extensions) you want to upload,
                                      separated by commas. Example: pdf,tif,mp4''')

    # print help if no args given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # parse
    if args is None:
        args = parser.parse_args()

    # TODO: make filename more granular (collection name?) to allow logging simultaneous processes
    logfile = "nuxeo-ingest_" + datetime.date.today().isoformat() + ".log"
    logging.basicConfig(filename=logfile, level=logging.INFO)

    nuxeo_path = args.nuxeo_path[0]
    local_directory = args.local_directory[0]
    file_types = [f.strip() for f in args.file_type[0].split(",")]
    local_paths = get_file_paths(local_directory, file_types)

    for file in local_paths:
        logging.info(nx_upload(file, local_directory, nuxeo_path))

    verify(nuxeo_path, local_paths)

def get_file_paths(local_directory, file_types):
    """Return list of file paths in local directory.

    """
    local_file_paths = []
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.startswith("."):
                extension = extension[1:]
            if extension in file_types:
                filepath = os.path.join(root, file)
                # remove first segment of path & append to list
                filepath = splitall(filepath)
                filepath.pop(0)
                local_file_paths.append(os.path.join(*filepath))

    return local_file_paths

def nx_upload(file, local_directory, nuxeo_path):
    """Upload single file. Retry up to three times if error.

    """
    attempts = 0
    while attempts <= 3:
        upload = upfile(file, local_directory, nuxeo_path)
        attempts += 1
        if file_status(upload) == 'error':
            upload = upfile(file, local_directory, nuxeo_path)
        else:
            break

    return upload

def upfile(file, local_directory, nuxeo_path):
    """ nx upfile command. return stdout as string

    """
    upload = subprocess.run(["nx", "upfile", "-doc", "/".join([nuxeo_path, file]),
                             "".join([local_directory, file])],
                            stdout=subprocess.PIPE).stdout.decode("utf-8")

    return upload

def file_status(output):
    """ Parse stdout to get upload status.
    """
    firstline = output.split("\n", 1)[0]
    if firstline.startswith("{ Error:"):
        # TODO: figure out specific error types
        status = "error"
    else:
        status = "ok"

    return status

def verify(nuxeo_path, local_paths):
    """Make sure the number of files locally and on Nuxeo match.

    """
    nxls = subprocess.run(["nxls", nuxeo_path, "--recursive-objects"],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    nx_list = list(filter(None, nxls.split("\n")))

    print("Nuxeo files:", len(nx_list))
    print("Local files:", len(local_paths))


if __name__ == "__main__":
    main()
