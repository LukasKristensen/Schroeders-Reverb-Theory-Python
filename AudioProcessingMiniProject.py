import matplotlib.pyplot as plt
import tkinter as tk
import pyaudio
import wave
import threading
import numpy as np

currentThreads = []
playing = False


def playWav():
    print("Hello Audio!")
    wavRead = wave.open("africa-toto.wav", "rb")
    pyA = pyaudio.PyAudio()

    frameRate = wavRead.getframerate()

    audioStream = pyA.open(format=pyA.get_format_from_width(wavRead.getsampwidth()),
                           channels=wavRead.getnchannels(),
                           rate=frameRate,
                           output=True)
    data = wavRead.readframes(frameRate)
    while data and len(currentThreads) != 0:
        audioStream.write(data)
        data = wavRead.readframes(frameRate)


def threadStart(event):
    holdThreadSize = len(currentThreads)
    currentThreads.append(threading.Thread(target=playWav))
    currentThreads[holdThreadSize].start()


def threadStop(event):
    if len(currentThreads) != 0:
        currentThreads.pop(len(currentThreads) - 1)


applicationW = tk.Tk()
applicationW.title("Audio Processing Mini-project - Lukas Kristensen")
applicationW.wm_minsize(1000, 500)

testLabel = tk.Label(text="Hello AP Mini Project")
playAudio = tk.Button(text="Play original .wav file", width="50", height="10", bg="gray", fg="black")
stopAudio = tk.Button(text="Stop .wav original", width="50", height="10", bg="gray", fg="black")
playAudio.bind("<Button-1>", threadStart)
stopAudio.bind("<Button-1>", threadStop)

testLabel.pack()
playAudio.pack()
stopAudio.pack()

applicationW.mainloop()
