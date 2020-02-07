import cv2
import numpy as np
import webcolors
import distance

class Imago(object):
    """classe immagine, inizializzata con una foto ed in grado di riconoscere figure e colori."""

# attributi = imgBN / img / contorni / figure / colori / centri / distanza / posM1 / posM2
    def __init__(self, img_path):
        super(Imago, self).__init__()
        self.imgBN = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        self.img = cv2.imread(img_path,1)
        self.figure = []
        self.colori = []
        self.centri = []
        self.contorni = []
        self.distanza = 0

# trova i contorni, elimino quelli troppo piccoli (errori)
    def trova_contorni(self):
        blurred = cv2.GaussianBlur(self.imgBN, (5, 5), 10)
        _, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

            if (cv2.contourArea(cnt) > 10) & (cv2.contourArea(cnt) < self.imgBN.size/2):
                self.contorni.append(cnt)

# identifico le figure e le aggiungo all'attributo figure
    def riconosci_figure(self):
        for cnt in self.contorni:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if len(approx) == 3:
                self.figure.append("triangle")
            elif len(approx) == 4:
                [_,_,altezza,larghezza] = cv2.boundingRect(cnt)
                rapporto = altezza/float(larghezza)
                if (rapporto > 0.95) & (rapporto < 1.05):
                    self.figure.append("square")
                else:
                    self.figure.append("rectangle")
            elif len(approx) == 5:
                self.figure.append("pentagon")
            elif len(approx) == 6:
                self.figure.append("hexagon")
            elif len(approx) == 10:
                self.figure.append("star")
            elif 11 < len(approx) < 15:
                self.figure.append("ellipse")
            else:
                self.figure.append("circle")

# identifico colori e centri(coordinate y e x) e li aggiuno al rispettivo attributo
    def riconosci_colori_centri(self):
        for cnt in self.contorni:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            center = cv2.moments(cnt)
            cx = int(center['m10']/center['m00'])
            cy = int(center['m01']/center['m00'])
            color = self.img[cy,cx]

            colore = self.converti_colore(color)
            self.centri.append((cy,cx))
            self.colori.append(colore)

# converte il colore da bgr nel nome del colore piu vicino
    def converti_colore(self,requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[2]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[0]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]


# metodo riassuntivo che classifica tutti gli elementi dell'immagine per forma e colore
    def elabora(self):
        self.trova_contorni()
        self.riconosci_figure()
        self.riconosci_colori_centri()

# calcola a che distanza sono posizionati gli oggetti in base ad un marker
# (2 cerchi neri a distanza definita)
    def calcola_distanza(self):
        pos1,pos2 = self.trova_marker()
        lun_calcolata = distance.trova_lun_marker(pos1,pos2)
        distanza = distance.dist_camera(lun_calcolata)
        return distanza

# trova le posizioni dei 2 marker
    def trova_marker(self):
        indici = []
        for i in range(len(self.figure)):
            # cerco solo cerchi neri
            col_centro = self.imgBN[self.centri[i]]
            if (self.figure[i] == "circle"):
                indici.append(i)
        self.posM1 = self.centri[indici[0]]
        self.posM2 = self.centri[indici[1]]
        return self.posM1,self.posM2

# trova la distanza sul piano a cui si trova il punto speciicato
# ritorna di quanto ci si deve spostare nella realta rispetto al punto noto (marker1)
    def trova_xy(self,pos):

        # lunghezza vera : distanza vera = lunghezza vista : distanza vista

        # lunghezza vera e' nota a priori
        _, lun_teorica = distance.trova_lun_focale_lun_teorica()
        # lunghezza vista la posso trovare coi centri dei marker
        lun_calcolata = distance.trova_lun_marker(self.posM1,self.posM2)
        # distanza vista e' data dalla posizione dei centri rispetto al punto noto dvi
        ydvi = pos[0] - self.posM1[0]
        xdvi = pos[1] - self.posM1[1]

        y = ydvi*lun_teorica/lun_calcolata
        x = xdvi*lun_teorica/lun_calcolata

        print lun_calcolata

        return x,y
