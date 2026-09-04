import sys, threading
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QLabel,QTextEdit,QMessageBox
from .model import VisionModel
from .operator import WindowsOperator
from .agent import Agent
from .voice import LanguageDetector, SpeechRecognizer, TTS

class Bus(QObject):
    event=Signal(object)

class MainWindow(QMainWindow):
    def __init__(self,settings):
        super().__init__(); self.settings=settings; self.setWindowTitle("ACE Python — AI Computer Agent"); self.resize(900,700)
        self.bus=Bus(); self.bus.event.connect(self.on_event)
        self.model=VisionModel(settings); self.operator=WindowsOperator(settings.action_delay); self.tts=TTS(settings); self.lang=LanguageDetector()
        self.agent=Agent(settings,self.model,self.operator,emit=lambda e:self.bus.event.emit(e),confirm=self.confirm)
        root=QWidget(); lay=QVBoxLayout(root)
        self.status=QLabel("READY"); self.activity=QTextEdit(); self.activity.setReadOnly(True)
        self.input=QLineEdit(); self.input.setPlaceholderText("What would you like me to do?")
        run=QPushButton("Start"); stop=QPushButton("Stop"); pause=QPushButton("Pause / Resume"); read=QPushButton("Read Screen")
        run.clicked.connect(self.start); stop.clicked.connect(self.agent.stop); pause.clicked.connect(self.toggle_pause); read.clicked.connect(self.read_screen)
        row=QHBoxLayout(); row.addWidget(self.input); row.addWidget(run); row.addWidget(stop); row.addWidget(pause); row.addWidget(read)
        lay.addWidget(QLabel("AI COMPUTER AGENT")); lay.addWidget(self.status); lay.addWidget(self.activity); lay.addLayout(row); self.setCentralWidget(root)
    def start(self):
        task=self.input.text().strip()
        if task: threading.Thread(target=self.agent.run,args=(task,),daemon=True).start()
    def toggle_pause(self):
        from .models import AgentState
        self.agent.resume() if self.agent.state.value=="PAUSED" else self.agent.pause()
    def confirm(self,a):
        return QMessageBox.question(self,"Confirmation",f"Allow {a.name} with {a.args}?") == QMessageBox.StandardButton.Yes
    def read_screen(self):
        def work():
            self.bus.event.emit(type("E",(),{"state":type("S",(),{"value":"OBSERVING"})(),"message":"Reading screen"})())
            text=self.model.next_action("Read and describe the current screen for the user. Do not output an action; output only the description.",self.agent.capture.grab()[1],[])
            self.bus.event.emit(type("E",(),{"state":type("S",(),{"value":"COMPLETED"})(),"message":text})())
        threading.Thread(target=work,daemon=True).start()
    def on_event(self,e): self.status.setText(e.state.value); self.activity.append(e.message)

def run_gui(settings):
    app=QApplication(sys.argv); w=MainWindow(settings); w.show(); sys.exit(app.exec())
