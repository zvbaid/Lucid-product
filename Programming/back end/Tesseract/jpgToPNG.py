from PIL import Image
from os import listdir
from os.path import splitext

target_directory = input("Please specify a directory of images")
target = '.png'

for image in listdir(target_directory):
    
