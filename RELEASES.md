# How to prepare a new release

-   Update the version number in the following files:

    -   `pyproject.toml`

    -   `instrumentdb/__init__.py`

    -   `CHANGELOG.md` (be sure to leave an empty `HEAD` title at the
        top);
    
-   Run

    ```
    poetry update
    ```

-   Export the requirements:

    ```
    poetry export > requirements.txt
    ```

-   Create a `.tar.gz` file using `poetry build` and upload it to the GitHub release page.
