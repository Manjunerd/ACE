import threading
from .model import VisionModel
from .operator import WindowsOperator
from .agent import Agent
from .models import AgentState

def run_cli(settings):
    model=VisionModel(settings); operator=WindowsOperator(settings.action_delay)
    def emit(e): print(f"[{e.state.value}] {e.message}")
    def confirm(a): return input(f"CONFIRM {a.name} {a.args}? [y/N] ").lower().startswith("y")
    agent=Agent(settings,model,operator,emit,confirm)
    print("ACE Python. Type a task, 'stop', 'pause', 'resume', or 'quit'.")
    while True:
        task=input("You> ").strip()
        if task.lower()=="quit": break
        if task.lower()=="stop": agent.stop(); continue
        if task.lower()=="pause": agent.pause(); continue
        if task.lower() in {"resume","continue"}: agent.resume(); continue
        if task: threading.Thread(target=agent.run,args=(task,),daemon=True).start()
