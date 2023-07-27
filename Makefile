.PHONY: all
all: help

ECR_REPOSITORY := $(AWS_ACCOUNT_ID).dkr.ecr.ap-northeast-1.amazonaws.com
DOCKER_TAG := latest
DOCKER_PREDICTOR_IMAGE := ${USER_NAME}-mlops-handson/predict-api
DOCKER_ML_IMAGE := ${USER_NAME}-mlops-handson/ml-pipeline
PORT := 8080


format: ## Run pysen format
	poetry run pysen run format

lint: ## Run code static analyse
	poetry run pysen run lint

test: ## Run pytest
	poetry run pytest

build-ml: ## Build docker image to ml pipeline
	docker build -t $(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE):$(DOCKER_TAG) --target ml ./

push-ml: ## Push ml pipeline image to ECR
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $(ECR_REPOSITORY)
	docker tag $(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE):$(DOCKER_TAG) $(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE):latest
	docker push $(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE):$(DOCKER_TAG) && docker push $(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE):latest

run-ml: ## Run ml Pipeline
	docker run -it -v $(HOME)/.aws/credentials:/root/.aws/credentials:ro \
				-e AWS_PROFILE=$(AWS_PROFILE) \
				-e AWS_BUCKET=${AWS_BUCKET} \
				-e MODEL=${MODEL} \
				-e VERSION=${VERSION} \
				$(ECR_REPOSITORY)/$(DOCKER_ML_IMAGE)

build-predictor: ## Build docker image to deploy
	docker build -t $(ECR_REPOSITORY)/$(DOCKER_PREDICTOR_IMAGE):$(DOCKER_TAG) --target predictor ./

push-predictor: ## Push predictor image to ECR
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $(ECR_REPOSITORY)
	docker tag $(ECR_REPOSITORY)/$(DOCKER_PREDICTOR_IMAGE):$(DOCKER_TAG) $(ECR_REPOSITORY)/$(DOCKER_PREDICTOR_IMAGE):latest
	docker push $(ECR_REPOSITORY)/$(DOCKER_PREDICTOR_IMAGE):$(DOCKER_TAG) && docker push $(ECR_REPOSITORY)/$(DOCKER_PREDICTOR_IMAGE):latest

up: ## Do docker compose up with hot reload
	docker-compose up -d

down: ## Do docker compose down
	docker-compose down

logs: ## Tail docker compose logs
	docker-compose logs -f

predict: ## Request prediction
	curl -X 'POST' 'http://localhost:${PORT}/predict' \
	    -H 'accept: application/json' \
	    -H 'Content-Type: application/json' \
	    -d '{"hour": "14102100", \
	         "banner_pos": "0", \
	         "site_id": "1fbe01fe", \
	         "site_domain": "f3845767", \
	         "site_category": "28905ebd", \
	         "app_id": "ecad2386", \
	         "app_domain": "7801e8d9", \
	         "app_category": "07d7df22", \
	         "device_id": "a99f214a", \
	         "device_ip": "ddd2926e", \
	         "device_model": "44956a24", \
	         "device_type": "1"}'

predict-ecs: ## Request prediction to ECS
	curl -X 'POST' '${AWS_ALB_DNS}:${PORT}/predict' \
	    -H 'accept: application/json' \
	    -H 'Content-Type: application/json' \
	    -d '{"hour": "14102100", \
	         "banner_pos": "0", \
	         "site_id": "1fbe01fe", \
	         "site_domain": "f3845767", \
	         "site_category": "28905ebd", \
	         "app_id": "ecad2386", \
	         "app_domain": "7801e8d9", \
	         "app_category": "07d7df22", \
	         "device_id": "a99f214a", \
	         "device_ip": "ddd2926e", \
	         "device_model": "44956a24", \
	         "device_type": "1"}'

healthcheck: ## Request health check
	curl -X 'GET' 'http://localhost:${PORT}/healthcheck'

check-scale: ## Request many times to check auto scaling
	hey -n 10000 -c 100 "http://${AWS_ALB_DNS}:${PORT}/healthcheck"

help: ## Show options
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

