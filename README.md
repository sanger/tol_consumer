# tol-lab-share

Rabbitmq consumer for TOL data input


## Getting Started

The following tools are required for development:

- python (use pyenv or something similar to install the python version specified in the `Pipfile`)

Use pyenv or something similar to install the version of python
defined in the `Pipfile`:

```bash
    brew install pyenv
    pyenv install <python_version>
```
        
Use pipenv to install the required python packages for the application and development:

```bash
     pipenv install --dev
```


### Setting up with Docker

If you want to setup a local development environment with Docker please check
the instructions in [SETUP_DOCKER.md](SETUP_DOCKER.md)


## Running

1. Enter the python virtual environment using:
```bash
    pipenv shell
```

1. Run the app using:

```bash
    python main.py
```

## Testing

Run the tests using pytest (flags are for verbose and exit early):

```bash
    python -m pytest -vx
```


## Deployment

This project uses a Docker image as the unit of deployment. Update `.release-version` with
major/minor/patch. On merging a pull request into *develop* or *master*, a release will be created
along with the Docker image associated to that release.

## Snappy

```
If when you install the dependencies and you see the following error:

[pipenv.exceptions.InstallError]:       src/snappy/snappymodule.cc:33:10: fatal error: 'snappy-c.h' file not found
[pipenv.exceptions.InstallError]:       #include <snappy-c.h>
[pipenv.exceptions.InstallError]:                ^~~~~~~~~~~~
[pipenv.exceptions.InstallError]:       1 error generated.
[pipenv.exceptions.InstallError]:       error: command '/usr/bin/clang' failed with exit code 1
[pipenv.exceptions.InstallError]:       [end of output]
[pipenv.exceptions.InstallError]:
[pipenv.exceptions.InstallError]:   note: This error originates from a subprocess, and is likely not a problem with pip.
[pipenv.exceptions.InstallError]:   ERROR: Failed building wheel for python-snappy
[pipenv.exceptions.InstallError]: ERROR: Could not build wheels for python-snappy, which is required to install pyproject.toml-based projects
ERROR: Couldn't install package: {}
 Package installation failed...
```

You need to install snappy and set the path:

```
brew install snappy
```

```
pip install --global-option=build_ext --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' python-snappy
```
