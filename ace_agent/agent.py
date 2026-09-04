import threading, time, traceback
from .models import AgentState, AgentEvent
from .screenshot import ScreenCapture
from .actions import parse_call, normalize
from .safety import Safety

class Agent:
    def __init__(self, settings, model, operator, emit=None, confirm=None):
        self.settings=settings; self.model=model; self.operator=operator; self.emit=emit or (lambda e:None); self.confirm=confirm or (lambda _:True)
        self.capture=ScreenCapture(settings.screenshot_scale); self.safety=Safety(settings.safety_confirmation)
        self.stop_event=threading.Event(); self.pause_event=threading.Event(); self.pause_event.set(); self.state=AgentState.READY
    def _state(self,s,msg): self.state=s; self.emit(AgentEvent(s,msg))
    def stop(self): self.stop_event.set(); self._state(AgentState.STOPPED,"Stopped")
    def pause(self): self.pause_event.clear(); self._state(AgentState.PAUSED,"Paused")
    def resume(self): self.pause_event.set(); self._state(AgentState.READY,"Resumed")
    def run(self, task):
        self.stop_event.clear()
        self.pause_event.set()
        history = []

        self._state(AgentState.UNDERSTANDING, "Understanding task")

        for step in range(self.settings.max_steps):
            if self.stop_event.is_set():
                return

            self.pause_event.wait()

            self._state(AgentState.OBSERVING, "Observing screen")
            _, shot = self.capture.grab()

            self._state(AgentState.THINKING, "Choosing next action")
            raw = self.model.next_action(task, shot, history)

            try:
                action = normalize(parse_call(raw))
            except Exception as e:
                history.append(f"invalid model output: {e}")
                continue

            history.append(f"{action.name} {action.args}")

            # Task completed:
            # show COMPLETED briefly, then leave the agent in WAITING
            # so it is ready for the next task.
            if action.name == "finished":
                self._state(AgentState.COMPLETED, "Task completed")

                # Final operational state after completion
                self._state(
                    AgentState.WAITING,
                    "Waiting for next task"
                )

                return

            if action.name == "call_user":
                self._state(
                    AgentState.FAILED,
                    "Agent needs your help"
                )
                return

            if self.safety.needs_confirmation(task, action):
                self._state(
                    AgentState.CONFIRMATION_REQUIRED,
                    "Confirmation required"
                )

                if not self.confirm(action):
                    self._state(
                        AgentState.STOPPED,
                        "Cancelled by user"
                    )
                    return

            self._state(
                AgentState.ACTING,
                self._activity(action)
            )

            try:
                self.operator.execute(action)

            except Exception as e:
                detail = "".join(
                    traceback.format_exception_only(type(e), e)
                ).strip()

                self.emit(
                    AgentEvent(
                        AgentState.FAILED,
                        f"Action failed: {detail}"
                    )
                )

                self.emit(
                    AgentEvent(
                        AgentState.FAILED,
                        traceback.format_exc().strip()
                    )
                )

                self.state = AgentState.FAILED
                return

        self._state(
            AgentState.FAILED,
            "Maximum agent steps reached"
        )
    def _activity(self,a):
        return {"click":"Clicking","left_double":"Double-clicking","right_single":"Right-clicking","drag":"Dragging","hotkey":"Using shortcut","type":"Typing","scroll":"Scrolling","wait":"Waiting"}.get(a.name,a.name)
