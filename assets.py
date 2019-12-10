# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:41:59 2019

@author: Aman Aadi
"""

import pygame

if __name__ == "__main__":
    print("This is the asset library")

class Stack:
    
    def __init__(self):
        self.items=[]
    
    def push(self,data):
        self.items.append(data)
    
    def pop(self):
        if self.items!=[]:
            return self.items.pop(-1)
        else:
            print("Underflow")

    def peek(self):
        if self.items!=[]:
            return self.items[-1]
    
    def is_empty(self):
        if self.items==[]:
            return True
        return False
    
    def __len__(self):
        return len(self.items)
    
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
grey=(130,130,130)
yellow=(255,255,51)

iconImg=pygame.image.load("icon.png")
mainImg=pygame.image.load("LEVELCREATOR.png")

bgroundMenu=pygame.image.load("bgmenu.png")
bgroundCreate=pygame.image.load("bgcreate.png")
bgroundLoad=pygame.image.load("bgload.png")
bgroundTest=pygame.image.load("bgtest.png")
bgroundShaded=pygame.image.load("shaded.png")

createButtonI=pygame.image.load("createI.png")
createButtonA=pygame.image.load("createA.png")
loadButtonI=pygame.image.load("loadI.png")
loadButtonA=pygame.image.load("loadA.png")
credButtonI=pygame.image.load("creditsI.png")
credButtonA=pygame.image.load("creditsA.png")

rightButtonI=pygame.image.load("rightI.png")
rightButtonA=pygame.image.load("rightA.png")
leftButtonI=pygame.image.load("leftI.png")
leftButtonA=pygame.image.load("leftA.png")

saveButtonI=pygame.image.load("savebuttonI.png")
saveButtonA=pygame.image.load("savebuttonA.png")
camButtonI=pygame.image.load("cambuttonI.png")
camButtonA=pygame.image.load("cambuttonA.png")
backButtonI=pygame.image.load("backbuttonI.png")
backButtonA=pygame.image.load("backbuttonA.png")
eraseButtonI=pygame.image.load("erasebuttonI.png")
eraseButtonC=pygame.image.load("erasebuttonC.png")

playButtonI=pygame.image.load("playbuttonI.png")
playButtonA=pygame.image.load("playbuttonA.png")
backButtonLoadI=pygame.image.load("backbuttonloadI.png")
backButtonLoadA=pygame.image.load("backbuttonloadA.png")

emptyCell=pygame.image.load("cell.png")
startZoneImg=pygame.image.load("startzone.png")
endZoneImg=pygame.image.load("endzone.png")
floorImg=pygame.image.load("floor.png")
floorImgSelect=pygame.image.load("floorA.png")
wallImg=pygame.image.load("wall.png")
wallImgSelect=pygame.image.load("wallA.png")
cobwebImg=pygame.image.load("web.png")
cobwebImgSelect=pygame.image.load("webselect.png")

fireGrate=[pygame.image.load(".\Fire\grate{f}.png".format(f=i)) for i in range(1,16)]
fireGrateSelect=pygame.image.load(".\Fire\grateselect.png")

coinImg=pygame.image.load("coin.png")
coinImgSelect=pygame.image.load("coinselect.png")
gemImg=pygame.image.load("gem.png")
gemImgSelect=pygame.image.load("gemselect.png")

charSpriteD=[pygame.image.load(".\Sprites\spriteherodown{f}.png".format(f=i)) for i in range(1,10)]
charSpriteU=[pygame.image.load(".\Sprites\spriteheroup{f}.png".format(f=i)) for i in range(1,10)]
charSpriteL=[pygame.image.load(".\Sprites\spriteheroleft{f}.png".format(f=i)) for i in range(1,10)]
charSpriteR=[pygame.image.load(".\Sprites\spriteheroright{f}.png".format(f=i)) for i in range(1,10)]

charSpriteDict={"D":charSpriteD,"U":charSpriteU,"L":charSpriteL,"R":charSpriteR}

loadBarImg=pygame.image.load("loadbar.png")
coverImg=pygame.image.load("cover.png")

upImg=pygame.image.load("up.png")
downImg=pygame.image.load("down.png")
leftImg=pygame.image.load("left.png")
rightImg=pygame.image.load("right.png")

trashButtonI=pygame.image.load("trashI.png")
trashButtonA=pygame.image.load("trashA.png")
editButtonI=pygame.image.load("editI.png")
editButtonA=pygame.image.load("editA.png")

credit=pygame.image.load("credits.png")

pygame.quit()
