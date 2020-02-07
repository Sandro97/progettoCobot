from Tkinter import *
import tkMessageBox
from PIL import Image
from PIL import ImageTk
import cv2
import time
import numpy as np
import math

TITOLO="Scelta oggetto da cercare"
PATH_IMMAGINE="img/sawyer2.png"

class MenuScelta:

    def __init__(self,master):
        #Attributi (la finestra oggetto TK, e la scelta effettuata in radiobutton)
        self.finestra=master
        self.scelta=IntVar()

        #Settate caratteristiche finestra
        master.geometry("800x750")
        master.grid_columnconfigure(0,weight=1)
        master.title("prova")

        #Inserimento titolo
        titolo = Label(self.finestra,text=TITOLO,font=("Helvetica",16))
        titolo.grid(row=0,column=0, pady=20)

    #Metodo per aggiungere l'immagine centrale e riaggiornarla per sostituirla con l'immagine della videocamera, passare un opecv image
    def aggiungiImmagine(self,imm):
        #immagine = Image.open(PATH_IMMAGINE)
        immagine = Image.fromarray(imm)
        #immagine = Image.open(PATH_IMMAGINE)
        immagine.thumbnail([400,400])
        photo = ImageTk.PhotoImage(immagine)
        etichetta2 = Label(self.finestra,image=photo)
        etichetta2.image = photo
        etichetta2.grid(row=1,column=0,pady=20)
        return etichetta2
    #Metodo per aggiungere le scelte del radiobutton, argomento: lista di figure
    def aggiungiScelte(self,figure):
        for figura in figure:
            indice=figure.index(figura)
            #print indice
            Radiobutton(self.finestra, text=figura, variable=self.scelta, value=indice).grid(row=2+indice,pady=10,padx=10, sticky=W)
