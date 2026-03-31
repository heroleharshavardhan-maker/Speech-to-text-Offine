import sounddevice as sd
import vosk
import json
import queue
import sys

# Load model
model = vosk.Model("model")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen_offline():
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    print("Listening offline... Say 'stop' to exit. Ctrl+C to force quit.")
    
    with sd.RawInputStream(samplerate=16000,
                           blocksize=8000,
                           dtype='int16',
                           channels=1,
                           callback=callback):
        while True:
            try:
                data = q.get()
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    
                    if text:
                        print("You said:", text)
                        
                        if "stop" in text.lower():
                            print("Stopping...")
                            break
                            
            except KeyboardInterrupt:
                print("Stopped.")
                break

listen_offline()