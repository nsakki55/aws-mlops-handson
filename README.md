# AWS MLOps Handson
## Architecture
AWS Infra Architecture made by the handson.
### ML Pipeline
![ml_pipeline](./imgs/ml_pipeline_architecture.png)

### Predict Server
![predict_server](./imgs/predict_server_architecture.png)

## Requirements
| Software                   | Install (Mac)              |
|----------------------------|----------------------------|
| [pyenv](https://github.com/pyenv/pyenv#installation)             | `brew install pyenv`       |
| [Poetry](https://python-poetry.org/docs/#installation)           | curl -sSL https://install.python-poetry.org &#x7C; python3 - |
| [direnv](https://formulae.brew.sh/formula/direnv)           | `brew install direnv`      |
| [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-terraform)    | `brew install terraform`   |

## Setup
### Install Python Dependencies
Use `pyenv` to install Python 3.9.0 environment
```bash
$ pyenv install 3.9.0
$ pyenv local 3.9.0
```

Use `poetry` to install library dependencies 
```bash
$ poetry install
```

### Configure environment variable
Use `direnv` to configure environment variable
```bash
$ cp .env.example .env
$ direnv allow .
```

## Usage
### Create AWS Resources
move current directory to `infra` 
```bash
$ cd infra
```

Use terraform to create aws resources.   
Set your aws resource values in vars.tfvars
```bash
aws_region="{your-aws-region}"         # e.g| ap-northeast-1
aws_profile="{your-aws-profile}"       # e.g| default
aws_account_id="{your-aws-account-id}" # e.g| 0123456789101
```
Apply terraform
```bash
$ terraform init
$ terraform -var-file terraform.tfvars
```


### Local Command
Build ML Pipeline
```bash
$ make build-ml
```

Run ML Pipeline
```bash
$ make run-ml
```

Build Predict API
```bash
$ make build-predictor
```

Run Predict API locally
```bash
$ make up
```

Shutdown Predict API locally
```bash
$ make down
```

Run formatter
```bash
$ make format
```

Run linter 
```bash
$ make lint 
```

Run pytest 
```bash
$ make test 
```
