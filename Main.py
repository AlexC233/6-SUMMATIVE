from tkinter import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Body
import schedule

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
step = 5
interval = 1
xlim = []
ylim = []

objects = 500

# Screen change function
def clear():
    # Create a list of all the names of the widgets on screen at the time
    list = root.grid_slaves()
    # Destroy every widget that was in the list to clear the screen
    for i in list:
        i.destroy()

def startScreen():

    clear()

    # create a Label widget that is 600x100 pixels and is placed at (100,100)
    titleLabel = Label(root, text="Gravity Simulator", font="Helvetica 24")
    titleLabel.place(bordermode=OUTSIDE ,x=100, y=100, width=600, height=100)

    # create a button called startButton that is 200x100 pixels and is placed at (300, 300)
    startButton = Button(root, text="Start", font="Helvetica 24", command=simulationScreen)
    startButton.place(bordermode=OUTSIDE ,x=300, y=300, width=200, height=100)

    # create a button called quitButton that is 200x100 pixels and is placed at (300, 400)
    quitButton = Button(root, text="Quit", font="Helvetica 24", command=root.quit)
    quitButton.place(bordermode=OUTSIDE ,x=300, y=400, width=200, height=100)

def simulationScreen():    
    clear()
    Body.randomBodies(objects)

    def control():
        if controlButton.config('text')[-1] == 'Pause':
            controlButton.config(text='Resume')
        elif controlButton.config('text')[-1] == 'Resume' or controlButton.config('text')[-1] == 'Start':
            controlButton.config(text='Pause')

            def update(interval):
                global runtime
                #print(Body.body.instance.__len__())
                runtime += step
                Body.body.calcAll()
                plot()

                if (runtime > DAY):
                    timeElapsed.config(text= '{:.2f}d'.format(runtime/DAY))
                elif (runtime > HOUR):
                    timeElapsed.config(text= '{:.2f}h'.format(runtime/HOUR))
                elif (runtime > MINUTE):
                    timeElapsed.config(text= '{:.2f}m'.format(runtime/MINUTE))
                else:
                    timeElapsed.config(text= '{:.2f}s'.format(runtime))
                
                root.after(interval, update, interval)

            update(interval)
            # repeat the calcAll function every interval milliseconds
            

    def randomize():
        pass

    def speedChange():
        pass

    def getPlots():
        args = []
        for i in Body.body.instance:
            args.append(i.xpos)
            args.append(i.ypos)
        return args

    def plot():
        figure.clear()
        figure.add_subplot(111).plot(*getPlots(), marker="o", ms="1")
        # set the x and y limits of the plot
        
        canvas.draw()

    # create a matplotlib figure that is 800x500 pixels and is placed at (0,0)
    figure = mpl.figure.Figure()   
    figure.add_subplot(111).plot(*getPlots(), marker="o", ms="1")
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(bordermode=OUTSIDE ,x=0, y=0, width=800, height=500)
    canvas.draw()

    xlim = figure.get_axes()[0].get_xlim()
    ylim = figure.get_axes()[0].get_ylim()

    # create a button called controlButton that is 200x100 pixels and is placed at (0, 500)
    controlButton = Button(root, text="Start", font="Helvetica 24", command=control)
    controlButton.place(bordermode=OUTSIDE ,x=0, y=500, width=200, height=100)

    # create a button called randomizeButton that is 200x100 pixels and is placed at (200, 500)
    randomizeButton = Button(root, text="Randomize", font="Helvetica 24", command=randomize)
    randomizeButton.place(bordermode=OUTSIDE ,x=200, y=500, width=200, height=100)

    # create a button called speedButton that is 200x100 pixels and is placed at (400, 500)
    speedButton = Button(root, text="1x", font="Helvetica 24", command=speedChange)
    speedButton.place(bordermode=OUTSIDE ,x=400, y=500, width=200, height=100)

    # create a rectangular frame that is 200x100 pixels and is placed at (600, 500)
    frame = Frame(root, borderwidth=1, relief=SUNKEN)
    frame.place(bordermode=OUTSIDE ,x=600, y=500, width=200, height=100)

    # create a Label called timeElapsed that is 200x100 pixels and is placed at (600, 500)
    timeElapsed = Label(root, text=str(runtime) + "s", font="Helvetica 24")
    timeElapsed.place(bordermode=OUTSIDE ,x=600, y=500, width=200, height=100)



if __name__ == "__main__":
    # create a 800x600 window
    root = Tk()
    root.geometry("800x600")
    root.title("Path")

    startScreen()
    root.mainloop()