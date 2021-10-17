from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
import sys
import pytesseract
import cv2
import matplotlib
import os



Choice = Tk()
Choice.title("Lucid - Input Data")
Choice.configure(background = '#ffffff')
Choice.config(height = 1600, width = 800)
Choice.state('zoomed')

fileView = Listbox(Choice, font = "Adam")
fileView.place(relx = 0.5, rely = 0)



global filenames
filenames = ['hello', 'hi', 'test']

for i in filenames:
    fileView.insert(i, filenames[i])


Choice.mainloop()
