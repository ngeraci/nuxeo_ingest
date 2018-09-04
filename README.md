# nuxeo ingest scripts

scripts for ingesting files into Nuxeo at UCR Library, using [nxcli](https://github.com/ucldc/nxcli)

## make_directory_structure.py
sets up the directory structure for a Nuxeo collection, matching a local directory structure.

__Example__:
```python make_directory_structure.py "/asset-library/UCR/University Archives/Yearbook"```

This example would create blank folders in Nuxeo at "/asset-library/UCR/University Archives/Yearbook" that match the folders in the local directory where you're running the script.