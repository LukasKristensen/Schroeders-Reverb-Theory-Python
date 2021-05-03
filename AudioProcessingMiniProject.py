import matplotlib.pyplot as plt
import tkinter as tk
import pyaudio
import wave
import threading
import numpy as np
import scipy.io.wavfile


currentThreads = []
playing = False



def matplobLib():
    samplerate, data = scipy.io.wavfile.read("africa-toto.wav", mmap=False )

    print(len(data))
    listHalf = data[:len(data)//2]
    listHalfHalf = data[:len(listHalf)//2]

    emptyarray = []

    for i in listHalfHalf:
        emptyarray.append(i/2)

    emptyarray=np.array(emptyarray)

    plt.figure(1)
    plt.title("Graph for .wav file")
    plt.plot(data)
    plt.plot(listHalf)
    plt.plot(listHalfHalf)
    plt.plot(emptyarray)

    scipy.io.wavfile.write("testing-africa.wav",samplerate,emptyarray.astype(np.dtype('i2')))
    plt.show()


def displayGUI():
    applicationW = tk.Tk()
    applicationW.title("Audio Processing Mini-project - Lukas Kristensen")
    applicationW.wm_minsize(1000, 500)

    testLabel = tk.Label(text="Audio Processing Mini-project 2021 spring")
    playAudio = tk.Button(text="Play original .wav file", width="50", height="10", bg="gray", fg="black")
    stopAudio = tk.Button(text="Stop .wav original", width="50", height="10", bg="gray", fg="black")
    playAudio.bind("<Button-1>", threadStart)
    stopAudio.bind("<Button-1>", threadStop)

    testLabel.pack()
    playAudio.pack()
    stopAudio.pack()
    applicationW.mainloop()


def playWav():
    fileName = "africa-toto.wav"
    wavRead = wave.open(fileName, "rb")
    print("Status: Currently playing",fileName)

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
        print("Status: Stopped. Total threads -",len(currentThreads))


tkinterGUIthread = threading.Thread(target=displayGUI)
tkinterGUIthread.start()
matplobLib()

