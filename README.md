# turbular_reactor_lib
Collection of functions for microreactor usage

## Set up python

Should work with Python > 3.9.

The simplest way of installing Python in modern Windows 10 and 11 is by using winget package manager in cmd. 

```cmd
winget install python3.12
```
Close and reopen powershell and verify, that the installation was succesful

```cmd
python --version
```

>Python 3.12.10 or something similar


### Create virtual environment
To keep a clean environment for a project and to avoid possible package conflicts, it is always recomended to create a new Python environment for a new project. For that direct into the user directory with `cd ~`, Documents `cd ~/Documents` or any other prefered location into your shell, create a new folder for that project `mkdir <name of project>`, move into it `cd <name_of_project>` and create a virtual environment

```cmd
python -m venv <venv_of_project>
```

Now the github repository can be downloaded, unpacked and the content moved into the folder of the project (so that `src`, `requirements.txt` and `<venv_of_project>` are in the same folder). Then activate the virtual environment and install all necessay packages.
```cmd
.\<venv_of_project>\Scripts\activate
pip install -r requirements
```
