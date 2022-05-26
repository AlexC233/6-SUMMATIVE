from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    messagebox.showerror("matplotlib not installed!",
                         "Please install matplotlib by running \n\"python -m pip install -U matplotlib\" in your terminal.")
    exit()

try:
    import numpy as np
except ImportError:
    messagebox.showerror("numpy not installed!",
                         "Please install numpy by running \n\"python -m pip install -U numpy\" in your terminal.")
    exit()

try:
    import tkcap
except ImportError:
    messagebox.showerror("tkcap not installed!",
                         "Please install tkcap by running \n\"python -m pip install -U tkcap\" in your terminal.")
    exit()

import Body
import FileManager

try:
    import VideoMaker
except ImportError:
    messagebox.showerror("opencv-python not installed!",
                         "Please install VideoMaker by running \n\"python -m pip install -U opencv-python\" in your terminal.")
    exit()

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

interval = 100
frame = 0

interval, step, xlim, ylim, objects = FileManager.startSettings()

loadedJSON = None
videoFolder = None

cap = None


def clear():
    """Screen change function"""
    # Create a list of all the names of the widgets on screen at the time
    list = root.grid_slaves()
    # Destroy every widget that was in the list to clear the screen
    for i in list:
        i.destroy()


def startScreen():
    """Function containing the starting screeen"""
    def loadWindow():
        """Function for loading a simulation file"""
        global runtime, loadedJSON, videoFolder, frame

        file = filedialog.askopenfilename(
            initialdir="./simulations/", title="Select file", filetypes=(("json files", "*.json"), ("all files", "*.*")))

        # Pressing cancel returns an empty string, so we need to check for that
        if file != "":
            # Depending on whether a recording is in progress, the loadSimulation will return different values
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

    def infoScreen():
        """Function for displaying information about the program"""
        info = messagebox.showinfo("Info", "This is a n-body simulation program.\n\nIt simulates 500 random objects of near Earth attributes.\n\nTo record a simulation, first save the simulation, then press the record button. The recording cannot be paused once started.\n\nTo load a simulation, first press the load button, then select the simulation file.\n\nTo start a new simulation, press the new button.\n\nTo exit the program, press the exit button.")

    clear()

    # Setting up the components of the start screen
    titleLabel = Label(root, text="Gravity Simulator", font="Helvetica 24")
    titleLabel.place(bordermode=OUTSIDE, x=100, y=100, width=800, height=200)

    startButton = Button(root, text="Start", font="Helvetica 24",
                         command=lambda: [simulationScreen(True)])
    startButton.place(bordermode=OUTSIDE, x=300, y=300, width=400, height=100)

    loadButton = Button(root, text="Load",
                        font="Helvetica 24", command=loadWindow)
    loadButton.place(bordermode=OUTSIDE, x=300, y=400, width=400, height=100)

    infoButton = Button(root, text="Info",
                        font="Helvetica 24", command=infoScreen)
    infoButton.place(bordermode=OUTSIDE, x=300,
                     y=500, width=400, height=100)

    quitButton = Button(root, text="Quit",
                        font="Helvetica 24", command=root.quit)
    quitButton.place(bordermode=OUTSIDE, x=300, y=600, width=400, height=100)


def simulationScreen(generate):
    """Function for the simulation screen
    generate: Boolean value for whether the simulation should generate 500 random objects or not"""
    clear()

    if generate:
        Body.Body.randomBodies(objects, xlim, ylim)

    def setTimeLabel():
        """Function for setting the time label
        This function rounds the time to two decimal places and changes units to days, hours, minutes, and seconds as appropriate"""
        if (runtime > DAY):
            timeElapsed.config(text='{:.2f}d'.format(runtime/DAY))
        elif (runtime > HOUR):
            timeElapsed.config(text='{:.2f}h'.format(runtime/HOUR))
        elif (runtime > MINUTE):
            timeElapsed.config(text='{:.2f}m'.format(runtime/MINUTE))
        else:
            timeElapsed.config(text='{:.2f}s'.format(runtime))

    def update(interval):
        """Function for updating the simulation
        interval: The interval between frames in milliseconds"""
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
        """Function for calling the save simulation function when the save button is pressed"""
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
        """Function for starting the recording of a video when the record button is pressed"""
        global videoFolder, loadedJSON
        fileName = filedialog.asksaveasfilename(
            initialdir="./videos/", title="Save Video", filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
        if fileName != "":
            FileManager.saveVideo(fileName, loadedJSON)
        videoFolder = fileName

        if videoFolder != None:
            recordButton.config(state=DISABLED)

    def control():
        """Function for starting and stopping the simulation when the control button is pressed"""
        if controlButton.cget('text') == 'Pause':
            controlButton.config(text='Resume')
        elif controlButton.cget('text') == 'Resume' or controlButton.cget('text') == 'Start':
            controlButton.config(text='Pause')

        update(interval)

    def randomize():
        """Function for randomizing the simulation when the randomize button is pressed"""
        controlButton.config(text='Start')

        Body.Body.randomBodies(objects, xlim, ylim)
        plot()

        global runtime
        runtime = 0
        timeElapsed.config(text='0.00s')

        root.after(interval, lambda: [timeElapsed.config(text='0.00s')])

    def speedChange():
        """Function for changing the speed of the simulation when the speed button is clicked"""
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
        """Function for getting the x coordinates of all the objects"""
        args = []
        for i in Body.Body.instance:
            args.append(i.xpos)
        return args

    def getYPlots():
        """Function for getting the y coordinates of all the objects"""
        args = []
        for i in Body.Body.instance:
            args.append(i.ypos)
        return args

    def getSizes():
        """Function for getting the sizes of all the objects"""
        global xsize, ysize, xlim, ylim
        args = []
        for i in Body.Body.instance:
            args.append(np.ceil((i.radius**2*np.pi) /
                        (xlim[1]*ylim[1])*xsize*ysize))
        return args

    def plot():
        """Function for plotting the objects"""
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

    # https://stackoverflow.com/a/50596988
    root.eval('tk::PlaceWindow . center')

    window_height = 800
    window_width = 1000

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width,
                  window_height, x_cordinate, y_cordinate))

    cap = tkcap.CAP(root)

    startScreen()
    root.mainloop()
