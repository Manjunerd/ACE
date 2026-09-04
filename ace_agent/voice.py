import asyncio, re, tempfile, os

class SpeechRecognizer:
    def __init__(self, model_name="small", device="auto", compute_type="auto"):
        self.model=None; self.cfg=(model_name,device,compute_type)
    def _load(self):
        if self.model is None:
            from faster_whisper import WhisperModel
            model,device,compute=self.cfg
            if device=="auto": device="cuda" if self._cuda_available() else "cpu"
            if compute=="auto": compute="float16" if device=="cuda" else "int8"
            self.model=WhisperModel(model,device=device,compute_type=compute)
    def _cuda_available(self):
        try:
            import torch; return torch.cuda.is_available()
        except Exception: return False
    def transcribe(self, path):
        self._load(); segments,info=self.model.transcribe(path, language=None, vad_filter=True, beam_size=5)
        text=" ".join(s.text.strip() for s in segments).strip()
        return text, getattr(info,"language",None)

class LanguageDetector:
    def detect(self,text):
        te=sum('\u0c00'<=c<='\u0c7f' for c in text); hi=sum('\u0900'<=c<='\u097f' for c in text)
        if te and hi: return "mixed-hi-te"
        if te: return "te"
        if hi: return "hi"
        return "en"

class TTS:
    def __init__(self, settings): self.settings=settings
    async def _speak(self,text,voice):
        import edge_tts
        out=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3").name
        await edge_tts.Communicate(text,voice,rate=f"{int((self.settings.speaking_speed-1)*100):+d}%").save(out)
        return out
    def speak(self,text,language="en"):
        if self.settings.tts_provider!="edge": return
        voice={"hi":self.settings.tts_voice_hi,"te":self.settings.tts_voice_te}.get(language,self.settings.tts_voice_en)
        path=asyncio.run(self._speak(text,voice))
        try:
            from playsound import playsound; playsound(path)
        except Exception:
            try: os.startfile(path)
            except Exception: pass
        finally:
            try: os.unlink(path)
            except Exception: pass
