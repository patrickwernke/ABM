import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
from tkinter import (Tk, StringVar, Frame, Label, Button, Scale, Entry,
            Canvas, Scrollbar, Text, YES, NO, LEFT, RIGHT, BOTH, TOP, SUNKEN, X,
            Y, W, WORD, NORMAL, DISABLED, HORIZONTAL, END)

class GUI:
    def __init__(self, model, title='PyCX Simulator', interval=0):
        self.model = model
        self.titleText = title
        self.timeInterval = interval
        self.param_entries = {}
        self.statusStr = ""
        self.running = False
        self.currentStep = 0

        self.initGUI()

    def initGUI(self):
        #create root window
        self.rootWindow = Tk()
        self.statusText = StringVar(value=self.statusStr)
        self.setStatusStr("Simulation not yet started")

        self.rootWindow.wm_title(self.titleText)
        self.rootWindow.protocol('WM_DELETE_WINDOW', self.quitGUI)
        self.rootWindow.geometry('550x700')
        self.rootWindow.columnconfigure(0, weight=1)
        self.rootWindow.rowconfigure(0, weight=1)

        self.frameSim = Frame(self.rootWindow)

        self.frameSim.pack(expand=YES, fill=BOTH, padx=5, pady=5, side=TOP)
        self.status = Label(self.rootWindow, width=40, height=3, relief=SUNKEN,
                            bd=1, textvariable=self.statusText)
        self.status.pack(side=TOP, fill=X, padx=1, pady=1, expand=NO)

        self.runPauseString = StringVar()
        self.runPauseString.set("Run")
        self.buttonRun = Button(self.frameSim, width=30, height=2,
                                textvariable=self.runPauseString,
                                command=self.runEvent)
        self.buttonRun.pack(side=TOP, padx=5, pady=5)

        self.buttonStep = Button(self.frameSim, width=30, height=2,
                                 text="Step Once", command=self.stepOnce)
        self.buttonStep.pack(side=TOP, padx=5, pady=5)
        self.buttonReset = Button(self.frameSim, width=30, height=2,
                                  text="Reset", command=self.resetModel)
        self.buttonReset.pack(side=TOP, padx=5, pady=5)

        for param in self.model.params:
            can = Canvas(self.frameSim)
            lab = Label(can, width=25, height=1 + param.count('\n'),
                        text=param, anchor=W, takefocus=0)
            lab.pack(side='left')
            ent = Entry(can, width=11)
            val = getattr(self.model, param)

            ent.insert(0, str(val))
            ent.pack(side='left')
            can.pack(side='top')
            self.param_entries[param] = ent
        if self.param_entries:
            self.buttonSaveParameters = Button(self.frameSim, width=50,
                    height=1, command=self.saveParametersCmd,
                    text="Save parameters to the running model", state=DISABLED)

            self.buttonSaveParameters.pack(side='top', padx=5, pady=5)
            self.buttonSaveParametersAndReset = Button(self.frameSim, width=50,
                    height=1, command=self.saveParametersAndResetCmd,
                    text="Save parameters to the model and reset the model")

            self.buttonSaveParametersAndReset.pack(side='top', padx=5, pady=5)

        can = Canvas(self.frameSim)
        lab = Label(can, width=25, height=1,
                    text="Step visualization delay in ms ", justify=LEFT,
                    anchor=W, takefocus=0)
        lab.pack(side='left')
        self.stepDelay = Scale(can, from_=0, to=max(2000, self.timeInterval),
                               resolution=10, command=self.changeStepDelay,
                               orient=HORIZONTAL, width=25, length=150)
        self.stepDelay.set(self.timeInterval)

        self.stepDelay.pack(side='left')
        can.pack(side='top')

    def setStatusStr(self, newStatus):
        self.statusStr = newStatus
        self.statusText.set(self.statusStr)

    #model control functions

    def changeStepDelay(self, val):
        self.timeInterval = int(val)

    def saveParametersCmd(self):
        for param, entry in self.param_entries.items():
            val = entry.get()
            setattr(self.model, param, int(val))
            # See if the model changed the value (e.g. clipping)
            new_val = getattr(self.model, param)
            if isinstance(new_val, bool):
                new_val = int(new_val)
            entry.delete(0, END)
            entry.insert(0, str(new_val))
        self.setStatusStr("New parameter values have been set")

    def saveParametersAndResetCmd(self):
        self.saveParametersCmd()
        self.resetModel()

    def runEvent(self):
        if not self.running:
            self.running = True
            self.rootWindow.after(self.timeInterval, self.stepModel)
            self.runPauseString.set("Pause")
            self.buttonStep.configure(state=DISABLED)
            if self.param_entries:
                self.buttonSaveParameters.configure(state=NORMAL)
                self.buttonSaveParametersAndReset.configure(state=DISABLED)
        else:
            self.stopRunning()

    def stopRunning(self):
        self.running = False
        self.runPauseString.set("Continue Run")
        self.buttonStep.configure(state=NORMAL)
        self.drawModel()
        if self.param_entries:
            self.buttonSaveParameters.configure(state=NORMAL)
            self.buttonSaveParametersAndReset.configure(state=NORMAL)

    def stepModel(self):
        if self.running:
            if self.model.step() is True:
                self.stopRunning()
            self.currentStep += 1
            self.setStatusStr("Step " + str(self.currentStep))
            self.status.configure(foreground='black')
            self.drawModel()
            self.rootWindow.after(int(self.timeInterval), self.stepModel)

    def stepOnce(self):
        self.running = False
        self.runPauseString.set("Continue Run")
        self.model.step()
        self.currentStep += 1
        self.setStatusStr("Step " + str(self.currentStep))
        self.drawModel()
        if self.param_entries:
            self.buttonSaveParameters.configure(state=NORMAL)

    def resetModel(self):
        self.running = False
        self.runPauseString.set("Run")
        self.model.reset()
        self.currentStep = 0
        self.setStatusStr("Model has been reset")
        self.drawModel()

    def drawModel(self):
        self.model.draw()
        self.canvas.draw()


    def start(self):
        self.model.reset()
        self.model.startdraw()
        self.canvas = FigureCanvasTkAgg(self.model.fig, master=self.rootWindow)
        self.canvas.get_tk_widget().pack()
        self.drawModel()
        self.rootWindow.mainloop()

    def quitGUI(self):
        plt.close('all')
        self.rootWindow.quit()
        self.rootWindow.destroy()
