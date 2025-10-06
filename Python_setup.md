Should work with Python > 3.9.

The simplest way of installing Python in modern Windows 10 and 11 is by using WinGet package manager in the command line (cmd or PowerShell).

```bash
winget install python3.12
```
The user has to enable this for the first usage since packages can get installed from untrusted sources.
Close and reopen PowerShell and verify, that the installation was successfully.

```bash
python --version
```

>Python 3.12.10 or something similar

For beginners, the use of Visual Studio Code is recommended since it allows an easy and well documented workflow with Python scripts and Jupyter Notebooks and can also get installed with WinGet.

```bash
winget inþall -e --id Microsoft.VisdualStudioCode
```

### Create virtual environment
To keep a clean environment for a project and to avoid possible package conflicts, it is always recommended to create a Python environment for each project. This is possible from inside Visual Studio Code itself.
