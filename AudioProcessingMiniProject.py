import matplotlib.pyplot as plt
import tkinter as tk
import pyaudio
import wave
import threading
import numpy as np
from numpy import random
import scipy.io.wavfile

defaultValues = [["0.10","0.12","0.14","0.16"],["0.2","0.22","0.24","0.26"],["0.30","0.32","0.34","0.36"],["0.40","0.42","0.44","0.46"]]
currentThreads = []

mixingGUI = []
mixingLABEL = []

plainReverbGUI = []
plainReverbLABEL = []

plainReverbAmpGUI = []
plainReverbAmpLABEL = []

allPassGUI = []
allPassLABEL = []

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

def randomPreset():
    for i in range (len(mixingGUI)):
        mixingGUI[i].set(random.rand())
        plainReverbAmpGUI[i].set(random.rand())
        plainReverbGUI[i].set(random.rand())
        allPassGUI[i].set(random.rand())

def standardPresetOne():
    for i in range (len(mixingGUI)):
        mixingGUI[i].set(defaultValues[0][i])
        plainReverbAmpGUI[i].set(defaultValues[1][i])
        plainReverbGUI[i].set(defaultValues[2][i])
        allPassGUI[i].set(defaultValues[3][i])

def getValues():
    storedVals=[[],[],[],[]]

    for i in range(len(mixingGUI)):
        storedVals[0].append(mixingGUI[i].get())
        storedVals[1].append(plainReverbAmpGUI[i].get())
        storedVals[2].append(plainReverbGUI[i].get())
        storedVals[3].append(allPassGUI[i].get())
    print(storedVals)


def displayGUI():
    bgC = "Light gray"

    audioGUIWindow = tk.Tk()
    audioGUIWindow.title("Audio Processing Mini-project - Lukas Kristensen")

    audioGUIWindow.wm_minsize(1000, 500)
    audioGUIWindow.resizable(False,False)

    mixingLabel = tk.Label(text="Mixing parameters")
    plainReverbLabel = tk.Label(text="Plain reverb parameters")
    allPassLabel = tk.Label(text="Allpass parameters")

    playAudio = tk.Button(text="Play original .wav file", width="20", height="5", bg=bgC, fg="black", command=threadStart)
    stopAudio = tk.Button(text="Stop .wav original", width="20", height="5", bg=bgC, fg="black", command=threadStop)
    processAudio = tk.Button(text="Start Processing", width="20", height="5", bg=bgC, fg="black", command="")
    playNewAudio = tk.Button(text="Play new .wav file", width="20", height="5", bg=bgC, fg="black",command="")
    stopNewAudioAudio = tk.Button(text="Stop new .wav original", width="20", height="5", bg=bgC, fg="black", command="")

    defaultPreset = tk.Button(text="Random preset", width="20", height="5", bg=bgC, fg="black", command=randomPreset)
    standardPreset = tk.Button(text="Standard preset", width="20", height="5", bg=bgC, fg="black", command=standardPresetOne)
    getValue = tk.Button(text="GetValues", width="20", height="5", bg=bgC, fg="black", command=getValues)

    s1label = tk.Label(text="s1")
    s2label = tk.Label(text="s2")
    s3label = tk.Label(text="s3")
    s4label = tk.Label(text="s4")
    mixingLABEL.extend([s1label, s2label, s3label,s4label])

    s1scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    s2scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    s3scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    s4scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    mixingGUI.extend([s1scale, s2scale, s3scale,s4scale])

    d1label = tk.Label(text="d1")
    d2label = tk.Label(text="d2")
    d3label = tk.Label(text="d3")
    d4label = tk.Label(text="d4")
    plainReverbLABEL.extend([d1label, d2label, d3label,d4label])

    d1scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d2scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d3scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d4scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    plainReverbGUI.extend([d1scale, d2scale, d3scale,d4scale])

    a1label = tk.Label(text="a1")
    a2label = tk.Label(text="a2")
    a3label = tk.Label(text="a3")
    a4label = tk.Label(text="a4")
    plainReverbAmpLABEL.extend([a1label, a2label, a3label,a4label])

    a1scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    a2scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    a3scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    a4scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    plainReverbAmpGUI.extend([a1scale, a2scale, a3scale,a4scale])

    a5label = tk.Label(text="a5")
    a6label = tk.Label(text="a6")
    d5label = tk.Label(text="d5")
    d6label = tk.Label(text="d6")
    allPassLABEL.extend([a5label, a6label, d5label,d6label])

    a5scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    a6scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d5scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d6scale = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    allPassGUI.extend([a5scale, a6scale, d5scale,d6scale])


    for i in range(len(mixingGUI)):
        # mixingGUI[i].bind("<Button-1>")
        mixingGUI[i].grid(row=(i*2)+1,column=0,pady=10, padx=20,sticky="N")
        mixingLABEL[i].grid(row=(i*2)+2,column=0,pady=0,sticky="N")
    mixingLabel.grid(row = 0, column=0, pady =5)

    for i in range(len(plainReverbGUI)):
        plainReverbGUI[i].grid(row=(i*2)+1,column=1,pady=10,sticky="N")
        plainReverbLABEL[i].grid(row=(i*2)+2,column=1,pady=0,sticky="N")
    plainReverbLabel.grid(row = 0, column=1, pady =5)

    for i in range(len(plainReverbAmpGUI)):
        plainReverbAmpGUI[i].grid(row=(i*2)+1,column=2,pady=10,sticky="N")
        plainReverbAmpLABEL[i].grid(row=(i*2)+2,column=2,pady=0,sticky="N")

    allPassLabel.grid(row = 0, column=3, pady =5)
    for i in range(len(plainReverbAmpGUI)):
        allPassGUI[i].grid(row=(i*2)+1,column=3,pady=10,sticky="N")
        allPassLABEL[i].grid(row=(i*2)+2,column=3,pady=0,sticky="N")

    defaultPreset.grid(row = 11, column=1, pady =40)
    standardPreset.grid(row=11,column=2, pady=40)
    getValue.grid(row=11,column=3,pady=40)


    playAudio.grid(row = 12, column=1, pady =40)
    stopAudio.grid(row = 12, column=2, pady =40)
    processAudio.grid(row = 12, column=3, pady =40)
    playNewAudio.grid(row = 12, column=4, pady =40)
    stopNewAudioAudio.grid(row = 12, column=5, pady =40)

    audioGUIWindow.mainloop()


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


def threadStart():
    holdThreadSize = len(currentThreads)
    currentThreads.append(threading.Thread(target=playWav))
    currentThreads[holdThreadSize].start()


def threadStop():
    if len(currentThreads) != 0:
        currentThreads.pop(len(currentThreads) - 1)
        print("Status: Stopped. Total threads -", len(currentThreads))


tkinterGUIthread = threading.Thread(target=displayGUI)
tkinterGUIthread.start()
matplobLib()

