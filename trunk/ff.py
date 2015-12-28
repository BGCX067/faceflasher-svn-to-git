import pygame
import imp, sys, time, os, ConfigParser, random

from pygame.locals import *
#from config import *
from colors import *

def printHelp():
    print("faceFlasher v0.2")
    print("Usage: python faceFlasher.py experimentdatei.dat [CONFIGFILE.ini] \n")
    
def loadControlFile(strFile):
    datFile = open(strFile, "r")
    lineNo = 1
    lstLine = []
    for tmpLine in datFile:
        lstLine.append(tmpLine.rstrip())
    return lstLine

def checkControlFile(lstLine):
    lineNo = 1
    ret = True
    for line in lstLine:
        col = line.split("\t")        
        if(len(col)<3):
            print("Fehler in Steuerdatei!\nZeile "+str(lineNo)+": Eine Zeile muss aus mindestens 3 Spalten bestehen!")
            ret = False
        if(len(col)>4):
            print("Fehler in Steuerdatei!\nZeile "+str(lineNo)+": Eine Zeile darf nicht aus mehr als 5 Spalten bestehen!")
            ret = False
        #if(not os.path.exists("images/"+col[0]+".gif") or not os.path.exists("images/"+col[1]+".gif")):
        #    print("Fehler in Steuerdatei!\nZeile "+str(lineNo)+": Bilddatei existiert nicht!")
        #    ret = False
        lineNo+=1
    return ret

def loadImageFromFile(strImg):    
    """strImgAbs = conf["imgDir"]+"/"+strImg+".gif"
    image = pygame.image.load(strImgAbs).convert()
    return image"""
   
    for type in conf["imgFileType"]:
        strImgAbs = conf["imgDir"]+"/"+strImg+"."+type
        if(os.path.isfile(strImgAbs)):
            image = pygame.image.load(strImgAbs).convert()
            return image            
    return None

def loadImage(strImg):
    return images[strImg]
    
def preLoadImages(lstLine):
    image = {}
    for line in lstLine:
        col = line.split("\t")
        if(col[0] != "!"):
            img = loadImageFromFile(col[0])
            image[col[0]] = scaleImage(img)
        if(col[1] != "!"):
            img = loadImageFromFile(col[1])            
            image[col[1]] = scaleImage(img)
        if(col[2] != "!"):
            img = loadImageFromFile(col[2])            
            image[col[2]] = scaleImage(img)
    return image
        
def scaleImage(image):
    if(conf["imgScale"] != 1.0):
        image = pygame.transform.scale(image,(int(image.get_rect().width*conf["imgScale"]), int(image.get_rect().height*conf["imgScale"])))
    return image

def displayLineImages(img1,img2,img3,surface):
    infoObj = pygame.display.Info()
    
    image = loadImage(images.keys()[0])
    if(conf["imgCenter"]):                
        conf["imgTop"] = (infoObj.current_h - image.get_rect().height)/2
        conf["imgLeft"] = infoObj.current_w/2 - conf["imgDist"]/2 - image.get_rect().width - image.get_rect().width/2
    
	if(conf["randomize"]):
            rand = random.randint(0,1)
            if(rand == 1):
                _img = img1
                img1 = img3
                img3 = _img
        

    #Stimuluspraesentatation    
    if(not img1 == "!"):        
        image = loadImage(img1)
        if(not image):
            print("Fehler in Steuerdatei!\nBilddatei \""+img1+"\" existiert nicht!")
            pygame.quit()
            sys.exit(1)
        else:
            #image = scaleImage(image)
            if(conf["imgCenter"]):                
                conf["imgTop"] = (infoObj.current_h - image.get_rect().height)/2
                conf["imgLeft"] = infoObj.current_w/2 - conf["imgDist"]/2 - image.get_rect().width - image.get_rect().width/2
            surface.blit(image, (conf["imgLeft"],conf["imgTop"]))
            
    if(not img2 == "!"):        
            image = loadImage(img2)
            if(not image):
                print("Fehler in Steuerdatei!\nBilddatei \""+img2+"\" existiert nicht!")
                pygame.quit()
                sys.exit(1)
            else:
                #image = scaleImage(image)
                img2Top = conf["imgTop"]              
                if(conf["imgCenter"]):
                    img2Left = infoObj.current_w/2 - image.get_rect().width/2
                else:
                    img2Left = conf["imgLeft"] + image.get_rect().width + conf["imgDist"]
                surface.blit(image, (img2Left,img2Top))

    if(not img3 == "!"):        
            image = loadImage(img3)
            if(not image):
                print("Fehler in Steuerdatei!\nBilddatei \""+img3+"\" existiert nicht!")
                pygame.quit()
                sys.exit(1)
            else:
                #image = scaleImage(image)
                img3Top = conf["imgTop"]              
                if(conf["imgCenter"]):
                    img3Left = infoObj.current_w/2 + image.get_rect().width/2 + conf["imgDist"]/2
                else:
                    img3Left = conf["imgLeft"] + 2*(image.get_rect().width + conf["imgDist"])
                surface.blit(image, (img3Left,img3Top))
 
def getImgRectList():
    img1Rect = img2Rect = img3Rect = pygame.Rect(0,0,0,0)
    if(conf["imgCenter"]):
        imgTop = (conf["screenHeight"] - conf["imgHeight"])/2
        img1Left = conf["screenWidth"]/2 - conf["imgDist"]/2 - conf["imgWidth"]
        img1Rect = pygame.Rect(img1Left-50,imgTop-50,conf["imgWidth"] + 50,conf["imgHeight"]+50)
        img2Left = conf["screenWidth"]/2 + conf["imgDist"]/2
        img2Rect = pygame.Rect(img2Left-50,imgTop-50,conf["imgWidth"] + 50,conf["imgHeight"]+50)
    else:
        img2Left = conf["imgLeft"] + conf["imgWidth"] + conf["imgDist"]
        print "img2left"+str(img2Left);
        img1Rect = pygame.Rect(conf["imgLeft"]- 50,conf["imgTop"] - 50,conf["imgWidth"]+50,conf["imgHeight"]+100)
        img2Rect = pygame.Rect(img2Left-50,conf["imgTop"]-50,conf["imgWidth"]+50,conf["imgHeight"]+100)
    lstRect = []
    lstRect.append(img1Rect)
    lstRect.append(img2Rect)
    return lstRect

def clearDisplay(surface):
    #surface.fill(conf["bgColor"])
    #background = pygame.Surface(surface.get_size())
    #background = background.convert()
    #background.fill((255, 255, 255))
    infoObj = pygame.display.Info()
    # workaround

    ###if(conf["imgCenter"]):
    ###    top = (infoObj.current_h - conf["imgHeight"])/2 - 50
    ###    left = infoObj.current_w/2 - conf["imgDist"]/2 - conf["imgWidth"] - conf["imgWidth"]/2 - 50
    ###else:
    ###    top = conf["imgTop"]
    ###    left = conf["imgLeft"]

    ###rect = pygame.Rect(top,left,3*conf["imgWidth"]+2*conf["imgDist"]+20,conf["imgHeight"]+20)
    ###pygame.draw.rect(surface,conf["bgColor"],rect)
    rect = pygame.Rect(0,0,infoObj.current_w,infoObj.current_h)
    pygame.draw.rect(surface,conf["bgColor"],rect)
    
    ##lstRect = getImgRectList()
    ##pygame.draw.rect(surface,conf["bgColor"],lstRect[0])
    ##pygame.draw.rect(surface,conf["bgColor"],lstRect[1])    
    #pygame.display.update(lstRect)    
    

def drawCross(surface):
    if(conf["crossVisible"]):
        if(conf["crossCenter"]):
            infoObject = pygame.display.Info()
            w = infoObject.current_w
            h = infoObject.current_h
            pygame.draw.line(surface,conf["crossColor"],[w/2-(conf["crossLineLength"]/2), h/2],[w/2+(conf["crossLineLength"]/2),h/2],conf["crossLineWidth"])
            pygame.draw.line(surface,conf["crossColor"],[w/2, h/2-(conf["crossLineLength"]/2)],[w/2,h/2+(conf["crossLineLength"]/2)],conf["crossLineWidth"])
        else:
            pygame.draw.line(surface,conf["crossColor"],[conf["crossPosX"]-(conf["crossLineLength"]/2), conf["crossPosY"]],[conf["crossPosX"]+(conf["crossLineLength"]/2),conf["crossPosY"]],conf["crossLineWidth"])
            pygame.draw.line(surface,conf["crossColor"],[conf["crossPosX"], conf["crossPosY"]-(conf["crossLineLength"]/2)],[conf["crossPosX"],conf["crossPosY"]+(conf["crossLineLength"]/2)],conf["crossLineWidth"])    

def getImgDim(strImage):
    image = loadImageFromFile(strImage)
    arrImgDim = []
    arrImgDim.append(image.get_rect().width * conf["imgScale"])
    arrImgDim.append(image.get_rect().height * conf["imgScale"])
    return arrImgDim

def getFramesInMs(frames):
    ms = float(1000) / float(conf['frameRate']) * float(frames)
    return ms
    

def loadConfFile(file):
    global conf
    conf = {}    
    cp = ConfigParser.ConfigParser()
    cp.read(file)
    conf['frameRate']  = cp.getint("general","frameRate")
    conf['si']  = cp.getint("general","stimulusInterval")
    conf['isi'] = cp.getint("general","interStimulusInterval")
    conf["repetitions"] = cp.getint("general","repetitions")
    conf["bgColor"] = colors[cp.get("general","backgroundColor")]
    conf["imgDir"] = cp.get("images","directory")
    conf["imgDist"] = cp.getint("images","imageDistance")
    conf["imgCenter"] = cp.getboolean("images","verticalCenter")
    conf["imgScale"] = cp.getfloat("images","scale")
    conf["imgLeft"] = cp.getint("images","posX")
    conf["imgTop"] = cp.getint("images","posY")
    conf["randomize"] = cp.getboolean("images","randomize")
    conf["crossVisible"] = cp.getboolean("fixationCross","visible")
    conf["crossColor"] = colors[cp.get("fixationCross","color")]
    conf["crossCenter"] = cp.getboolean("fixationCross","center")
    conf["crossPosX"] = cp.getint("fixationCross","posX")
    conf["crossPosY"] = cp.getint("fixationCross","posY")
    conf["crossLineLength"] = cp.getint("fixationCross","lineLength")
    conf["crossLineWidth"] = cp.getint("fixationCross","lineWidth")
    infoObj = pygame.display.Info()
    conf["screenHeight"] = infoObj.current_h
    conf["screenWidth"] = infoObj.current_w
    # add image filetype to conf
    conf["imgFileType"] = ["jpg","JPG","jpeg","Jpeg","gif","GIF","Gif","png","PNG","png","BMP","bmp"]

def setConfImgDim(arrImgDim):
    conf["imgWidth"] = arrImgDim[0]
    conf["imgHeight"] = arrImgDim[1]

    return None

def main():
    # check number of args
    if(len(sys.argv) < 2 or len(sys.argv)>3):
        printHelp();
        sys.exit(1);
    name = confFile = datFile = ""
    if(len(sys.argv) == 2):
        name, datFile = sys.argv
    if(len(sys.argv) == 3):
        name, datFile, confFile = sys.argv
    pygame.init();
    pygame.display.set_caption("faceFlasher v0.1")
    pygame.mouse.set_visible(0)
    global surface
    # fullscreen mode
    # pygame.DOUBLEBUF|pygame.HWSURFACE
    surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF,0)    

    if(confFile != ""):
        loadConfFile(confFile)
    else:
        loadConfFile("config.ini")
    
    #clock = pygame.time.Clock()
        
    infoObject = pygame.display.Info()
    surface.fill(conf["bgColor"])            
    
    # load control file
    lstLine = loadControlFile(datFile)
    global images
    images = {}    
    images = preLoadImages(lstLine)

    # Set imgDimension in config dict
    line = lstLine[0]
    col = line.split("\t")
    setConfImgDim(getImgDim(images.keys()[0]))
    #print conf["imgWidth"]
    
    #print str(conf["imgWidth"])+"---"+str(conf["imgHeight"])
      
    #print lstLine
    #if(not checkControlFile(lstLine)):
    #    sys.exit(1)    
    
    counter = 0
    ts1 = ts2 = si = isi = rep = 0
    flash = False
    
    drawCross(surface)
    pygame.display.update()
    #t=0
    frames = 0
    clearing = False
    ms = 0
    refresh = False
    """if surface.get_flags() & DOUBLEBUF:
        print "it worked!"
    else:
        print "it worked not ! :("   
    sys.exit(1) """
    while True:
        #ts2 = int(round(time.time()*1000))
        ts2 = time.clock() * 1000
        frames+=1
        # check for events
        for event in pygame.event.get():
            # quit game ?
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE) or (event.type == KEYUP and event.key == K_x):
                print("program terminated!")
                pygame.quit()
                sys.exit(1)
        if(len(lstLine) <= counter):        
            rep += 1
            if(rep < conf["repetitions"]):
                counter = 0
                frames = 0
            elif(conf["repetitions"] == 0):
                counter = 0
                rep = 0
                frames=0
            else:
                print("EndOfFile: .dat-File successfully executed!")
                pygame.quit()
                sys.exit(1)            
        if(not flash):            
            flash = True
            line = lstLine[counter]
            col = line.split("\t")
            counter += 1
            displayLineImages(col[0],col[1],col[2],surface)
            #lstRect = getImgRectList()
            #pygame.display.update(getImgRectList())
            si = getFramesInMs(conf["si"])
            isi = getFramesInMs(conf["isi"])            
            if(len(col) > 3):
                si = getFramesInMs(int(col[3]))
            if(len(col) > 4):
                isi = getFramesInMs(int(col[4]))
            #ts1 = int(round(time.time()*1000))
            #print str(ts2-ts1)
            ts1 = time.clock() * 1000
            #pygame.display.update(getImgRectList())   
            frames=0
            refresh = True
            #print(ms)
        """if(isi > 0 and not clearing):
            if(frames >= si):
                clearDisplay(surface)
                clearing = True
                #print "Clearing"
                #pygame.display.update(getImgRectList())   
                
        if(frames >= si+isi):
            flash = False
            clearing = False"""
        if(isi>0  and not clearing):
            if(ts2 - ts1 >= si):
                #print str(ts2-ts1)
                clearDisplay(surface)
                drawCross(surface)
                clearing = True
                refresh = True
        if(ts2 - ts1 >= si + isi):
            #print str(ts2-ts1)
            flash = False
            clearing = False
        
        #lstRect = getImgRectList()
        #print isi
        #print si
        if(refresh):
            pygame.display.flip()
            refresh = False
        #pygame.display.update(getImgRectList())  
             
        #print(type(isi),type(si))
        
        #pygame.display.update()
        #diff = ts2-ts1
        #print("ts1 %d ts2 %d isi %d diff %d" %(ts1,ts2,conf["isi"],diff))
        
        #for line in datFile:        
            #lineNo = lineNo+1
            #col = line.split("\t")
            #if (len(col) < 2):
                #print("Fehler in Steuerdatei!\n Zeile "+lineNo+": Eine Zeile muss aus mindestens 2 Spalten bestehen!")
            ## Stimuluspraesentatation
            #image = pygame.image.load("images/"+col[0]+".gif")
            #imageRect = image.get_rect()        
            #surface.blit(image, (200,200))
            #pygame.display.update()         
            #time.sleep(conf["si"]/1000)
            #surface.fill(conf["bgColor"])
            #pygame.display.update()    
            #time.sleep(conf["isi"]/1000)
        
        
if __name__ == "__main__":
    main()
