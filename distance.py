import cv2
import math

# calcola (e ritorna) la distanza nella stessa udm di lun_teorica
# (lun_calcolata e' in pixel)
def dist_camera(lun_calcolata):
    lun_focale,lun_teorica = trova_lun_focale_lun_teorica()
    dist = (lun_teorica*lun_focale)/lun_calcolata
    return dist

# prende il valore di lun_focale e lun_teorica precedentemente calcolati
def trova_lun_focale_lun_teorica():
    file = open("valori.txt","r")
    lun_focale, lun_teorica = file.readlines()
    file.close()
    return int(lun_focale),int(lun_teorica)

# calcola la distanza focale con un metodo sperimentale, metodo da chiamare solo
# quando si utilizza per la prima volta la fotocamera.
# Salva i valori di lun_focale e lun_teorica
def calibrazione(lun_teorica,dist_teorica):
    marker = trova_lun_marker()
    lun_focale = (marker*dist_teorica)/lun_teorica
    file = open("valori.txt","w")
    file.write(str(lun_focale) + "\n")
    file.write(str(dist_teorica))
    file.close()

# trova la lunghezza del marker, ovvero 2 cerchi neri (in pixel)
#  con in ingresso le 2 posizioni dei centri
def trova_lun_marker(pos1,pos2):
    (y1,x1) = pos1
    (y2,x2) = pos2
    lun_marker =  math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return lun_marker
