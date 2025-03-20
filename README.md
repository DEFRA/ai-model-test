# cdp-python-backend-template

This is work-in-progress. See [To Do List](./TODO.md)

- [cdp-python-backend-template](#cdp-python-backend-template)
  - [Requirements](#requirements)
    - [Python](#python)
    - [Docker](#docker)
  - [Local development](#local-development)
    - [Setup](#setup)
    - [Development](#development)
    - [Testing](#testing)
    - [Production](#production)
  - [API endpoints](#api-endpoints)
  - [Custom Cloudwatch Metrics](#custom-cloudwatch-metrics)
  - [Pipelines](#pipelines)
    - [Dependabot](#dependabot)
    - [SonarCloud](#sonarcloud)
  - [Licence](#licence)
    - [About the licence](#about-the-licence)

## Requirements

### Python

Please install python `>= 3.12` and [configure your python virtual environment](https://fastapi.tiangolo.com/virtual-environments/#create-a-virtual-environment):

```python
# create the virtual environment
python -m venv .venv

# activate the the virtual environment in the command line
source .venv/bin/activate

# update pip
python -m pip install --upgrade pip

# install the dependencies
pip install -r requirements-dev.txt
```

This opinionated template uses the [`Fast API`](https://fastapi.tiangolo.com/) Python API framework.

This and all other runtime python libraries must reside in `requirements.txt`

Other non-runtime dependencies used for dev & test must reside in `requirements-dev.txt`

### Docker

This repository uses Docker throughput its lifecycle i.e. both for local development and the environments. A benefit of this is that environment variables & secrets are managed consistently throughout the lifecycle

See the `Dockerfile` and `compose.yml` for details

### Linting and Formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting Python code.

#### Running Ruff

To run Ruff from the command line:

```bash
# Run linting with auto-fix
ruff check . --fix

# Run formatting
ruff format .
```

#### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run linting and formatting checks automatically before each commit.

The pre-commit configuration is defined in `.pre-commit-config.yaml`

To set up pre-commit hooks:

```bash
# Set up the git hooks
pre-commit install

# Alternatively, use the provided setup script
python scripts/setup_hooks.py
```

To run the hooks manually on all files:

```bash
pre-commit run --all-files
```

#### VS Code Configuration

For the best development experience, configure VS Code to use Ruff:

1. Install the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for VS Code
2. Configure your VS Code settings (`.vscode/settings.json`):

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.ruff": "explicit",
        "source.organizeImports.ruff": "explicit"
    },
    "ruff.lint.run": "onSave",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```

This configuration will:

- Format your code with Ruff when you save a file
- Fix linting issues automatically when possible
- Organize imports according to isort rules

#### Ruff Configuration

Ruff is configured in the `.ruff.toml` file

## Local development

### Setup

Libraries: Ensure the python virtual environment is configured and libraries are installed using `requirements-dev.txt`, [as above](#python)

Environment variables: `compose/aws.env`

Secrets: `compose/secrets.env`. You need to create this, as it's excluded from version control.

### Development

The app can be run locally using Docker compose.  This template contains a local environment with:

- Localstack
- MongoDB
- This service

To run the application in development mode:

```bash
docker compose watch
```

Alternatively you can start it using:
```
 uvicorn app.main:app --log-config logging-dev.json --reload
```

### Testing

Ensure the python virtual environment is configured and libraries are installed using `requirements-dev.txt`, [as above](#python)

Testing follows the [FastApi documented approach](https://fastapi.tiangolo.com/tutorial/testing/); using pytest & starlette.

To test the application run:

```bash
pytest
```

### Production

To mimic the application running in `production mode locally run:

```bash
docker compose up --build -d
```

Stop the application with

```bash
docker compose down
```

Alternatively you can start it using:

```bash
$ uvicorn app.main:app --host=0.0.0.0 --log-config logging.json --no-access-log
```


## API endpoints

| Endpoint             | Description                    |
| :------------------- | :----------------------------- |
| `GET: /docs`         | Automatic API Swagger docs     |
| `GET: /example`      | Simple example                 |

## Custom Cloudwatch Metrics

Uses the [aws embedded metrics library](https://github.com/awslabs/aws-embedded-metrics-python). An example can be found in `metrics.py`

In order to make this library work in the environments, the environment variable `AWS_EMF_ENVIRONMENT=local` is set in the app config. This tells the library to use the local cloudwatch agent that has been configured in CDP, and uses the environment variables set up in CDP `AWS_EMF_AGENT_ENDPOINT`, `AWS_EMF_LOG_GROUP_NAME`, `AWS_EMF_LOG_STREAM_NAME`, `AWS_EMF_NAMESPACE`, `AWS_EMF_SERVICE_NAME`

## Pipelines

### Dependabot

We have added an example dependabot configuration file to the repository. You can enable it by renaming
the [.github/example.dependabot.yml](.github/example.dependabot.yml) to `.github/dependabot.yml`

### SonarCloud

Instructions for setting up SonarCloud can be found in [sonar-project.properties](./sonar-project.properties)

## Licence

THIS INFORMATION IS LICENSED UNDER THE CONDITIONS OF THE OPEN GOVERNMENT LICENCE found at:

<http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3>

The following attribution statement MUST be cited in your products and applications when using this information.

> Contains public sector information licensed under the Open Government license v3

### About the licence

The Open Government Licence (OGL) was developed by the Controller of Her Majesty's Stationery Office (HMSO) to enable
information providers in the public sector to license the use and re-use of their information under a common open
licence.

It is designed to encourage use and re-use of information freely and flexibly, with only a few conditions.
