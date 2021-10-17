from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import sys
import os


os.chdir('C:/Users/zubi_/Desktop/[project_skyfall]/Programming/GUI/Current')

root = Tk()
root.title("Lucid")
root.configure(background = '#ffffff')
root.config(height = 1600, width = 800)
root.state('zoomed')

#if the user chooses Input/Edit/Generate Report, it will be loaded
#current GUI will be closed

def InputData():
    root.destroy()
    import choices.InputData

def EditData():
    root.destroy()
    import choices.EditData

def GenerateReport():
    root.destroy()
    import choices.GenerateReport

inputImage = ImageTk.PhotoImage(Image.open("input.png"))
editImage = ImageTk.PhotoImage(Image.open("edit.png"))
genImage = ImageTk.PhotoImage(Image.open("genreport.png"))
choice1 = Button(root, image = inputImage, command=InputData).place(relx = 0.04, rely = 0, anchor= "n")
choice2 = Button(root, image = editImage, command=EditData).place(relx = 0.115, rely = 0, anchor = "n")
choice3 = Button(root, image = genImage, command = GenerateReport).place(relx = 0.19, rely = 0, anchor = "n")
text = Label(text="Please choose from the following options:", border = 0, font = ("Adam", 40), bg = "white").place(relx=0.5, rely=0.5, anchor='center')

root.mainloop()
