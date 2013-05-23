#-------------------------------------------------------------------------------
# Name:        OliPotter
# Purpose:
#
# Author:      Olivier
#
# Created:     01-03-2013
# Copyright:   (c) Olivier 2013

#-------------------------------------------------------------------------------

# Importation des modules
import cv2
import pygame
import numpy as np
from pygame.locals import *
from PIL import Image
import sys

##########################################################################

##  Classe DataWebcam:
##  Cette classe sert ? faire la communication entre l'image Opencv et Pygame

##########################################################################
class DataWebcam:

    ## D?finit la couleur recherch?e
    def setColor(self,pos):
        self.color=[0,0,0]
        hsv=cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
        #hsv=self.img
        self.color[0]=hsv[pos[1],pos[0]][0]
        self.color[1]=hsv[pos[1],pos[0]][1]
        self.color[2]=hsv[pos[1],pos[0]][2]

    # Initialisation de la classe
    def __init__(self):
        self.cam=cv2.VideoCapture(0)    # Initialise la webcam
        self.color=[0,0,0]
        self.centroid_x=0
        self.centroid_y=0
        #cv2.namedWindow("Principale")
        #cv2.namedWindow("Bin")

##    Retourne le centre de l'objet recherch? sous la forme d'un Tuple
    def get_centroid(self):

        # Threshold
        _thresh=75

        # Operation de Morphologie pour limiter le bruit de la Webcam
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        imgMorph=cv2.morphologyEx(self.img,cv2.MORPH_OPEN,kernel)

        # Transformation de l'image de l'image en HSV pour r?duire l'impacte de la luminosit?
        hsv=cv2.cvtColor(imgMorph,cv2.COLOR_BGR2HSV)

        # Creation de l'image binaire en d?finissant la plage de couleur ? selectionner
        imgBin=cv2.inRange(hsv,
                np.array((self.color[0]-_thresh,self.color[1]-_thresh,self.color[2]-_thresh)),
                np.array((self.color[0]+_thresh,self.color[1]+_thresh,self.color[2]+_thresh)))

        # On recherche les contours puis on calcul le centre de gravit? de chaque contour
        contours, hierarchy = cv2.findContours(imgBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # On ne selectionne que les contours dont la surface est > ? 1000 pixel pour
            # ne garder que l'objet principal
            if cv2.contourArea(cnt)>1000:
                #approx = cv2.approxPolyDP(cnt,3,True)
                #cv2.polylines(self.img,[approx],True,(255,255,0))

                # Retourne le centre de gravit? de l'objet
                M = cv2.moments(cnt)
                self.centroid_x = int(M['m10']/M['m00'])
                self.centroid_y = int(M['m01']/M['m00'])

                return (self.centroid_x,self.centroid_y)

    ## Retourne l'image ?u format IPL pour la g?rer dasn pygame
    def get_image(self):
        result , self.img=self.cam.read()


        # Fait un flip de l'image
        self.img=cv2.flip(self.img,1)

        #cv2.circle(self.img,(self.centroid_x,self.centroid_y),2,(0,0,255),2)

        #drawContours(self.img,contours,-1,(255,0,0),3)
       # cv2.imshow("Principale",self.img)
        #cv2.imshow("Bin",imgBin)

        #convert numpy array to PIL image
        img_rgb=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        img_rgb = np.array(img_rgb)
        return Image.fromarray(img_rgb)


def main():
    pygame.init()

    sizeInit=(width,height)=(640,480)

    disp=pygame.display.set_mode(sizeInit)
    webcam=DataWebcam()

    screen = pygame.display.get_surface()


    # Image du chapeau
    imHat=pygame.image.load('hat-magic.gif').convert()
    imHat=pygame.transform.scale(imHat,(200,200))

    # Image du lapin
    imRabbit=pygame.image.load('hat-magic-rabbit.gif').convert()
    imRabbit=pygame.transform.scale(imRabbit,(200,200))

    while(1): #Boucle d'?v?nements
        for event in pygame.event.get(): #parcours de la liste des ?v?nements
                if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #interrompt la boucle si n?cessaire
                    pygame.quit()
                    sys.exit(0)
                # Clique gauche: Definit la couleur a rechercher
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    webcam.setColor(event.pos)

        # Recupere l'image de la webcam dans la fen?tre Pygame
        im=webcam.get_image()
        pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)

        # Affiche l'image de la webcam

        screen.blit(pg_img, (0,0))
        # Affiche l'image du chapeau en bas au centre
        screen.blit(imHat,(width/2-imHat.get_width()/2,height-imHat.get_height()))

        # Si le centre de l'objet se trouve dans la surface du chapeau, on affiche le lapin
        if webcam.get_centroid():
            # Test de la position
            if webcam.get_centroid()[0]>width/2-imHat.get_width()/2 and webcam.get_centroid()[0]<width/2+imHat.get_width()/2 and webcam.get_centroid()[1]>height-imHat.get_height():
                screen.blit(imRabbit,(width/2-imHat.get_width()/2,height-imHat.get_height()-150))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
