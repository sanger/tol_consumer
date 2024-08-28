# Tol Lab Share

RabbitMQ consumer for TOL input, and for Traction input in volume tracking.

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
the instructions in [SETUP_DOCKER.md](https://github.com/sanger/tol-lab-share/blob/develop/SETUP_DOCKER.md)

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

If when you install the dependencies and you see the following error:

```stdout
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

You need to install snappy:

```bash
brew install snappy
```

Ensure the `include` and `lib` directories of `homebrew` are set in environment variables.
You might want to add these to your `~/.zshrc` file:

```bash
export CPPFLAGS="-I$(brew --prefix)/include"
export LDFLAGS="-L$(brew --prefix)/lib"
```

## TOL Automated Manifest Process

Following diagram discusses how automated manifests are received by `tol-lab-share` and published to Traction.

![TOL Labware Production Flow - Architecture](https://github.com/sanger/tol-lab-share/assets/519327/5356846a-6d9b-4b8d-8ffb-af26d0776222)

## Formatting, Type Checking and Linting

Black is used as a formatter, to format code before committing:

    black .

Mypy is used as a type checker, to execute:

    mypy .

Flake8 is used for linting, to execute:

    flake8

## API Docs

API Docs can be accessed via [https://sanger.github.io/tol-lab-share/api-docs/](https://sanger.github.io/tol-lab-share/api-docs/).
