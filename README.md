# AWS MLOps Handson
This repository is designed to provide a comprehensive ML infrastructure for CTR (Click-Through Rate) prediction.  
With a focus on AWS services, this repository offer practical learning experience for MLOps.  
Slide[japanese]: https://speakerdeck.com/nsakki55/cyberagent-aishi-ye-ben-bu-mlopsyan-xiu-ying-yong-bian

## Key Features
### Python Development Environment  
We guide you through setting up a Python development environment that ensures code quality and maintainability.   
This environment is carefully configured to enable efficient development practices and facilitate collaboration.

### Train Pipeline
This repository includes the implementation of a training pipeline.   
This pipeline covers the stages, including data preprocessing, model training, and evaluation.   

### Prediction Server
This repository provides an implementation of a prediction server that serves predictions based on your trained CTR prediction model.   

### AWS Deployment
To showcase industry-standard practices, this repository guide you in deploying the training pipeline and inference server on AWS. 


## AWS Infra Architecture
AWS Infra Architecture made by this repository.

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
| [Docker](https://docs.docker.com/desktop/install/mac-install/) | install via dmg |
| [awscli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-installjkkkkj.html) | `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"` |

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
Set your environment variable setting
```bash
AWS_REGION=
AWS_ACCOUNT_ID=
AWS_PROFILE=
AWS_BUCKET=
AWS_ALB_DNS=
USER_NAME=
VERSION=2023-05-11
MODEL=sgd_classifier_ctr_model
```

### Create AWS Resources
move current directory to `infra` 
```bash
$ cd infra
```

Use terraform to create aws resources.   
Apply terraform
```bash
$ terraform init
$ terraform apply
```

### Prepare train data
unzip train data
```bash
$ unzip train_data.zip
```

upload train data to S3
```bash
$ aws s3 mv train_data s3://$AWS_BUCKET
```

## Code static analysis tool
| Tool                   | Usage              |
|----------------------------|----------------------------|
| [isort](https://pycqa.github.io/isort/)             | library import statement check     |
| [black](https://pypi.org/project/black/)           | format code style  |
| [flake8](https://flake8.pycqa.org/en/latest/)           | code quality check      |
| [mypy](https://mypy.readthedocs.io/en/stable/)    |  static type checking |
| [pysen](https://github.com/pfnet/pysen)    | manage static analysis tool  |



## Usage
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
