from tkinter import *
from tkinter import ttk
from search_algorithm2 import *
# from search_algorithm2 import getKanji
import MeCab
from timeit import default_timer as timer
from  tokenise import parseSentence
import re

# Creates a class which acts as a base for menus to be created on top of.
class Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.title("Bunpou Pal")

        for F in (Menu, Dict, Gramm, Rads):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        if 'dict' in str(frame) or 'gramm' in str(frame):
            self.geometry("600x455")
        elif 'rads' in str(frame):
            self.geometry("945x675")
        else:
            self.geometry("200x150")
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
        button3 = ttk.Button(self, text="Visit Kanji Search by Radical", command=lambda: controller.show_frame(Rads))
        button3.pack()
# for i in range (all the things):
#     square = Square(xcoord * 1 + i, ycoord etc, image = allthethings[i.image])
#     display(square)

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
        self.output = Text(self, width = 75, height = 22, wrap = WORD, background = "white")
        self.output.grid(row=6, column=0, sticky = W)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(Menu))
        button1.grid(row=7, column=0, sticky=EW)

    # Function that outputs the search results to the GUI window.
    def outputWord(self, x):
        self.output.delete(0.0, END)
        if x != '':
            senseParts = wordResults(x)
            if not senseParts:
                # Returns if the word wasn't found in JMdict
                self.output.insert(END, "This search didn't return anything!")
            else:
                meanings = 1
                for i in senseParts:
                    self.output.insert(END, 'Meaning ' + str(meanings) + '\n')
                    meanings += 1
                    for p in i:
                        self.output.insert(END, str(p))
                    self.output.insert(END, '\n')

        else:
            self.output.insert(END, 'Please Input a Word')
            # .strip("[]").strip("}{").replace("'", "").replace('"[', '').replace(']"', '')

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
        self.but = ttk.Button(self, text="Parse", command=lambda : self.showWords(self.x.get()))  # Note the use of lambda and the x and y variables.
        self.but.grid(row=5, column=0, sticky=EW)
        self.output = Text(self, width = 75, height = 22, wrap = WORD, background = "white")
        self.output.grid(row=6, column=0, sticky = W)

    def showWords(self, word):
        self.output.delete(0.0, END)
        wordParts = parseSentence(word)
        if word == '':
            self.output.insert(END, 'Please Input a Word')
        else:
            if not wordParts:
                # Returns if the word wasn't found in JMdict
                self.output.insert(END, "This search didn't return anything!")
            else:
                wordCount = 1
                for i in wordParts:
                    self.output.insert(END, 'Word '+str(wordCount)+'\n')
                    wordCount+=1
                    for x in i:
                        for p in x:
                            self.output.insert(END, p)
                        self.output.insert(END, '\n')
                 
class Rads(Frame):
    def __init__(self, parent, controller):
        radNumb = 0
        self.colourBool = False
        self.pastComp = []
        Frame.__init__(self, parent)
        button1 = Button(self, text="Home", command=lambda: controller.show_frame(Menu))
        button1.grid(row=7, column=0, sticky=EW)
        self.buttons = {}
        self.stroke = {}
        self.rads = getKanji()
        self.compare = set()
        #import all rads and store them in list "rads"
        row = 8
        column = 0
        for rad in self.rads:
            if rad[1] > radNumb:
                self.stroke[rad[1]] = Label(self, text=str(rad[1]), bg="black",  fg="white")
                self.stroke[rad[1]].grid(row=row, column=column, sticky=NSEW)
                column+=1
                radNumb = rad[1]
            rad += ([False], self.rads.index(rad),)
            self.buttons[rad[0]] = Button(self, text=rad[0], command=lambda r = rad: self.pressed(r), width=5, bg='white')
            self.buttons[rad[0]].grid(row=row, column=column, sticky=EW)
            column +=1
            if column == 21:
                column = 0
                row += 1
        self.label = Label(self, text="Test", bg="#333333", fg="white", width=50)
        self.label.grid(row=21, column=0, columnspan=16, sticky=EW)
        self.output = Text(self, width = 50, height = 10, wrap = WORD, background = "white")
        self.output.grid(row=22, column=0, columnspan=16, sticky = N)
    def pressed(self, rad):
        kanjiOutput = ''
        if rad[2][0]:
            self.buttons[rad[0]].configure(bg="white")
            rad[2][0]= False
            self.pastComp.remove(rad[0])
            
        elif not rad[2][0]:
            self.buttons[rad[0]].configure(bg="red")
            rad[2][0] = True
            kanji = getRads(rad[0])
            self.pastComp.append(rad[0])
    
        for i in self.pastComp:
            if len(self.compare) == 0:
                self.compare = getRads(i)
            else:
                self.compare = self.compare.intersection(getRads(i))
                if len(self.compare) == 0:
                    kanjiOutput = 'No Matches'
        if self.compare == set():
            kanjiOutput = ''
        if type(self.compare) != str:
            if kanjiOutput != 'No Matches':
                for i in self.compare:
                    kanjiOutput += i + ' '
                    
        self.output = Text(self, width = 50, height = 10, wrap = WORD, background = "white")
        self.output.grid(row=22, column=0, columnspan=16, sticky = N)
        self.output.insert(END, kanjiOutput)
        self.compare = set()

app = Main()
app.mainloop()
