import os
import random

from PIL import Image, ImageTk
from PIL.ExifTags import TAGS #for converting strings

import tkinter
from tkinter import ttk, filedialog#allows to open files and folders


class App:
    #first method to be runned
    def __init__(self,master):
        self.master = master
        self.drawBoard() #calling drawBoard

#passing all the widget needs for this appp
    def drawBoard(self): 
        self.photo_frame = ttk.Frame(self.master, width=850,height=650)#holds img
        self.photo_frame.pack(side='left',padx=50,fill='x',expand=True)
        self.photo_frame.pack_propagate(False) #avoid auto_resize#pack_propagate is used to avoid shrinkage of frame

        self.content_frame = ttk.Frame(self.master, width=400,height=350)
        self.content_frame.pack(side='left',padx=20,fill='x',expand=True)
        self.content_frame.pack_propagate(False)

        self.image_label = ttk.Label(self.photo_frame)#holds the img
        self.image_label.pack(anchor='sw')

        self.open_button = ttk.Button(self.photo_frame, text='open',command=self.openFolder)
        self.open_button.pack(side='left',anchor='sw')
        
        self.close_button = ttk.Button(self.photo_frame, text='close',command=self.master.destroy)
        self.close_button.pack(side='left',anchor='sw')

        self.back_button = ttk.Button(self.photo_frame, text='<',state='disabled',command=self.moveBackward)
        self.back_button.pack(side='left',anchor='sw')

        self.forward_button = ttk.Button(self.photo_frame, text='>',state='disabled',command=self.moveForward)
        self.forward_button.pack(side='left',anchor='sw')

        self.meta_button = ttk.Button(self.photo_frame, text='meta',state='disabled',command=self.extractMeta)
        self.meta_button.pack(side='left',anchor='sw')

    def openFolder(self):
        #try and catch block is used to throw exception
        try:
            self.folder = filedialog.askdirectory(title='Open a folder',initialdir= 'C:\\Users\\nandh\\OneDrive\\Pictures')
            self.image_list = os.listdir(self.folder)
            self.new_image_list = [img for img in self.image_list if img.endswith('jpg') or img.endswith('JPG') or img.endswith('png') or img.endswith('JPEG') or img.endswith('jpeg')]
            self.loadImage()
            self.forward_button.state(['!disabled'])
            self.meta_button.state(['!disabled'])

        except FileNotFoundError:
            self.pop_up = tkinter.Toplevel(master)
            self.pop_up.title('alert')
            self.pop_up.geometry('225x125+650+300')
            self.pop_up.resizable(False, False)
            self.pop_up.lift(master)

            ttk.Label(self.pop_up, text='operation cancelled', background='light blue').pack(padx=20, pady=25)
            ttk.Button(self.pop_up, text='Ok', command=self.pop_up.destroy).pack(padx=10, pady=5)


    def loadImage(self, image_counter=0):
        self.image_counter = image_counter
        self.image = self.folder + '/' + self.new_image_list[self.image_counter]#folder give path #list gives 1st img in list
        width, height = Image.open(self.image).size

        if width > height:
            self.image_resized = Image.open(self.image).resize((850,550))
        else:
            self.image_resized = Image.open(self.image).resize((450,600))

        self.load_image = ImageTk.PhotoImage(self.image_resized)
        self.image_label.image = self.load_image
        self.image_label.config(image=self.image_label.image)
    def moveForward(self):
        self.clearMeta()
        self.image_counter +=1
        self.loadImage(self.image_counter)
        self.back_button.state(['!disabled'])
        if self.image_counter +1 == len(self.new_image_list):
            self.forward_button.state(['disabled'])

    def moveBackward(self):
        self.clearMeta()
        self.image_counter -=1
        self.loadImage(self.image_counter)
        if self.image_counter == 0:
            self.back_button.state(['disabled'])
        self.forward_button.state(['!disabled'])
        
    def clearMeta(self):
        if self.content_frame.pack_slaves():
            for widget in self.content_frame.pack_slaves():
                widget.destroy()
    
    def extractMeta(self):
        self.clearMeta()
        file = Image.open(self.image)
        data = file.getexif()
        if data:
            for key, val in data.items():
                string = TAGS.get(key)
                labeltext = '{} : {}'.format(string, val)
                ttk.Label(self.content_frame, text=labeltext).pack(anchor='sw',padx=20, pady=3)
        else:
            ttk.Label(self.content_frame, text='no metadata found').pack(anchor='sw',padx=20, pady=3)

if __name__ == '__main__':
    master = tkinter.Tk()
    App(master)
    master.title('Crystal Ball')
    master.geometry('1350x750+125+50')
    master.mainloop()