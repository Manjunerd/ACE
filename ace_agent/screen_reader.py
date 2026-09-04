from .screenshot import ScreenCapture
class ScreenReader:
    def __init__(self,model): self.model=model; self.capture=ScreenCapture()
    def read(self,focus="full"):
        _,shot=self.capture.grab()
        task=f"Describe the current Windows screen concisely for the user. Focus: {focus}. Read important visible text, application/window identity, controls, alerts and useful state. Do not invent content. Return only the concise description."
        return self.model.next_action(task,shot,[])
