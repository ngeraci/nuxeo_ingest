#!/usr/bin/python3
"""Build out folder structure for a Nuxeo collection, based on local folder structure.

"""
import os
import sys
import subprocess
import argparse
from local_utils import splitall

def main(args=None):
    """Main loop, parse command line argument.

    """
    parser = argparse.ArgumentParser(
        description='''build folder structure for a Nuxeo collection,
                       based on local folder structure.''')
    parser.add_argument(
        "nuxeo_path", nargs=1, help='''path to parent folder in Nuxeo.
                                      be sure to enclose it in quotation
                                      marks if it contains whitespace.

                                      Example: "/asset-library/UCR/University Archives/Highlander"''')
    parser.add_argument(
        "local_directory", nargs=1, help='''path to local directory whose structure
                                            you want to replicate. to use your current
                                            working directory, use "."''')

    # print help if no args given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # parse
    if args is None:
        args = parser.parse_args()

    nuxeo_path = args.nuxeo_path[0]
    folders = get_recursive_folders(args.local_directory[0])
    make_folder_structure(nuxeo_path, folders)
    verify(nuxeo_path, folders)

def get_recursive_folders(local_directory):
    """Returns list of all folders within current folder.

    """
    folders = []
    for path, dirs, files in os.walk(local_directory):
        # exclude hidden directories
        dirs[:] = [d for d in dirs if not d[0] == '.']
        # exclude root directory
        if path != local_directory:
            # remove first segment of path & append to list
            path = splitall(path)
            path.pop(0)
            folders.append(os.path.join(*path))

    return folders

def make_folder_structure(nuxeo_path, local_folders):
    """Run the command that makes the folders.

    """
    for folder in local_folders:
        subprocess.run(["nx", "mkdoc", "-t", "Organization", "/".join([nuxeo_path, folder])],
                       check=True)

def verify(nuxeo_path, local_folders):
    """Make sure the number of folders locally and on Nuxeo match.

    """
    nxls = subprocess.run(["nxls", nuxeo_path, "--recursive-folders"],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    nx_list = list(filter(None, nxls.split("\n")))

    warning = """
    Warning: possible missing folders. You may want to re-run this script.

    Local folders: {}
    Nuxeo folders: {}
    """.format(len(local_folders), len(nx_list))

    if len(nx_list) != len(local_folders):
        print(warning)

if __name__ == "__main__":
    main()
