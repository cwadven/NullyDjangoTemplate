import os
from django.core.management.base import BaseCommand
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def create_file_from_project_root(path):
    if is_creatable_file(path):
        f = open(os.path.join(BASE_DIR, *path.split("/")), "w+")
        f.close()
    else:
        print("파일을 생성할 위치의 상위 폴더가 존재하지 않습니다.")


def create_folder_from_project_root(path):
    os.makedirs(os.path.join(BASE_DIR, *path.split("/")), exist_ok=True)


def is_creatable_file(path):
    has_parent_folder = len(path.split("/")) > 1
    is_parent_folder_exist = has_parent_folder and os.path.exists(os.path.join(BASE_DIR, *path.split("/")[:-1]))

    return (not has_parent_folder) or is_parent_folder_exist


def set_gitaction_settings(path, name, **kwargs):
    """
    CI/CD 용 yml 설정
    path - setting 할 yml 경로
    name - CI/CD 명
    kwargs - name: yml 이름 / branch: 적용 브랜치 / steps: 단계별 실행할 이름과 명령

    :param path: file-path
    :param name: CI/CD 명
    :param kwargs: branch-str, status-str, steps-list in objects [{"name": "", "run": ""}, ]
    :return:
    """
    if is_creatable_file(path):
        with open(path, 'w+') as f:
            f.writelines(f"name: {name}\n\n")

            f.writelines(f"on:\n")
            f.writelines(f"  {kwargs.get('status', 'push')}:\n")
            f.writelines(f"    branch: [ {kwargs.get('branch', 'master')} ]\n\n")

            f.writelines(f"jobs:\n")
            f.writelines(f"  build:\n")
            f.writelines(f"    runs-on: self-hosted\n\n")

            f.writelines(f"    steps:\n")

            for step in kwargs.get('steps', []):
                f.writelines(f"    - name: {step.get('name', '')}\n")
                f.writelines(f"      run: |\n")
                f.writelines(f"        {step.get('run', '')}\n\n")


class Command(BaseCommand):
    help = "GitActions 추가하는 명령"

    def add_arguments(self, parser):

        # 키워드 인자 (named arguments)
        parser.add_argument("github_action_file_name", type=str, help="GitHubAction 이름 설정")

    def handle(self, *args, **kwargs):
        """
        실행할 동작을 정의해줌
        """
        github_action_file_name = kwargs.get("github_action_file_name", "default")  # 최근 며칠간 쪽지를 삭제할것인지

        create_folder_from_project_root(".github/workflows")
        create_file_from_project_root(f".github/workflows/{github_action_file_name}.yml")
        set_gitaction_settings(
            f".github/workflows/{github_action_file_name}.yml",
            "CI/CD",
            branch="master",
            status="push",
            steps=[
                {"name": "Pull Request", "run": "cd /var/www/roadmap/ && sudo git pull origin master"}
            ]
        )
        print('GitActions Code Setted')
