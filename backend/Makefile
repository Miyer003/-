# 默认输出帮助信息
.DEFAULT_GOAL := help
# 检查 tmux 是否存在
TMUX_EXISTS := $(shell command -v tmux)
# 远程仓库
REMOTE_REPOSITORY = registry.cn-hangzhou.aliyuncs.com/schwarzsail/docker
# 项目 MODULE 名
MODULE = yunyiwang
# 当前架构
ARCH := $(shell uname -m)
# 目录相关
DIR = $(shell pwd)
CMD = $(DIR)/cmd
CONFIG_PATH = $(DIR)/config
IDL_PATH = $(DIR)/idl
OUTPUT_PATH = $(DIR)/output
API_PATH= $(DIR)/cmd/api

# 服务名
SERVICES := api
service = $(word 1, $@)

PREFIX = "[Makefile]"

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  {service name}    : Build a specific service (e.g., make api). use BUILD_ONLY=1 to avoid auto bootstrap."
	@echo "                      Available service list: [${SERVICES}]"
	@echo "  env-up            : Start the docker-compose environment."
	@echo "  env-down          : Stop the docker-compose environment."
	@echo "  kitex-gen-%       : Generate Kitex service code for a specific service (e.g., make kitex-gen-user)."
	@echo "  kitex-update-%    : Update Kitex generated code for a specific service (e.g., make kitex-update-user)."
	@echo "  hertz-gen-api     : Generate Hertz scaffold based on the API IDL."
	@echo "  test              : Run unit tests for the project."
	@echo "  clean             : Remove the 'output' directories and related binaries."
	@echo "  clean-all         : Stop docker-compose services if running and remove 'output' directories and docker data."
	@echo "  push-%            : Push a specific service to the remote repository (e.g., make push-api)."
	@echo "  fmt               : Format the codebase using gofumpt."
	@echo "  import            : Optimize import order and structure."
	@echo "  vet               : Check for possible errors with go vet."
	@echo "  lint              : Run golangci-lint on the codebase."
	@echo "  verify            : Format, optimize imports, and run linters and vet on the codebase."
	@echo "  license           : Check and add license to go file and shell script."

## --------------------------------------
## 构建与调试
## --------------------------------------

# 启动必要的环境，比如 etcd、mysql
.PHONY: env-up
env-up:
	@ docker compose -f ./docker/docker-compose.yml up -d

# 关闭必要的环境，但不清理 data（位于 deploy/data 目录中）
.PHONY: env-down
env-down:
	@ cd ./deploy && docker compose down


.PHONY: $(SERVICES)
$(SERVICES):
	@if [ -z "$(TMUX_EXISTS)" ]; then \
		echo "$(PREFIX) tmux is not installed. Please install tmux first."; \
		exit 1; \
	fi
	@if [ -z "$$TMUX" ]; then \
		echo "$(PREFIX) you are not in tmux, press ENTER to start tmux environment."; \
		read -r; \
		if tmux has-session -t yuyiwang 2>/dev/null; then \
			echo "$(PREFIX) Tmux session 'yuyiwang' already exists. Attaching to session and running command."; \
			tmux attach-session -t yuyiwang; \
			tmux send-keys -t yuyiwang "make $(service)" C-m; \
		else \
			echo "$(PREFIX) No tmux session found. Creating a new session."; \
			tmux new-session -s yuyiwang "make $(service); $$SHELL"; \
		fi; \
	else \
		echo "$(PREFIX) Build $(service) target..."; \
		mkdir -p output; \
		bash $(DIR)/docker/script/build.sh $(service); \
		echo "$(PREFIX) Build $(service) target completed"; \
	fi
ifndef BUILD_ONLY
	@echo "$(PREFIX) Automatic run server"
	@if tmux list-windows -F '#{window_name}' | grep -q "^yuyiwang-$(service)$$"; then \
		echo "$(PREFIX) Window 'yuyiwang-$(service)' already exists. Reusing the window."; \
		tmux select-window -t "yuyiwang-$(service)"; \
	else \
		echo "$(PREFIX) Window 'yuyiwang-$(service)' does not exist. Creating a new window."; \
		tmux new-window -n "yuyiwang-$(service)"; \
		tmux split-window -h ; \
		tmux select-layout -t "yuyiwang-$(service)" even-horizontal; \
	fi
	@echo "$(PREFIX) Running $(service) service in tmux..."
	@tmux send-keys -t yuyiwang-$(service).0 'export SERVICE=$(service) && bash ./docker/script/entrypoint.sh' C-m
	@tmux select-pane -t yuyiwang-$(service).1
endif

# 推送到镜像服务中，需要提前 deploy login，否则会推送失败
.PHONY: push-%
push-%:
	@read -p "Confirm service name to push (type '$*' to confirm): " CONFIRM_SERVICE; \
	if [ "$$CONFIRM_SERVICE" != "$*" ]; then \
		echo "Confirmation failed. Expected '$*', but got '$$CONFIRM_SERVICE'."; \
		exit 1; \
	fi; \
	if echo "$(SERVICES)" | grep -wq "$*"; then \
		if [ "$(ARCH)" = "x86_64" ] || [ "$(ARCH)" = "amd64" ]; then \
			echo "Building and pushing $* for amd64 architecture..."; \
			docker build --build-arg SERVICE=$* -t $(REMOTE_REPOSITORY):$* -f deploy/Dockerfile .; \
			docker push $(REMOTE_REPOSITORY):$*; \
		else \
			echo "Building and pushing $* using buildx for amd64 architecture..."; \
			docker buildx build --platform linux/amd64 --build-arg SERVICE=$* -t $(REMOTE_REPOSITORY):$* -f deploy/Dockerfile --push .; \
		fi; \
	else \
		echo "Service '$*' is not a valid service. Available: [$(SERVICES)]"; \
		exit 1; \
	fi
## --------------------------------------
## 清理与校验
## --------------------------------------

# 清除所有的构建产物
.PHONY: clean
clean:
	@find . -type d -name "output" -exec rm -rf {} + -print

# 清除所有构建产物、compose 环境和它的数据
.PHONY: clean-all
clean-all: clean
	@echo "$(PREFIX) Checking if docker-compose services are running..."
	@docker-compose -f ./deploy/docker-compose.yml ps -q | grep '.' && docker-compose -f ./docker/docker-compose.yml down || echo "$(PREFIX) No services are running."
	@echo "$(PREFIX) Removing docker data..."
	rm -rf ./deploy/data