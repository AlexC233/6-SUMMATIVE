from ast import match_case
from tkinter import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Body
import FileManager
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
# xlim = [-1e8 , 1e8]
# ylim = [-1e8, 1e8]

interval, step, xlim, ylim, objects = FileManager.startSettings()

# objects = 100

# Screen change function
def clear():
    # Create a list of all the names of the widgets on screen at the time
    list = root.grid_slaves()
    # Destroy every widget that was in the list to clear the screen
    for i in list:
        i.destroy()

def startScreen():
    def loadWindow():
        pass

    def settingsScreen():
        pass

    clear()

    titleLabel = Label(root, text="Gravity Simulator", font="Helvetica 24")
    titleLabel.place(bordermode=OUTSIDE, x=100, y=100, width=800, height=200)

    startButton = Button(root, text="Start", font="Helvetica 24", command=simulationScreen)
    startButton.place(bordermode=OUTSIDE, x=300, y=300, width=400, height=100)

    loadButton = Button(root, text="Load", font="Helvetica 24", command=loadWindow)
    loadButton.place(bordermode=OUTSIDE, x=300, y=400, width=400, height=100)

    settingsButton = Button(root, text="Settings", font="Helvetica 24", command=settingsScreen)
    settingsButton.place(bordermode=OUTSIDE, x=300, y=500, width=400, height=100)

    quitButton = Button(root, text="Quit", font="Helvetica 24", command=root.quit)
    quitButton.place(bordermode=OUTSIDE, x=300, y=600, width=400, height=100)


def simulationScreen():    
    clear()
    Body.Body.randomBodies(objects, xlim, ylim)

    def update(interval):
        global runtime
        #print(Body.body.instance.__len__())
        runtime += step
        Body.Body.calcAll()
        plot()
        objectsLabel.config(text="Objects: " + Body.Body.instance.__len__().__str__())

        if (runtime > DAY):
            timeElapsed.config(text= '{:.2f}d'.format(runtime/DAY))
        elif (runtime > HOUR):
            timeElapsed.config(text= '{:.2f}h'.format(runtime/HOUR))
        elif (runtime > MINUTE):
            timeElapsed.config(text= '{:.2f}m'.format(runtime/MINUTE))
        else:
            timeElapsed.config(text= '{:.2f}s'.format(runtime))
        
        if controlButton.cget('text') == 'Pause':
            root.after(interval, update, interval)

    def saveWindow():
        FileManager.saveSimulation("test", runtime)

    def control():
        if controlButton.cget('text') == 'Pause':
            controlButton.config(text='Resume')
        elif controlButton.cget('text') == 'Resume' or controlButton.cget('text') == 'Start':
            controlButton.config(text='Pause')

        update(interval)
        # repeat the calcAll function every interval milliseconds
            

    def randomize():
        controlButton.config(text='Start')

        Body.Body.randomBodies(objects, xlim, ylim)
        plot()

        global runtime
        runtime = 0
        timeElapsed.config(text= '0s')

        root.after(interval, lambda:[timeElapsed.config(text= '0s')])

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
            controlButton.config(text= 'Resume')
            #root.after(interval*2, lambda:[controlButton.config(text= 'Pause'), update(interval)])

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
            args.append(np.ceil((i.radius**2*np.pi)/(xlim[1]*ylim[1])*xsize*ysize))
        return args

    def plot():
        figure.clear()

        figure.add_subplot(111, xlim = (xlim[0], xlim[1]), ylim = (ylim[0], ylim[1])).scatter(getXPlots(), getYPlots(), s=getSizes(), marker="o", color="white")
        
        canvas.draw()

    # create a matplotlib figure that is 800x600 pixels and is placed at (0,0)
    figure = mpl.figure.Figure(figsize = [6.4, 6.4], dpi = 100)  
    
    size = figure.get_size_inches() * figure.dpi

    global xsize, ysize

    xsize = size[0]
    ysize = size[1]
    print(xsize, ysize)

    figure.add_subplot(111, xlim = (xlim[0], xlim[1]), ylim = (ylim[0], ylim[1])).scatter(getXPlots(), getYPlots(), s=getSizes(), marker="o", color="white")
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(bordermode=OUTSIDE ,x=0, y=0, width=800, height=800)

    canvas.draw()

    controlButton = Button(root, text="Start", font="Helvetica 24", command=control)
    controlButton.place(bordermode=OUTSIDE, x=800, y=0, width=200, height=100)

    randomizeButton = Button(root, text="Randomize", font="Helvetica 24", command=randomize)
    randomizeButton.place(bordermode=OUTSIDE, x=800, y=100, width=200, height=100)

    speedButton = Button(root, text="1x", font="Helvetica 24", command=speedChange)
    speedButton.place(bordermode=OUTSIDE, x=800, y=200, width=200, height=100)

    timeElapsed = Label(root, text=str(runtime) + "s", borderwidth= 2, relief="ridge", font="Helvetica 24")
    timeElapsed.place(bordermode=OUTSIDE, x=800, y=300, width=200, height=100)

    objectsLabel = Label(root, text="Objects: " + str(objects), borderwidth= 2, relief="ridge", font="Helvetica 24")
    objectsLabel.place(bordermode=OUTSIDE, x=800, y=400, width=200, height=100)

    saveButton = Button(root, text="Save", font="Helvetica 24", command=saveWindow)
    saveButton.place(bordermode=OUTSIDE, x=800, y=500, width=200, height=100)

if __name__ == "__main__":
    # create a 800x600 window
    root = Tk()
    # prevent resizing
    root.resizable(width=False, height=False)
    root.geometry("1000x800")
    root.title("Path")

    startScreen()
    root.mainloop()