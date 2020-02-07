from Tkinter import *
import tkMessageBox
from PIL import Image
from PIL import ImageTk
import cv2
import time

TITOLO="Sawyer searcher"
PATH_IMMAGINE="img/sawyer2.png"
PATH_FRECCIA="img/arrow.png"

class MenuIniziale:

    def __init__(self):
        #istanzia oggetto di classe Tk
        self.finestra=Tk()
        #Definisci caratteristiche finestra
        self.finestra.geometry("600x650")
        self.finestra.title(TITOLO)
        self.finestra.resizable(False,False)
        self.finestra.grid_columnconfigure(0,weight=1)      #Centra tutti gli elementi

        #Inserisci titolo
        etichetta = Label(self.finestra,text=TITOLO,font=("Helvetica",16))
        etichetta.grid(row=0,column=0,columnspan=2, pady=20)

        #Inserisci immagine del sawyer
        immagine = Image.open(PATH_IMMAGINE)
        immagine.thumbnail([400,500])
        photo = ImageTk.PhotoImage(immagine)
        etichetta = Label(self.finestra,image=photo)
        etichetta.grid(row=1,column=0,columnspan=2)

        #Molstra etichetta
        scritta = Label(self.finestra,text="Procedi con il posizionamento del robot",font=("Helvetica",12))
        scritta.grid(row=2,column=0,padx=50,pady=20,sticky="W")

        #Mostra bottone con freccia
        arrow=Image.open(PATH_FRECCIA)
        size=50,50
        arrow.thumbnail(size)
        bottoneImm = ImageTk.PhotoImage(arrow)
        bottone=Button(image=bottoneImm, command=self.chiudi,height="50",width="50")
        bottone.grid(row=2,column=1,padx=(0,10),sticky=W)

        self.finestra=mainloop()
    def chiudi(self):
        self.finestra.destroy()
