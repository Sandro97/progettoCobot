#! /usr/bin/env python
from MenuIniziale import *
from MenuScelta import *
from posiziona import posiziona
from Tkinter import *
from Imago import Imago
from camera import camera
import tkMessageBox
import cv2
from PIL import Image           #sudo apt install python-pip
from PIL import ImageTk
# se ImageTk da problemi scrivere nel terminale:
#sudo apt-get install python-imaging python-pil.imagetk


def get_image_callback(img_data):
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(img_data, "bgr8")
    except CvBridgeError, err:
        rospy.logerr(err)
        return
    cv2.imwrite("img/foto.png", cv_image)

#Metodo per prendere l'oggetto cercato
def prendiOggetto(numero,immagine):
    print immagine.centri[numero]
    #vai in posizione corretta
    x,y = immagine.trova_xy(immagine.centri[numero])
    print x,y

def main():
    #Mostra la schermata di benvenuto
    MenuIniziale()

    #Fai partire il posizionamento del robot
    print("Robot vai in posizione")             #rospy.loginfo("Posizionamento robot")
    posiziona()

    cameras = camera()
    cameras.set_callback(camera, get_image_callback, rectify_image=True, callback_args=None)

    #Apri la nuova finestra che mostrera' l'immagine della telecamera
    master=Tk()
    menu=MenuScelta(master)


    path = "img/foto.png"
    #Mostra l'immagine della fotocamera usando il metodo aggiungiImmagine
    imgDaSawyer = cv2.imread(path, 1)
    imgDaSawyer=cv2.cvtColor(imgDaSawyer,cv2.COLOR_BGR2RGB)
    immagine=menu.aggiungiImmagine(imgDaSawyer)     #Per rimuoverla e rimpiazzarla immagine.destroy()

    #Trova le forme che vi sono sul piano creando una lista come in esempio sottostante:
    imma = Imago(path)
    imma.elabora()
    distanza = imma.calcola_distanza()

    #Inseriscile nell'interfaccia grafica
    opzioni = []
    for i in range(len(imma.figure)):
        opzioni.append(imma.colori[i] + " " + imma.figure[i])

    menu.aggiungiScelte(opzioni)

    #Aggiungi il bottone di avvio presa oggetto e all'evento di premuta richiama la funzione che prende l'oggetto
    b = Button(master, text="Prendi oggetto", command= lambda: prendiOggetto(menu.scelta.get(),imma))
    b.grid(row=2+len(opzioni),column=0)

    master.mainloop()


if __name__=="__main__":
    main()
