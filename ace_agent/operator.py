import sys
import time
import ctypes
import pyautogui
from .models import Action


class WindowsOperator:
    """Execute the small UI-TARS action space on the real Windows desktop.

    Mouse operations use the Win32 API directly on Windows. This avoids
    PyAutoGUI's platform mouse wrapper for the most latency-sensitive actions
    and gives us a predictable implementation for click/drag/scroll.
    Keyboard operations still use PyAutoGUI because it provides a convenient
    cross-platform key-name mapping.
    """

    LEFT_DOWN = 0x0002
    LEFT_UP = 0x0004
    RIGHT_DOWN = 0x0008
    RIGHT_UP = 0x0010
    WHEEL = 0x0800

    def __init__(self, delay=0.2):
        self.delay = delay
        pyautogui.PAUSE = 0.05
        pyautogui.FAILSAFE = True
        self._win32 = sys.platform == "win32"
        self._user32 = ctypes.windll.user32 if self._win32 else None

    def _center(self, bounds):
        return ((bounds[0] + bounds[2]) // 2, (bounds[1] + bounds[3]) // 2)

    def _move(self, x, y):
        if self._win32:
            if not self._user32.SetCursorPos(int(x), int(y)):
                raise OSError(f"SetCursorPos failed for ({x}, {y})")
        else:
            pyautogui.moveTo(x, y)

    def _mouse_event(self, flags, data=0):
        if not self._win32:
            raise RuntimeError("Win32 mouse events are only available on Windows")
        self._user32.mouse_event(flags, 0, 0, int(data), 0)

    def _click(self, x, y, button="left", clicks=1):
        if not self._win32:
            pyautogui.click(
                x,
                y,
                button=button,
                clicks=clicks,
                interval=0.08,
            )
            return

        self._move(x, y)
        if button == "right":
            down, up = self.RIGHT_DOWN, self.RIGHT_UP
        else:
            down, up = self.LEFT_DOWN, self.LEFT_UP

        for index in range(clicks):
            self._mouse_event(down)
            self._mouse_event(up)
            if index + 1 < clicks:
                time.sleep(0.08)

    def _drag(self, start, end):
        sx, sy = self._center(start)
        ex, ey = self._center(end)
        if not self._win32:
            pyautogui.moveTo(sx, sy)
            pyautogui.dragTo(ex, ey, duration=0.35, button="left")
            return

        self._move(sx, sy)
        self._mouse_event(self.LEFT_DOWN)
        time.sleep(0.05)
        self._move(ex, ey)
        time.sleep(0.10)
        self._mouse_event(self.LEFT_UP)

    def _scroll(self, direction):
        if direction in {"up", "down"}:
            amount = 5
            delta = amount if direction == "up" else -amount
            if self._win32:
                self._mouse_event(self.WHEEL, delta * 120)
            else:
                pyautogui.scroll(delta)
            return

        amount = 3
        delta = amount if direction == "right" else -amount
        if self._win32:
            # MOUSEEVENTF_HWHEEL uses dwData for horizontal wheel movement.
            self._user32.mouse_event(0x01000, 0, 0, delta * 120, 0)
        else:
            pyautogui.hscroll(delta)

    def execute(self, action: Action):
        name = action.name
        args = action.args

        if name in {"click", "left_double", "right_single"}:
            x, y = self._center(args["box"])
            button = "right" if name == "right_single" else "left"
            clicks = 2 if name == "left_double" else 1
            self._click(x, y, button=button, clicks=clicks)

        elif name == "drag":
            self._drag(args["start_box"], args["end_box"])

        elif name == "hotkey":
            pyautogui.hotkey(*args["keys"])

        elif name == "type":
            content = args["content"]
            try:
                import pyperclip
                pyperclip.copy(content)
                pyautogui.hotkey("ctrl", "v")
            except Exception:
                pyautogui.write(content, interval=0.002)

        elif name == "scroll":
            self._scroll(args["direction"])

        elif name == "wait":
            time.sleep(5)

        elif name in {"finished", "call_user"}:
            return

        else:
            raise ValueError(f"unsupported action {name}")

        time.sleep(self.delay)
