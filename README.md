# nuxeo ingest scripts

scripts for ingesting files into Nuxeo at UCR Library, using [nxcli](https://github.com/ucldc/nxcli)

## make_directory_structure.py
using [nx mkdoc](https://github.com/ucldc/nxcli/blob/c25c61bc7a4e5c03fb42c14855fad60586b660b1/arguments.js#L52-L73), sets up the directory structure for a Nuxeo collection, matching a local directory structure.

__Example__:
```python make_directory_structure.py "/asset-library/UCR/University Archives/Yearbook"```

This example would create blank folders in Nuxeo at "/asset-library/UCR/University Archives/Yearbook" that match the folders in the local directory where you're running the script.
