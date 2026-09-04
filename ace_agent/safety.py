import re
RISK=re.compile(r"\\b(delete|remove|erase|overwrite|send|post|publish|purchase|buy|pay|shutdown|restart|format)\\b",re.I)
class Safety:
    def __init__(self,enabled=True): self.enabled=enabled
    def needs_confirmation(self,task,action):
        return self.enabled and bool(RISK.search(task+" "+action.name+" "+str(action.args)))
