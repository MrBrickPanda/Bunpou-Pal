from tkinter import *
from tkinter import ttk
from search_algorithm import wordResults
import MeCab
from timeit import default_timer as timer
from  tokenise import parseSentence
import re

# Creates a class which acts as a base for menus to be created on top of.
class TestingThing(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.title("Bunpou Pal")

        for F in (Menu, Dict, Gramm):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        if 'dict' or 'gramm' in str(frame):
            self.geometry("400x255")
        else:
            self.geometry("200x100")
        frame.tkraise()

class Menu(Frame):
    def __init__(self, parent, controller):
        # Creates various buttons and labels
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Visit Dictionary", command=lambda: controller.show_frame(Dict))
        button1.pack()
        button2 = ttk.Button(self, text="Visit Grammar Explaniner", command=lambda: controller.show_frame(Gramm))
        button2.pack()

class Dict(Frame):
    def __init__(self, parent, controller):
        # Creates various buttons and labels
        Frame.__init__(self, parent)

        self.x = StringVar()
        self.label_1 = Label(self, text="Enter a Word", bg="#333333", fg="white")
        self.entry_1 = Entry(self, textvariable=self.x, width=50)
        self.label_1.grid(row=3, sticky=EW)
        self.entry_1.grid(row=4, column=0, sticky=EW)
        self.but = ttk.Button(self, text="Search", command=lambda :self.outputWord(self.x.get()))  # Note the use of lambda and the x and y variables.
        self.but.grid(row=5, column=0, sticky=EW)
        self.output = Text(self, width = 50, height = 10, wrap = WORD, background = "white")
        self.output.grid(row=6, column=0, sticky = W)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(Menu))
        button1.grid(row=7, column=0, sticky=EW)

    # Function that outputs the search results to the GUI window.
    def outputWord(self, x):
        self.output.delete(0.0, END)
        if x == '':
            self.output.insert(END, 'Please Input a Word')
        else:
            if not wordResults(x):
                # Returns if the word wasn't found in JMdict
                self.output.insert(END, "This search didn't return anything!")
            else:
                for i in wordResults(x):
                    # Strip the result of things that get in the way of readability
                    self.output.insert(END, str(i).strip("[]").strip("}{").replace("'", "") + "\n")

class Gramm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(Menu))
        button1.grid(row=7, column=0, sticky=EW)
        self.x = StringVar()
        self.label_1 = Label(self, text="Enter a Sentence", bg="#333333", fg="white")
        self.entry_1 = Entry(self, textvariable=self.x, width=50)
        self.label_1.grid(row=3, sticky=EW)
        self.entry_1.grid(row=4, column=0, sticky=EW)
        self.but = ttk.Button(self, text="Parse", command=lambda : parseSentence(self.x.get()))  # Note the use of lambda and the x and y variables.
        self.but.grid(row=5, column=0, sticky=EW)


app = TestingThing()
app.mainloop()
