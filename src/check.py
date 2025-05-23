import json
import subprocess
from pathlib import Path

import github
import github.GitReleaseAsset

VERSION_PATH = Path(Path.cwd(), "version")
VERSION_RES_PATH = Path(Path.cwd(), "version.json")
RELEASE_TIME_PATH = Path(Path.cwd(), "release_time")
RESOURCE_TIME_PATH = Path(Path.cwd(), "res_time")
NOTE_PATH = Path(Path.cwd(), "note.md")


def check_in_progress(token: str) -> bool:
    _GH = github.Github(login_or_token=token, retry=None)
    _REPO = _GH.get_repo("weinibuliu/Maa-Mirror-Script")
    workflows = _REPO.get_workflow_runs().get_page(0)
    workflows.pop(0)  # 排除自身

    for w in workflows:
        if w.status == "in_progress":
            return True
    return False


class MAA:
    def __init__(self, token: str):
        self.token = token
        GH = github.Github(login_or_token=self.token, retry=None)
        self.REPO = GH.get_repo("MaaAssistantArknights/MaaAssistantArknights")

    def get_current_ver(self) -> str | None:
        if not VERSION_PATH.exists():
            return None

        with open(VERSION_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def check(self) -> str | None:
        RELEASE = self.REPO.get_releases().get_page(0)[0]

        curent_ver = self.get_current_ver()

        target_ver = RELEASE.tag_name
        release_time = int(RELEASE.created_at.timestamp())
        note = (
            RELEASE.body.replace(f"## {target_ver}\n\n", "")
            .replace(f"## {target_ver}\n", "")
            .replace("@", "`@`")
        )

        if target_ver != curent_ver:
            with open(VERSION_PATH, "w", encoding="utf-8") as f:
                f.write(target_ver)
            with open(RELEASE_TIME_PATH, "w", encoding="utf-8") as f:
                f.write(str(release_time))
            with open(NOTE_PATH, "w", encoding="utf-8") as f:
                f.write(note)
            return target_ver
        else:
            return None

    def run(self):
        ver = self.check()
        # in_progress = check_in_progress(self.token)
        print(f"Maa Version = {ver}")

        """
        if in_progress:
            print("Cancel because a workflow is in progress.")
            return
        """

        if ver:
            subprocess.run('echo "maa=true" >> "$GITHUB_ENV"', shell=True)
            subprocess.run(f'echo "ver={ver}" >> "$GITHUB_ENV"', shell=True)
            print(f"env.ver = {ver}")


class Resource:
    def __init__(self, token: str):
        self.token = token
        GH = github.Github(login_or_token=self.token, retry=None)
        self.REPO = GH.get_repo("MaaAssistantArknights/MaaAssistantArknights")

    def get_current_ver(self) -> str | None:
        if not VERSION_RES_PATH.exists():
            return None

        with open(VERSION_RES_PATH, "r", encoding="utf-8") as f:
            info: dict = json.load(f)
            ver = info["last_updated"]
            return ver

    def check(self) -> str | None:
        curent_ver = self.get_current_ver()

        target_path = Path(Path.cwd(), "res/resource/version.json")
        with open(target_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
            target_ver = cache["last_updated"]

        if target_ver != curent_ver:
            return target_ver
        else:
            return None

    def run(self):
        ver = self.check()
        # in_progress = check_in_progress(self.token)
        print(f"Resource Version = {ver}")

        """
        if in_progress:
            print("Cancel because a workflow is in progress.")
            return
        """

        if ver:
            subprocess.run('echo "res=true" >> "$GITHUB_ENV"', shell=True)
            subprocess.run(f'echo "res_ver={ver}" >> "$GITHUB_ENV"', shell=True)
            print(f"env.res_ver = {ver}")
