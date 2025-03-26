import requests
import json
import time
import os
from typing import Dict, Any, List, Optional

class ComfyUIAPI:
    def __init__(self, server_address: str = "http://127.0.0.1:8188"):
        """ComfyUI API 클라이언트 초기화

        Args:
            server_address: ComfyUI 서버 주소 (기본값: http://127.0.0.1:8188)
        """
        self.server_address = server_address
        self.history_data = {}
    
    def load_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """워크플로우 JSON 파일 로드

        Args:
            workflow_path: 워크플로우 JSON 파일 경로

        Returns:
            Dict: 로드된 워크플로우 데이터
        """
        with open(workflow_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def update_node_input(self, workflow: Dict[str, Any], node_id: str, input_name: str, new_value: Any) -> Dict[str, Any]:
        """워크플로우의 특정 노드의 입력값 업데이트

        Args:
            workflow: 워크플로우 데이터
            node_id: 업데이트할 노드 ID (문자열)
            input_name: 업데이트할 입력 파라미터 이름
            new_value: 새 입력값

        Returns:
            Dict: 업데이트된 워크플로우 데이터
        """
        if node_id in workflow:
            if input_name in workflow[node_id]["inputs"]:
                workflow[node_id]["inputs"][input_name] = new_value
                print(f"노드 {node_id}의 {input_name} 값을 업데이트했습니다.")
            else:
                print(f"경고: 노드 {node_id}에 {input_name} 입력이 없습니다.")
        else:
            print(f"경고: 워크플로우에 노드 {node_id}가 없습니다.")
        
        return workflow
    
    def run_workflow(self, workflow: Dict[str, Any], client_id: Optional[str] = None) -> str:
        """워크플로우 실행

        Args:
            workflow: 실행할 워크플로우 데이터
            client_id: 클라이언트 ID (옵션)

        Returns:
            str: 프롬프트 ID
        """
        # API 형식에 맞게 요청 데이터 구성
        prompt_data = {
            "prompt": workflow,
            "client_id": client_id if client_id else ""
        }
        
        # 워크플로우 실행 요청
        response = requests.post(f"{self.server_address}/prompt", json=prompt_data)
        
        if response.status_code != 200:
            raise Exception(f"워크플로우 실행 실패: {response.status_code}, {response.text}")
        
        result = response.json()
        print(f"응답 데이터: {result}")
        
        # prompt_id 추출 (ComfyUI 버전에 따라 다를 수 있음)
        prompt_id = ""
        if "prompt_id" in result:
            prompt_id = result["prompt_id"]
        elif "id" in result:
            prompt_id = result["id"]
        elif isinstance(result, list) and len(result) > 0:
            prompt_id = str(result[0])
        
        if not prompt_id:
            raise Exception(f"프롬프트 ID를 찾을 수 없습니다: {result}")
        
        print(f"워크플로우 실행 시작됨, 프롬프트 ID: {prompt_id}")
        return prompt_id
    
    def wait_for_completion(self, prompt_id: str, check_interval: float = 1.0) -> bool:
        """워크플로우 실행 완료 대기

        Args:
            prompt_id: 기다릴 프롬프트 ID
            check_interval: 상태 확인 간격(초)

        Returns:
            bool: 실행 성공 여부
        """
        print("실행 완료 대기 중...")
        while True:
            # 큐 상태 확인
            response = requests.get(f"{self.server_address}/queue")
            
            if response.status_code != 200:
                print(f"큐 상태 확인 실패: {response.status_code}")
                time.sleep(check_interval)
                continue
            
            queue_data = response.json()
            
            # 디버깅을 위해 큐 데이터 구조 출력
            # print("큐 데이터 구조:", json.dumps(queue_data, indent=2))
            
            # ComfyUI 큐 데이터 구조 처리
            running_prompts = []
            pending_prompts = []
            
            # 큐 데이터 구조 확인 및 처리
            if "queue_running" in queue_data:
                if isinstance(queue_data["queue_running"], list):
                    for item in queue_data["queue_running"]:
                        if isinstance(item, dict) and "prompt_id" in item:
                            running_prompts.append(item["prompt_id"])
                        elif isinstance(item, list) and len(item) > 0:
                            running_prompts.append(item[0])  # 첫 번째 요소가 prompt_id일 수 있음
            
            if "queue_pending" in queue_data:
                if isinstance(queue_data["queue_pending"], list):
                    for item in queue_data["queue_pending"]:
                        if isinstance(item, dict) and "prompt_id" in item:
                            pending_prompts.append(item["prompt_id"])
                        elif isinstance(item, list) and len(item) > 0:
                            pending_prompts.append(item[0])  # 첫 번째 요소가 prompt_id일 수 있음
            
            print(f"실행 중인 작업: {running_prompts}")
            print(f"대기 중인 작업: {pending_prompts}")
            
            # 해당 프롬프트가 큐에 없고 처리 중인 작업도 없으면 완료로 간주
            if prompt_id not in running_prompts and prompt_id not in pending_prompts:
                if not running_prompts:
                    print("워크플로우 실행 완료!")
                    return True
            
            # 아직 완료되지 않았으면 대기
            time.sleep(check_interval)
    
    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """특정 프롬프트의 실행 결과 이력 조회

        Args:
            prompt_id: 조회할 프롬프트 ID

        Returns:
            Dict: 이력 데이터
        """
        response = requests.get(f"{self.server_address}/history")
        
        if response.status_code != 200:
            raise Exception(f"이력 조회 실패: {response.status_code}")
        
        history = response.json()
        self.history_data = history
        
        if prompt_id in history:
            return history[prompt_id]
        else:
            print(f"경고: 프롬프트 ID {prompt_id}에 대한 이력이 없습니다.")
            return {}
    
    def download_images(self, prompt_id: str, output_dir: str = "output") -> List[str]:
        """생성된 이미지 다운로드

        Args:
            prompt_id: 이미지를 생성한 프롬프트 ID
            output_dir: 이미지를 저장할 디렉토리

        Returns:
            List[str]: 다운로드된 이미지 파일 경로 목록
        """
        # 이력 조회
        history = self.get_history(prompt_id)
        
        if not history or "outputs" not in history:
            print(f"경고: 프롬프트 ID {prompt_id}에 대한 출력이 없습니다.")
            return []
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 이미지 다운로드
        downloaded_files = []
        outputs = history.get("outputs", {})
        
        for node_id, node_output in outputs.items():
            for output_type, output_data in node_output.items():
                if output_type == "images":
                    for image_data in output_data:
                        filename = image_data.get("filename", "")
                        if filename:
                            # 이미지 파일 다운로드
                            image_url = f"{self.server_address}/view?filename={filename}"
                            local_path = os.path.join(output_dir, os.path.basename(filename))
                            
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                with open(local_path, "wb") as file:
                                    file.write(response.content)
                                
                                print(f"이미지 다운로드 완료: {local_path}")
                                downloaded_files.append(local_path)
                            else:
                                print(f"이미지 다운로드 실패: {filename}, 상태 코드: {response.status_code}")
        
        return downloaded_files


# 메인 실행 코드
if __name__ == "__main__":
    try:
        # ComfyUI API 클라이언트 초기화
        api = ComfyUIAPI("http://127.0.0.1:8188")  # 서버 주소 확인
        print("ComfyUI API 클라이언트가 초기화되었습니다.")
        
        # 워크플로우 파일 경로 확인
        workflow_path = "FluxAPi.json"
        print(f"워크플로우 파일 '{workflow_path}' 로드 중...")
        
        # 워크플로우 로드
        try:
            workflow = api.load_workflow(workflow_path)
            print("워크플로우 로드 성공!")
        except Exception as e:
            print(f"워크플로우 로드 실패: {e}")
            print(f"현재 작업 디렉토리: {os.getcwd()}")
            print(f"파일 존재 여부: {os.path.exists(workflow_path)}")
            raise
        
        # 테스트 실행을 위한 스토리 설명 목록
        # stories 폴더 내 JSON 파일 로드
        stories_folder = "stories"
        story_descriptions = []

        if os.path.exists(stories_folder) and os.path.isdir(stories_folder):
            for filename in os.listdir(stories_folder):
                if filename.endswith(".json"):
                    file_path = os.path.join(stories_folder, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            story_data = json.load(file)
                            if isinstance(story_data, dict) and "pages" in story_data:
                                for page in story_data["pages"]:
                                    if "image" in page:
                                        story_descriptions.append(page["image"])
                            else:
                                print(f"경고: 파일 {filename}에 'pages' 키가 없거나 올바르지 않습니다.")
                    except Exception as e:
                        print(f"파일 {filename} 로드 중 오류 발생: {e}")
        else:
            print(f"경고: '{stories_folder}' 폴더가 존재하지 않습니다.")
        # story_descriptions = [
        #     "작은 별 반짝이가 혼자서는 빛이 약해 슬펐지만, 친구들과 함께 모여 밝게 빛나게 되었어요.",
        #     "용감한 토끼 동동이가 숲속 친구들을 도와 겨울을 준비하는 이야기입니다.",
        #     "마법의 연필을 발견한 소녀가 그림으로 세상을 바꾸는 모험을 떠납니다.",
        #     "바다 속 작은 물고기가 플라스틱 쓰레기를 치우며 바다를 깨끗하게 만드는 환경 이야기",
        #     "하늘을 날고 싶었던 작은 거북이의 끈기와 노력으로 꿈을 이루는 감동적인 모험"
        # ]
        
        # 첫 번째 설명만 테스트로 실행
        print(f"\n===== 테스트 실행 =====")
        print(f"설명: {story_descriptions[0]}")
        
        # 워크플로우 복사 (원본 유지를 위해)
        current_workflow = workflow.copy()
        
        # 노드 32의 텍스트 입력 업데이트
        current_workflow = api.update_node_input(current_workflow, "32", "text", story_descriptions[0])
        
        # 워크플로우 실행
        try:
            prompt_id = api.run_workflow(current_workflow)
            print(f"워크플로우 실행 요청 성공, ID: {prompt_id}")
        except Exception as e:
            print(f"워크플로우 실행 요청 실패: {e}")
            raise
            
        # 완료 대기
        try:
            api.wait_for_completion(prompt_id)
        except Exception as e:
            print(f"워크플로우 완료 대기 실패: {e}")
            raise
            
        # 이미지 다운로드
        output_dir = "output/test"
        try:
            downloaded_files = api.download_images(prompt_id, output_dir)
            print(f"생성된 이미지: {len(downloaded_files)}개")
            for file in downloaded_files:
                print(f" - {file}")
        except Exception as e:
            print(f"이미지 다운로드 실패: {e}")
            
        print("===== 테스트 실행 완료 =====\n")
        
        # 첫 번째 테스트가 성공하면 나머지 실행
        print("첫 번째 테스트가 성공했습니다. 나머지 설명으로 계속하시겠습니까? (y/n)")
        response = 'y'
        
        if response == 'y':
            # 나머지 설명으로 이미지 생성
            for i, description in enumerate(story_descriptions[1:], 1):
                print(f"\n===== 스토리 {i+1} 이미지 생성 시작 =====")
                print(f"설명: {description}")
                
                # 워크플로우 복사 (원본 유지를 위해)
                current_workflow = workflow.copy()
                
                # 노드 32의 텍스트 입력 업데이트
                current_workflow = api.update_node_input(current_workflow, "32", "text", description)
                
                # 워크플로우 실행
                prompt_id = api.run_workflow(current_workflow)
                
                # 완료 대기
                api.wait_for_completion(prompt_id)
                
                # 이미지 다운로드
                output_dir = f"output/story_{i+1}"
                downloaded_files = api.download_images(prompt_id, output_dir)
                
                print(f"생성된 이미지: {len(downloaded_files)}개")
                for file in downloaded_files:
                    print(f" - {file}")
                
                print(f"===== 스토리 {i+1} 이미지 생성 완료 =====\n")
                
                # 요청 간격 두기 (서버 부하 방지)
                if i < len(story_descriptions) - 1:
                    time.sleep(2)
    
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()