# tol_consumer

Rabbitmq consumer for TOL data input


### Requirements for Development

The following tools are required for development:

- python (use pyenv or something similar to install the python version specified in the `Pipfile`)

### Getting Started

#### Setup

- Use pyenv or something similar to install the version of python
  defined in the `Pipfile`:

        brew install pyenv
        pyenv install <python_version>
        
- Use pipenv to install the required python packages for the application and development:

        pipenv install --dev

### Running

1. Enter the python virtual environment using:

        pipenv shell

1. Run the app using:

        flask run

### Testing

Run the tests using pytest (flags are for verbose and exit early):

    python -m pytest -vx

## Deployment

This project uses a Docker image as the unit of deployment. Update `.release-version` with
major/minor/patch. On merging a pull request into *develop* or *master*, a release will be created
along with the Docker image associated to that release.

