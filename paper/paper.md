---
title: 'InstrumentDB: A scientific database application and companion Python library'
tags:
  - Python
  - Django
  - SQLite
  - Databases
  - Scientific software
authors:
  - name: "Maurizio Tomasi"
    orcid: 0000-0002-1448-6131
    affiliation: "1, 2"
  - name: "Gemma Luzzi"
    orcid: 0000-0000-0000-0000
    affiliation: "3"
  - name: "Fabrizio Fabri"
    orcid: 0000-0000-0000-0000
    affiliation: "3"
affiliations:
  - name: "Department of Physics, University of Milan, Italy"
    index: 1
  - name: "Istituto Nazionale di Fisica Nucleare (INFN), Sezione di Milano"
    index: 2
  - name: "Space Science Data Center, Italian Space Agency"
    index: 3
date: 2025-09-25
bibliography: paper.bib
---

# Summary

InstrumentDB is a Django-based [@django] web application for storing and organizing the specifications and configurations of scientific instruments. It models instruments as a versioned tree of entities (e.g., subsystems and components) with associated quantities (parameters, models, calibration files, etc.). The quantities are versioned, linked to releases, and are always retrievable.

A companion Python package, Libinsdb, provides programmatic access to the InstrumentDB databases, supporting integration with simulation, calibration, and data reduction pipelines. Databases can also be exported by InstrumentDB to a self-contained directory tree, which Libinsdb can treat as a read-only database without a running server, enabling lightweight, offline, and reproducible workflows.

# Statement of need

Modern scientific collaborations require tracking of evolving instrument designs and metadata. Existing solutions (e.g., HDF5, STEP, ad-hoc spreadsheets, and shared folders) lack version tracking and programmatic accessibility. While there are scientific data platforms such as ICAT [@icat], LabKey Server [@labkey], and NOMAD [@nomad], none of them are specifically tailored for the handling of instrument designs, and most importantly, this kind of tool relies exclusively on REST/SOAP access, introducing overhead for pipelines that need to quickly access large parameter sets.

InstrumentDB addresses these issues by:

- Providing a version-controlled data model for entities, quantities, and data files.
- Enabling both web-based and programmatic access (via Libinsdb).
- Supporting an export-to-directory workflow, unique among comparable systems, for offline use, reproducibility, and simple sharing.

This combination makes InstrumentDB particularly suited for medium-sized collaborations, where design metadata must be both tracked historically and easily accessible to automated pipelines.

InstrumentDB is not designed to manage the scientific data produced by the instrument, but rather to capture the structure and evolution of its hardware design.

# Functionality

InstrumentDB organizes information using the following components:

-   **Entities**: Hierarchical components of the instrument (e.g., *accelerator* → *ion source*).
-   **Quantities**: Parameters or files attached to entities (e.g., CAD files and thermal models).
-   **Format specifications**: Text documents describing conventions (e.g., units and reference frames).
-   **Data files**: Uploaded files, automatically versioned; previous versions remain accessible.
-   **Releases**: Tagged snapshots of specific data file versions.

![Sketch of the data model implemented by InstrumentDB for a dummy linear accelerator experiment. Entities (white boxes) and quantities (black boxes) provide a tree-like structure, and data files (gray boxes) are the actual information stored in the database. Releases group data files.\label{fig:data-model}](data-model.svg)

All these objects, except for the format specifications, are shown in \autoref{fig:data-model}.

The system supports three access modes:

1. Web interface (Django application) for browsing.
2. REST API, optionally through Libinsdb, for scripted access and pipeline integration.
3. Exported directory tree and Libinsdb, which is accessed like the REST API but only in read-only mode.

Authentication is provided through Django and controls access to the web application and REST API; local exports have no restrictions.

# Demonstration

A publicly accessible instance is available at[^demo] <https://insdbdemo.fisica.unimi.it/>. It contains a reduced set of instrumental parameters based on a publicly available description of the ESA Planck mission, available in the Planck Legacy Archive[^PLA]. The database was populated using a set of scripts available at <https://github.com/ziotom78/planck_insdb_demo>. These scripts serve as a demonstration of InstrumentDB usage and documentation of the intended workflow for populating the database with entities, quantities, format specifications, and data files. The demo was designed to showcase the following features:

- The population of the database should go through two stages: (1) create the tree of entities and quantities and add format specifications, and (2) upload the actual data files once per each release.
- The versioning of the quantities is done by including a synthetic description of the instrument through the four Planck data releases of 2013 [@planck2013], 2015 [@planck2015], 2018 [@planck2018], and the so-called NPIPE release [@planck2021].

[^demo]: The availability of the server hosting the demo is best effort and not guaranteed in the long-term.

[^PLA]: <https://pla.esac.esa.int/>
# Example usage

## Remote access

```python
from libinsdb import RemoteInsDb

# Connect to a remote database
insdb = RemoteInsDb(
    server_address="https://insdbdemo.fisica.unimi.it",
    username="demo",
    password="planckdbdemo",
)

# Query a data file
data_file = insdb.query_data_file(
    "/releases/planck2021/LFI/frequency_030_ghz/bandpass"
)

# Open the actual file associated with the database entry
with data_file.open_data_file(insdb) as my_file:
    contents = my_file.read()

# `contents` is returned as a raw stream of bytes,
# but the format specification clarifies that it is
# a UTF-8 encoded file, so decode it
decoded_contents = contents.decode("utf-8")
```

## Local export

```python
from libinsdb import LocalInsDb

# Connect to a remote database
insdb = LocalInsDb("/path/to/exported/db")

# From now on, all the commands are the same as for
# the remote case
```

# Availability and documentation

The source code of InstrumentDB is available at <https://github.com/ziotom78/instrumentdb>, while Libinsdb is available at <https://github.com/ziotom78/libinsdb>. Both repositories contain full documentation published through GitHub pages. Continuous integration tests ensure the functionality of both InstrumentDB and LibinsDB.

InstrumentDB is released under GPL-3, whereas Libinsdb is released under the more permissive MIT license.

# Acknowledgements

We thank our colleagues and students who contributed ideas and testing during
the development of InstrumentDB and Libinsdb.

We acknowledge the use of AI tools (ChatGPT, PaperPal) for brainstorming and syntax/grammar checks. No content generated by AI technologies has been presented as our own work.

# References
