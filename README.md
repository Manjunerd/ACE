# ACE — AI Computer-Use Agent

> An AI agent that can actually use your Windows computer.

ACE is a general-purpose AI computer-use assistant for Windows. Instead of relying on predefined commands or hard-coded workflows, ACE observes the user's screen, understands the current state of the computer, decides what action to take, executes it, observes the result, and continues until the task is completed.

You can interact with ACE using text or voice, including **English, Hindi, Telugu, and mixed-language speech**.

---
## How to use
Download the latest release of the zip file,extract the file and run the .exe file 

## ✨ Features

### 🖥️ AI Computer Use

ACE can interact with the Windows desktop using AI-driven decisions.

It can:

- Move and click the mouse
- Double-click and right-click
- Drag objects
- Type text
- Use keyboard shortcuts
- Scroll
- Navigate applications
- Interact with browser interfaces
- Perform multi-step tasks
- Observe the screen after every action
- Dynamically adapt when the screen changes

ACE does **not** rely on a collection of predefined workflows.

The AI decides the next action based on the actual screen.

---

### 👁️ Visual Screen Understanding

ACE continuously uses screenshots as part of its computer-use loop:

```text
User Task
    ↓
Observe Screen
    ↓
AI Understands Screen
    ↓
Choose Action
    ↓
Execute Action
    ↓
Observe New Screen
    ↓
Choose Next Action
    ↓
...
    ↓
Task Completed
