import requests

from .constants import AGENT_SERVER_URL


class VisionModel:
    def __init__(self):
        self.endpoint = AGENT_SERVER_URL.rstrip("/")

    def next_action(self, task, screenshot_b64, history):
        response = requests.post(
            f"{self.endpoint}/v1/agent/action",
            json={
                "task": task,
                "screenshot": screenshot_b64,
                "history": history[-8:] if history else [],
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["action"]