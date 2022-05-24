from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkcap

import numpy as np
import Body
import FileManager
import VideoMaker

plt.style.use('dark_background')

MINUTE = 60
# Hour in seconds
HOUR = 60 * MINUTE
# Day in seconds
DAY = 24 * HOUR
# Week in seconds
WEEK = 7*DAY
# Month in seconds
MONTH = 30*DAY
# Year in seconds
YEAR = 365*DAY

runtime = 0
# step = 5
interval = 100
frame = 0
# xlim = [-1e8 , 1e8]
# ylim = [-1e8, 1e8]

interval, step, xlim, ylim, objects = FileManager.startSettings()

loadedJSON = None
videoFolder = None

cap = None

# Screen change function


def clear():
    # Create a list of all the names of the widgets on screen at the time
    list = root.grid_slaves()
    # Destroy every widget that was in the list to clear the screen
    for i in list:
        i.destroy()


def startScreen():
    def loadWindow():
        global runtime, loadedJSON, videoFolder, frame

        file = filedialog.askopenfilename(
            initialdir="./simulations/", title="Select file", filetypes=(("json files", "*.json"), ("all files", "*.*")))

        if file != "":
            try:
                try:
                    try:
                        runtime, videoFolder, frame = FileManager.loadSimulation(
                            file)
                    except:
                        runtime, videoFolder = FileManager.loadSimulation(file)
                except:
                    runtime = FileManager.loadSimulation(file)
                loadedJSON = file
                simulationScreen(False)

            except:
                messagebox.showerror(
                    "Error", file + "\nis not a valid simulation file!")

    def settingsScreen():
        pass

    clear()

    titleLabel = Label(root, text="Gravity Simulator", font="Helvetica 24")
    titleLabel.place(bordermode=OUTSIDE, x=100, y=100, width=800, height=200)

    startButton = Button(root, text="Start", font="Helvetica 24",
                         command=lambda: [simulationScreen(True)])
    startButton.place(bordermode=OUTSIDE, x=300, y=300, width=400, height=100)

    loadButton = Button(root, text="Load",
                        font="Helvetica 24", command=loadWindow)
    loadButton.place(bordermode=OUTSIDE, x=300, y=400, width=400, height=100)

    settingsButton = Button(root, text="Settings",
                            font="Helvetica 24", command=settingsScreen)
    settingsButton.place(bordermode=OUTSIDE, x=300,
                         y=500, width=400, height=100)

    quitButton = Button(root, text="Quit",
                        font="Helvetica 24", command=root.quit)
    quitButton.place(bordermode=OUTSIDE, x=300, y=600, width=400, height=100)


def simulationScreen(generate):
    clear()

    if generate:
        Body.Body.randomBodies(objects, xlim, ylim)

    def setTimeLabel():
        if (runtime > DAY):
            timeElapsed.config(text='{:.2f}d'.format(runtime/DAY))
        elif (runtime > HOUR):
            timeElapsed.config(text='{:.2f}h'.format(runtime/HOUR))
        elif (runtime > MINUTE):
            timeElapsed.config(text='{:.2f}m'.format(runtime/MINUTE))
        else:
            timeElapsed.config(text='{:.2f}s'.format(runtime))

    def update(interval):
        global runtime, frame, videoFolder, cap

        if videoFolder != None:
            if frame % 100 == 0:
                FileManager.saveSimulation(
                    loadedJSON, runtime, frame, videoFolder)
                cap.capture(videoFolder + "\\" + str(frame) + ".png")
                VideoMaker.makeVideo(videoFolder)
            frame += 1

        runtime += step
        Body.Body.calcAll()
        plot()
        objectsLabel.config(text="Objects: " +
                            Body.Body.instance.__len__().__str__())

        setTimeLabel()

        if controlButton.cget('text') == 'Pause':
            root.after(interval, update, interval)

    def saveSimulation():
        global frame, videoFolder, loadedJSON
        fileName = filedialog.asksaveasfilename(
            initialdir="./simulations/", title="Save Simulation", filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if fileName != "":
            if videoFolder != None:
                FileManager.saveSimulation(
                    fileName, runtime, frame, videoFolder)
            else:
                FileManager.saveSimulation(fileName, runtime, None, None)
        loadedJSON = fileName

        if not fileName.endswith(".json"):
            fileName += ".json"
        if videoFolder == None:
            recordButton.config(state=NORMAL)

    def saveVideo():
        global videoFolder, loadedJSON
        fileName = filedialog.asksaveasfilename(
            initialdir="./videos/", title="Save Video", filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
        if fileName != "":
            FileManager.saveVideo(fileName, loadedJSON)
        videoFolder = fileName

        if videoFolder != None:
            recordButton.config(state=DISABLED)

    def control():
        if controlButton.cget('text') == 'Pause':
            controlButton.config(text='Resume')
        elif controlButton.cget('text') == 'Resume' or controlButton.cget('text') == 'Start':
            controlButton.config(text='Pause')

        update(interval)

    def randomize():
        controlButton.config(text='Start')

        Body.Body.randomBodies(objects, xlim, ylim)
        plot()

        global runtime
        runtime = 0
        timeElapsed.config(text='0.00s')

        root.after(interval, lambda: [timeElapsed.config(text='0.00s')])

    def speedChange():
        global interval
        match speedButton.cget('text'):
            case '1x':
                speedButton.config(text='2x')
                interval = 50
            case '2x':
                speedButton.config(text='5x')
                interval = 20
            case '5x':
                speedButton.config(text='10x')
                interval = 10
            case '10x':
                speedButton.config(text='100x')
                interval = 1
            case '100x':
                speedButton.config(text='1x')
                interval = 100

        if controlButton.cget('text') == 'Pause':
            controlButton.config(text='Resume')

    # region plot functions
    def getXPlots():
        args = []
        for i in Body.Body.instance:
            args.append(i.xpos)
        return args

    def getYPlots():
        args = []
        for i in Body.Body.instance:
            args.append(i.ypos)
        return args

    def getSizes():
        global xsize, ysize, xlim, ylim
        args = []
        for i in Body.Body.instance:
            args.append(np.ceil((i.radius**2*np.pi) /
                        (xlim[1]*ylim[1])*xsize*ysize))
        return args

    def plot():
        figure.clear()

        figure.add_subplot(111, xlim=(xlim[0], xlim[1]), ylim=(ylim[0], ylim[1])).scatter(
            getXPlots(), getYPlots(), s=getSizes(), marker="o", color="white")

        canvas.draw()
    # endregion

    figure = mpl.figure.Figure(figsize=[6.4, 6.4], dpi=100)

    size = figure.get_size_inches() * figure.dpi

    global xsize, ysize

    xsize = size[0]
    ysize = size[1]

    figure.add_subplot(111, xlim=(xlim[0], xlim[1]), ylim=(ylim[0], ylim[1])).scatter(
        getXPlots(), getYPlots(), s=getSizes(), marker="o", color="white")
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(bordermode=OUTSIDE, x=0, y=0, width=800, height=800)

    canvas.draw()

    controlButton = Button(
        root, text="Start", font="Helvetica 20", command=control)
    controlButton.place(bordermode=OUTSIDE, x=800, y=0, width=200, height=100)

    randomizeButton = Button(root, text="Randomize",
                             font="Helvetica 20", command=randomize)
    randomizeButton.place(bordermode=OUTSIDE, x=800,
                          y=100, width=200, height=100)

    speedButton = Button(
        root, text="1x", font="Helvetica 20", command=speedChange)
    speedButton.place(bordermode=OUTSIDE, x=800, y=200, width=200, height=100)

    timeElapsed = Label(root, text=str(runtime) + "s",
                        borderwidth=2, relief="ridge", font="Helvetica 20")
    setTimeLabel()
    timeElapsed.place(bordermode=OUTSIDE, x=800, y=300, width=200, height=100)

    objectsLabel = Label(root, text="Objects: " + Body.Body.instance.__len__().__str__(),
                         borderwidth=2, relief="ridge", font="Helvetica 20")
    objectsLabel.place(bordermode=OUTSIDE, x=800, y=400, width=200, height=100)

    saveButton = Button(root, text="Save",
                        font="Helvetica 20", command=saveSimulation)
    saveButton.place(bordermode=OUTSIDE, x=800, y=500, width=200, height=100)

    recordButton = Button(root, text="Record",
                          font="Helvetica 20", command=saveVideo)
    if videoFolder != None or loadedJSON == None:
        recordButton.config(state=DISABLED)
    recordButton.place(bordermode=OUTSIDE, x=800, y=600, width=200, height=100)


if __name__ == "__main__":
    # create a 800x600 window
    root = Tk()
    Body.Body.setT(step)
    # prevent resizing
    root.resizable(width=False, height=False)
    root.geometry("1000x800")
    root.title("Gravity Simulator")

    cap = tkcap.CAP(root)

    startScreen()
    root.mainloop()
