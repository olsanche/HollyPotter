from SimpleCV import *
import os

class MyObject:

    def setColor(self,color):
        self.m_pixColor=color

    def setImage(self,img):
        self.m_img=img

    def setThresh(self,thresh):
        self.m_thresh=thresh

    def getCentroid(self):
        img2=self.m_img.morphOpen().hueDistance(self.m_pixColor).binarize(self.m_thresh)

        # Recup?rtion de tous les blobs
        blobs = img2.findBlobs()

        if blobs:
            for b in blobs:
                if b.area()>500:
                    b.draw(color=Color.PUCE, width=3)
                    centroid=b.centroid()

        return centroid


    def getRect(self):
        pass


def main():

    cam = Camera() #initialize the camera
    display = Display() #create a new display to draw images on

    mypath=os.path.join(os.getcwd(),"img")
    # Image du chapeau
    imHat = Image(mypath+os.sep+'hat-magic.gif')            #Chemin d'acces du chapeau
    imHat=imHat.resize(200,200)                                         #Dimension de l'image
    amask=imHat.colorDistance(color=Color.WHITE).binarize().invert()    # Creationu mask pour supprimer le controur blanc

    wizard_hat=Image(mypath+os.sep+'wizard_hat.png')
    # Image du lapin
    imRabbit = Image(mypath+os.sep+'hat-magic-rabbit.gif')
    imRabbit=imRabbit.resize(200,200)
    # Creation du mask pour supprimer le fond vert
    amaskg=imRabbit.colorDistance(color=Color.GREEN).binarize().invert()


    pixColor=Color.RED

    done = False # setup boolean to stop the program
    thresh=10
    myObject=MyObject()
    myObject.setColor(pixColor)
    myObject.setThresh(thresh)
    # Boucle principalw
    while not display.isDone():
            img=cam.getImage().flipHorizontal()
            myObject.setImage(img)
            # Gestion des evenements

            # Clique Gauche: R?cup?re la couleur de l'objet ? traquer
            if display.mouseLeft:
                    print "Position = "+repr(display.mouseX)+","+repr(display.mouseY)
                    myObject.setColor(img[display.mouseX,display.mouseY])

            # Molette: Augmente ou diminue le Threshold
            if display.mouseWheelDown:
                    if thresh>0:
                            thresh-=1
                            myObject.setThresh(thresh)
                            print "Thresh = "+repr(thresh)
            if display.mouseWheelUp:
                    if thresh<255:
                            thresh+=1
                            myObject.setThresh(thresh)
                            print "Thresh = "+repr(thresh)

            # Detection du visage
##            imgface=img.scale(0.25)
##            faces = imgface.findHaarFeatures("face") # load in trained face file
##            if faces:
##                face = faces[-1]
##                imgWizard= wizard_hat.resize(face.width()*4+200,face.height()*4+200) #load the image to super impose and scale it correctly
##                mymask = imgWizard.colorDistance(color=Color.WHITE)
##
##                # Place le chapeau
##                posWizard=((face.topLeftCorner()[0])*4-100,(face.topLeftCorner()[1])*4-imgWizard.size()[1]+40)
##                img = img.blit(imgWizard, posWizard,alphaMask=mymask)
##                faceROI=face.crop()


            x=img.size()[0]/2-imHat.size()[0]/2
            y=img.size()[1]-imHat.size()[1]

            # Ajout du chapeau
            img=img.blit(imHat,pos=(x,y),alphaMask=amask)

# Traitement de l'image source pour r?cup?rer le blob de l'objet recherch?
            # A partir de l'image source, on cr?e une morphologie de type "OPEN"
            # Ensuite on r?cup?re l'ensemble des pixels correspondant ? la couleur recherch?
            # puis on cr?e l'image binaire avec le Threshold
            centroid=myObject.getCentroid()

            if centroid[0]>x and centroid[0]<x+imHat.size()[0] and centroid[1]>img.size()[1]-imHat.size()[1]:
                img=img.blit(imRabbit,pos=(img.size()[0]/2-imRabbit.size()[0]/2,img.size()[1]-imRabbit.size()[1]-150),alphaMask=amaskg)
            # Affichage
            #img3=img.sideBySide(image)
            img.save(display)
    display.quit()

if __name__ == '__main__':
    main()
