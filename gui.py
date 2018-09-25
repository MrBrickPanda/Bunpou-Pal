from tkinter import *
from tkinter import ttk
from search_algorithm import wordResults
import MeCab
from timeit import default_timer as timer
import re
# Possible way to approach fixing tokenizing: If a particle by itself is in a sentence, take that particle out and start
# to add the possible word combinations by that.
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
        if 'dict' in str(frame):
            self.geometry("400x255")
        else:
            self.geometry("200x100")
        frame.tkraise()

class Menu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Visit Dictionary", command=lambda: controller.show_frame(Dict))
        button1.pack()
        button2 = ttk.Button(self, text="Visit Grammar Explaniner", command=lambda: controller.show_frame(Gramm))
        button2.pack()

class Dict(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # self.l1 = Label(self, text="Hover over me")
        # self.l2 = Label(self, text="", width=40)
        # self.l1.grid(row=1)
        # self.l2.grid(row=2)
        # self.l1.pack(side="top")
        # self.l2.pack(side="top", fill="x")
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
        # self.label2= Label(self, text='pos test', bg="#333333", fg="white")
        # self.label2.place(x=40, y=200)
        # self.l1.bind("<Enter>", self.on_enter)
        # self.l1.bind("<Leave>", self.on_leave)

    def outputWord(self, x):
        self.output.delete(0.0, END)
        if x == '':
            self.output.insert(END, 'Please Input a Word')
        else:
            if not wordResults(x):
                self.output.insert(END, "This search didn't return anything!")
            else:
                for i in wordResults(x):
                    self.output.insert(END, str(i).strip("[]").strip("}{").replace("'", "") + "\n")

class Gramm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(Menu))
        button1.grid(row=7, column=0, sticky=EW)

app = TestingThing()
app.mainloop()

# 食べる
