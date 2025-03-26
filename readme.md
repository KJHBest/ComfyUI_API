# ComfyUI API Client for Story Image Generation

<div align="right">
<a href="#english">English</a> | <a href="#korean">한국어</a>
</div>

<a id="english"></a>
# ComfyUI API Client for Story Image Generation

A Python-based client for interacting with ComfyUI to automate the generation of images based on story descriptions.

## Overview

This project provides a simple API client for ComfyUI that allows you to:

- Load and modify ComfyUI workflows
- Update specific node inputs programmatically
- Execute workflows and monitor their completion
- Retrieve and download generated images
- Process story descriptions from JSON files

## Features

- Simple interface to the ComfyUI API
- Ability to batch process multiple story prompts
- Automatic workflow execution and image downloading
- Detailed progress logging and error handling

## Prerequisites

- Python 3.6+
- ComfyUI server running (default: http://127.0.0.1:8188)
- Required Python packages:
  - requests
  - json
  - time
  - os

## Project Structure

```
.
├── compyuiAPI.py        # Main API client implementation
├── FluxAPi.json         # ComfyUI workflow file
├── stories/             # Folder containing story description files
│   ├── fairy-tale-1.json
│   ├── storybook-1.json
│   ├── storybook-2.json
│   ├── storybook-3.json
│   ├── storybook-4.json
│   └── storybook-5.json
└── output/              # Generated images will be saved here
    ├── test/
    ├── story_1/
    ├── story_2/
    └── ...
```

## Usage

### Basic Usage

```python
from compyuiAPI import ComfyUIAPI

# Initialize the API client
api = ComfyUIAPI("http://127.0.0.1:8188")

# Load a workflow
workflow = api.load_workflow("FluxAPi.json")

# Update a node input (e.g., changing the text prompt)
workflow = api.update_node_input(workflow, "32", "text", "A magical forest with talking animals")

# Run the workflow
prompt_id = api.run_workflow(workflow)

# Wait for completion
api.wait_for_completion(prompt_id)

# Download the generated images
downloaded_files = api.download_images(prompt_id, "output/my_image")
```

### Processing Story Files

The project is designed to process story files in JSON format. Each story file should have the following structure:

```json
{
  "title": "Story Title",
  "pages": [
    {
      "text": "Story text for page 1",
      "image": "Detailed description for image generation"
    },
    ...
  ]
}
```

The script automatically extracts the image descriptions from these files and uses them as prompts for image generation.

### Running the Script

Simply execute the main script:

```bash
python compyuiAPI.py
```

The script will:

1. Load the workflow file
2. Find all JSON story files in the `stories` directory
3. Extract image descriptions from those files
4. Execute a test run with the first description
5. Process all remaining descriptions if the test is successful

## API Documentation

### ComfyUIAPI Class

#### `__init__(server_address="http://127.0.0.1:8188")`
Initializes the ComfyUI API client with the specified server address.

#### `load_workflow(workflow_path)`
Loads a ComfyUI workflow from a JSON file.

#### `update_node_input(workflow, node_id, input_name, new_value)`
Updates a specific input parameter of a node in the workflow.

#### `run_workflow(workflow, client_id=None)`
Executes the workflow and returns the prompt ID.

#### `wait_for_completion(prompt_id, check_interval=1.0)`
Waits until the workflow execution is complete.

#### `get_history(prompt_id)`
Retrieves the execution history for the specified prompt ID.

#### `download_images(prompt_id, output_dir="output")`
Downloads all generated images from the workflow execution.

## Troubleshooting

- Make sure the ComfyUI server is running on the specified address
- Check that the workflow file exists and is correctly formatted
- Verify that the node IDs and input parameter names are correct

## Note

This API client is designed specifically for the included workflow. If you're using a different workflow, you may need to adjust the node IDs and input parameter names accordingly.

---

<a id="korean"></a>
# 스토리 이미지 생성을 위한 ComfyUI API 클라이언트

<div align="right">
<a href="#english">English</a> | <a href="#korean">한국어</a>
</div>

ComfyUI와 상호작용하여 스토리 설명을 기반으로 이미지 생성을 자동화하는 Python 기반 클라이언트입니다.

## 개요

이 프로젝트는 ComfyUI를 위한 간단한 API 클라이언트를 제공하여 다음과 같은 기능을 수행할 수 있습니다:

- ComfyUI 워크플로우 로드 및 수정
- 특정 노드 입력을 프로그래밍 방식으로 업데이트
- 워크플로우 실행 및 완료 모니터링
- 생성된 이미지 검색 및 다운로드
- JSON 파일에서 스토리 설명 처리

## 기능

- ComfyUI API에 대한 간단한 인터페이스
- 여러 스토리 프롬프트를 일괄 처리하는 기능
- 자동 워크플로우 실행 및 이미지 다운로드
- 자세한 진행 상황 로깅 및 오류 처리

## 필수 조건

- Python 3.6 이상
- ComfyUI 서버 실행 중 (기본값: http://127.0.0.1:8188)
- 필요한 Python 패키지:
  - requests
  - json
  - time
  - os

## 프로젝트 구조

```
.
├── compyuiAPI.py        # 주요 API 클라이언트 구현
├── FluxAPi.json         # ComfyUI 워크플로우 파일
├── stories/             # 스토리 설명 파일이 포함된 폴더
│   ├── fairy-tale-1.json
│   ├── storybook-1.json
│   ├── storybook-2.json
│   ├── storybook-3.json
│   ├── storybook-4.json
│   └── storybook-5.json
└── output/              # 생성된 이미지가 저장될 폴더
    ├── test/
    ├── story_1/
    ├── story_2/
    └── ...
```

## 사용 방법

### 기본 사용법

```python
from compyuiAPI import ComfyUIAPI

# API 클라이언트 초기화
api = ComfyUIAPI("http://127.0.0.1:8188")

# 워크플로우 로드
workflow = api.load_workflow("FluxAPi.json")

# 노드 입력 업데이트 (예: 텍스트 프롬프트 변경)
workflow = api.update_node_input(workflow, "32", "text", "말하는 동물이 있는 마법의 숲")

# 워크플로우 실행
prompt_id = api.run_workflow(workflow)

# 완료 대기
api.wait_for_completion(prompt_id)

# 생성된 이미지 다운로드
downloaded_files = api.download_images(prompt_id, "output/my_image")
```

### 스토리 파일 처리

이 프로젝트는 JSON 형식의 스토리 파일을 처리하도록 설계되었습니다. 각 스토리 파일은 다음과 같은 구조를 가져야 합니다:

```json
{
  "title": "스토리 제목",
  "pages": [
    {
      "text": "페이지 1의 스토리 텍스트",
      "image": "이미지 생성을 위한 자세한 설명"
    },
    ...
  ]
}
```

스크립트는 이러한 파일에서 이미지 설명을 자동으로 추출하여 이미지 생성을 위한 프롬프트로 사용합니다.

### 스크립트 실행

간단히 메인 스크립트를 실행하세요:

```bash
python compyuiAPI.py
```

스크립트는 다음을 수행합니다:

1. 워크플로우 파일 로드
2. `stories` 디렉토리에서 모든 JSON 스토리 파일 찾기
3. 해당 파일에서 이미지 설명 추출
4. 첫 번째 설명으로 테스트 실행
5. 테스트가 성공하면 모든 남은 설명 처리

## API 문서

### ComfyUIAPI 클래스

#### `__init__(server_address="http://127.0.0.1:8188")`
지정된 서버 주소로 ComfyUI API 클라이언트를 초기화합니다.

#### `load_workflow(workflow_path)`
JSON 파일에서 ComfyUI 워크플로우를 로드합니다.

#### `update_node_input(workflow, node_id, input_name, new_value)`
워크플로우에서 노드의 특정 입력 매개변수를 업데이트합니다.

#### `run_workflow(workflow, client_id=None)`
워크플로우를 실행하고 프롬프트 ID를 반환합니다.

#### `wait_for_completion(prompt_id, check_interval=1.0)`
워크플로우 실행이 완료될 때까지 대기합니다.

#### `get_history(prompt_id)`
지정된 프롬프트 ID에 대한 실행 기록을 검색합니다.

#### `download_images(prompt_id, output_dir="output")`
워크플로우 실행에서 생성된 모든 이미지를 다운로드합니다.

## 문제 해결

- ComfyUI 서버가 지정된 주소에서 실행 중인지 확인
- 워크플로우 파일이 존재하고 올바르게 포맷되었는지 확인
- 노드 ID와 입력 매개변수 이름이 올바른지 확인

## 참고

이 API 클라이언트는 포함된 워크플로우에 맞게 특별히 설계되었습니다. 다른 워크플로우를 사용하는 경우 노드 ID와 입력 매개변수 이름을 적절히 조정해야 할 수 있습니다.
