from tkinter import *
import tkinter as tk
from PIL import ImageTk
import PIL.Image
from tkinter import ttk
import sys
##
##class choiceGUI:
##    def __init__(self, Choice):
##        Choice.title("Lucid")
##        Choice.configure(background = '#ffffff')
##        Choice.config(height = 1600, width = 800)
##        Choice.state('zoomed')
##
##        def InputData():
##            Choice.destroy()
##            import InputData
##
##        def EditData():
##            Choice.destroy()
##            import EditData
##
##        def GR():
##            Choice.destroy()
##            import GenerateReport
##
##        inputImage = ImageTk.PhotoImage(Image.open("input.png"))
##        editImage = ImageTk.PhotoImage(Image.open("edit.png"))
##        genImage = ImageTk.PhotoImage(Image.open("genreport.png"))
##
##        choice1 = Button(Choice, image = inputImage, width = 100, height = 40, command=InputData)
##        choice1.place(relx = 0.04, rely = 0, anchor= "n")
##
##
##        choice2 = Button(Choice, image = editImage, width = 100, height = 40, command=EditData)
##        choice2.place(relx = 0.115, rely = 0, anchor = "n")
##
##        choice3 = Button(Choice, image = genImage, width = 100, height = 40, command=GR)
##        choice3.place(relx = 0.19, rely = 0, anchor = "n")
##
##
##
##
##Choice = tk.Tk()
##choiceGUI(Choice)
##Choice.mainloop()







from tkinter import *

class choices(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):
        
        def InputData():
            Choice.destroy()
            import InputData

        def EditData():
            Choice.destroy()
            import EditData

        def GR():
            Choice.destroy()
            import GenerateReport

        inputImage = ImageTk.PhotoImage(PIL.Image.open("input.png"))
        editImage = ImageTk.PhotoImage(PIL.Image.open("edit.png"))
        genImage = ImageTk.PhotoImage(PIL.Image.open("genreport.png"))

        self.pack(fill=BOTH, expand=1)
        
        choice1 = Button(self, image = inputImage, width = 100, height = 40, command=InputData)
        choice1.place(relx = 0.04, rely = 0, anchor= "n")


        choice2 = Button(self, image = editImage, width = 100, height = 40, command=EditData)
        choice2.place(relx = 0.115, rely = 0, anchor = "n")

        choice3 = Button(self, image = genImage, width = 100, height = 40, command=GR)
        choice3.place(relx = 0.19, rely = 0, anchor = "n")

root = Tk()

#size of the window
root.geometry("1600x800")
root.state('zoomed')

app = choices(root)
root.mainloop()  
##
