# nuxeo ingest scripts

scripts for ingesting files into Nuxeo at UCR Library, using [nxcli](https://github.com/ucldc/nxcli)

__make_directory_structure.py__: sets up the directoy structure for a Nuxeo collection, matching local directory structure.
_Example_:
'''python make_directory_structure.py "/asset-library/UCR/University Archives/Yearbook"''' would create blank folders in Nuxeo at "/asset-library/UCR/University Archives/Yearbook" that match the folders in your current local directory.