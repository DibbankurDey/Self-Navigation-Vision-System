try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception:
    engine = None

def speak(text):
    if engine is not None:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    else:
        print(f"[Voice Assistant]: {text}")