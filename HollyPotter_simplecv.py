from SimpleCV import *


def main():

    cam = Camera() #initialize the camera
    display = Display() #create a new display to draw images on

    # Image du chapeau
    imHat = Image('C:\Users\Olivier\Pictures\hat-magic.gif')            #Chemin d'acces du chapeau
    imHat=imHat.resize(200,200)                                         #Dimension de l'image
    amask=imHat.colorDistance(color=Color.WHITE).binarize().invert()    # Creationu mask pour supprimer le controur blanc

    wizard_hat=Image("wizard_hat.png")
    # Image du lapin
    imRabbit = Image('C:\Users\Olivier\Pictures\hat-magic-rabbit.gif')
    imRabbit=imRabbit.resize(200,200)
    # Creation du mask pour supprimer le fond vert
    amaskg=imRabbit.colorDistance(color=Color.GREEN).binarize().invert()


    pixColor=Color.RED

    done = False # setup boolean to stop the program
    thresh=35

    # Boucle principalw
    while not display.isDone():
            img=cam.getImage().flipHorizontal()

            # Gestion des evenements

            # Clique Gauche: R?cup?re la couleur de l'objet ? traquer
            if display.mouseLeft:
                    print "Position = "+repr(display.mouseX)+","+repr(display.mouseY)
                    pixColor=img[display.mouseX,display.mouseY]

            # Molette: Augmente ou diminue le Threshold
            if display.mouseWheelDown:
                    if thresh>0:
                            thresh-=1
                            print "Thresh = "+repr(thresh)
            if display.mouseWheelUp:
                    if thresh<255:
                            thresh+=1
                            print "Thresh = "+repr(thresh)

            # Detection du visage
            faces = img.findHaarFeatures("face") # load in trained face file
            if faces:
                face = faces[-1]
                imgWizard= wizard_hat.resize(face.width()+200,face.height()+200) #load the image to super impose and scale it correctly
                mymask = imgWizard.colorDistance(color=Color.WHITE)

                # Place le chapeau
                posWizard=(face.topLeftCorner()[0]-100,face.topLeftCorner()[1]-imgWizard.size()[1]+40)
                img = img.blit(imgWizard, posWizard,alphaMask=mymask)

            # Traitement de l'image source pour r?cup?rer le blob de l'objet recherch?
            # A partir de l'image source, on cr?e une morphologie de type "OPEN"
            # Ensuite on r?cup?re l'ensemble des pixels correspondant ? la couleur recherch?
            # puis on cr?e l'image binaire avec le Threshold
            img2=img.morphOpen().hueDistance(pixColor).binarize(35)

            # Recup?rtion de tous les blobs
            blobs = img2.findBlobs()

            x=img.size()[0]/2-imHat.size()[0]/2
            y=img.size()[1]-imHat.size()[1]

            # Ajout du chapeau
            img=img.blit(imHat,pos=(x,y),alphaMask=amask)
            if blobs:
                    for b in blobs:
                            if b.area()>500:
                                    b.draw(color=Color.PUCE, width=3)
                    #img.sideBySide(img2)
                                    #img.addDrawingLayer(img2.dl())
                                    #img.dl().circle(b.centroid(),10,Color.RED)
                                    #img.dl().text("Position: "+repr(b.centroid()),(0,10),Color.GREEN)
                                    if b.centroid()[0]>x and b.centroid()[0]<x+imHat.size()[0] and b.centroid()[1]>img.size()[1]-imHat.size()[1]:
                                        img=img.blit(imRabbit,pos=(img.size()[0]/2-imRabbit.size()[0]/2,img.size()[1]-imRabbit.size()[1]-150),alphaMask=amaskg)

            # Affichage
            #img3=img.sideBySide(image)
            img.save(display)
    display.quit()

if __name__ == '__main__':
    main()
