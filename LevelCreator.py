# -*- coding: utf-8 -*-
"""
This is the level creator.
"""

import pygame
import time
import tkinter as tk
import os
import pickle
import copy
import random

from assets import *

pygame.init()

pygame.mixer.music.load("Megalovania.ogg")

gameDisp=pygame.display.set_mode((1280,720))
pygame.display.set_caption("LevelCreator")
pygame.display.set_icon(iconImg)
clock=pygame.time.Clock()

cnt=0

def test():
    print("yes")

def readlines(f):
    m=[]
    while True:
        try:
            m.append(pickle.load(f))
        except:
            break
    
    return m

def text_objects(text,font,col=black):
    textSurface=font.render(text,True,col)
    return textSurface, textSurface.get_rect()

def message_display(text,f,col,size,x,y):
    largeText=pygame.font.Font(f,size)
    TextSurf = text_objects(text,largeText,col)[0]
    TextRect=(x,y)
    gameDisp.blit(TextSurf,TextRect)

def buttonImg(imgI,imgA,x,y,func):                     #hover/clickable buttons
    mouse=pygame.mouse.get_pos()
    w=imgI.get_rect().size[0]
    h=imgI.get_rect().size[1]
    click=pygame.mouse.get_pressed()
    
    global cnt
    
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        gameDisp.blit(imgA,(x,y))
        if click[0] == 1 and cnt==0:
            cnt+=1
            func()
        elif click[0]==0:
            cnt=0
            
    else:
        gameDisp.blit(imgI,(x,y))

def selectable(imgI,imgC,x,y,obj):                       #toggleable buttons, set highlight to a class
    
    global highlight,hpos,cnt
    
    mouse=pygame.mouse.get_pos()
    w=imgI.get_rect().size[0]
    h=imgI.get_rect().size[1]
    click=pygame.mouse.get_pressed()
    
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        if click[0] == 1 and cnt==0:
            cnt+=1
            highlight=obj(x,y)
            hpos=(x,y)
        elif click[0]==0:
            cnt=0
    
    if hpos == (x,y) and highlight:
        gameDisp.blit(imgC,(x,y))
    else:
        gameDisp.blit(imgI,(x,y))

def game_menu():                                         #game menu loop
    
    menuExit=False
    
    while not menuExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisp.fill(black)
        gameDisp.blit(bgroundMenu,(0,0))
        
        gameDisp.blit(mainImg,(140,100))
        
        buttonImg(createButtonI,createButtonA,100,520,game_create)
        buttonImg(loadButtonI,loadButtonA,493,520,game_load)
        buttonImg(credButtonI,credButtonA,886,520,game_credits)
        
        pygame.display.update()
        clock.tick(40)

#------------------------------------------------------------------------------
# CREATE MODE CLASSES
#------------------------------------------------------------------------------

class Placeable:
    
    @classmethod
    def assign(cls,x,y):
        return cls(x,y)
    
    def evoke(self,char,grid):
        pass

class Zone(Placeable):
    isWalkable=True
    
    def __init__(self,x,y,nature):
        self.nature=nature.upper()
        self.x=x
        self.y=y
    
    def draw(self):
        if self.nature=="END":
            gameDisp.blit(endZoneImg,(self.x,self.y))
        elif self.nature=="START":
            gameDisp.blit(startZoneImg,(self.x,self.y))

    def evoke(self,char,grid):
        if self.nature == "END":
            gameOver("good")

class Void(Placeable):
    isWalkable=False
    bottom=True
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def draw(self):
        gameDisp.blit(emptyCell,(self.x,self.y))
    
class Floor(Placeable):
    isWalkable=True
    bottom=True
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def draw(self):
        gameDisp.blit(floorImg,(self.x,self.y))

class Wall(Placeable):
    isWalkable=False
    bottom=True
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def draw(self):
        gameDisp.blit(wallImg,(self.x,self.y))

class Collectable(Placeable):
    isWalkable=True
    bottom=False
    value=0
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def evoke(self,char,grid):
        char.score+=self.value
        f=char.cur_grid()
        grid[f[1]][f[0]]=None
        
class Coin(Collectable):
    value=5

    def draw(self):
        gameDisp.blit(coinImg,(self.x,self.y))

class Gem(Collectable):
    value=10
    
    def draw(self):
        gameDisp.blit(gemImg,(self.x,self.y))

class Trap(Placeable):
    isWalkable=True
    bottom=False
    
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Cobweb(Trap):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.Activated=False
    
    def draw(self):
        gameDisp.blit(cobwebImg,(self.x,self.y))

    def evoke(self,char,grid):
        char.Stuck=True
        
        global buts
        
        imp={"U":(pygame.K_UP,upImg),
             "D":(pygame.K_DOWN,downImg),
             "L":(pygame.K_LEFT,leftImg),
             "R":(pygame.K_RIGHT,rightImg)
             }
        
        if self.Activated:
            
            if buts.is_empty():
                self.Activated=False
                char.Stuck=False
                f=char.cur_grid()
                grid[f[1]][f[0]]=None
            
            else:
                
                gameDisp.blit(imp[buts.items[0]][1],(1200,330))
                if len(buts)>1:
                    gameDisp.blit(imp[buts.items[1]][1],(20,330))
                
                keys=pygame.key.get_pressed()
                
                top=imp[buts.peek()][0]
                if keys[top]:
                    buts.pop()
                        
        else:
            buts=Stack()
            
            k=["U","D","L","R"]
            
            for i in range(2):
                f=random.randint(0,3)
                buts.push(k[f])
            
            self.Activated=True

class FireGrate(Trap):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.FireCount=0

    def draw(self):
        
        if self.FireCount <= 56:
            cur=fireGrate[self.FireCount//4]
            gameDisp.blit(cur,(self.x,self.y))
            self.FireCount+=1
        else:
            gameDisp.blit(fireGrate[0],(self.x,self.y))
            self.FireCount=0
        
    def evoke(self,char,grid):
        if 20<self.FireCount<36:
            char.Alive=False

#------------------------------------------------------------------------------
# CHARACTER CLASS
#------------------------------------------------------------------------------

class Character:

    def __init__(self,x,y,topleft,botright,main,hover):
        self.x=x
        self.y=y
        self.vel=4
        self.size=(64,64)
        
        self.pos=self.cur_grid
        
        self._BoundUp=topleft[1]
        self._BoundLeft=topleft[0]
        self._BoundRight=botright[0]
        self._BoundDown=botright[1]
        
        self.mainGrid=main
        self.hoverGrid=hover
        
        self.Walking=False
        self.WalkCount=0
        self.Facing='D'
        self.score=0
        
        self.Alive=True
        self.Stuck=False
    
    def cur_grid(self):
        cur_x=(self.x-self._BoundLeft)//self.size[0]
        cur_y=(self.y-self._BoundUp)//self.size[0]
        self.pos=cur_x,cur_y
        return self.pos
    
    def main_block(self):
        f = self.cur_grid()
        return self.mainGrid[f[1]][f[0]]

    def hover_block(self):
        f = self.cur_grid()
        return self.hoverGrid[f[1]][f[0]]

    def draw(self):
        
        global cnt
        
        keys=pygame.key.get_pressed()
        
        if self.Alive and not self.Stuck:
            try:
    
                if (keys[pygame.K_LEFT]) and self.mainGrid[self.cur_grid()[1]][self.cur_grid()[0]-1].isWalkable and cnt==0:
                    cnt+=1
                    self.Facing="L"
                    self.x-=64
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
                elif(keys[pygame.K_RIGHT]) and self.mainGrid[self.cur_grid()[1]][self.cur_grid()[0]+1].isWalkable and cnt==0:
                    cnt+=1
                    self.Facing="R"
                    self.x+=64
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
                elif keys[pygame.K_UP] and self.mainGrid[self.cur_grid()[1]-1][self.cur_grid()[0]].isWalkable and cnt==0:
                    cnt+=1
                    self.Facing="U"
                    self.y-=64
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
                elif keys[pygame.K_DOWN] and self.mainGrid[self.cur_grid()[1]+1][self.cur_grid()[0]].isWalkable and cnt==0:
                    cnt+=1
                    self.Facing="D"
                    self.y+=64
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
                elif not(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                    cnt=0
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
                else:
                    cur=charSpriteDict[self.Facing][0]
                    gameDisp.blit(cur,(self.x,self.y))
    
            except:
                cnt=0
                cur=charSpriteDict[self.Facing][0]
                gameDisp.blit(cur,(self.x,self.y))
        
        elif self.Stuck:
            cur=charSpriteDict[self.Facing][0]
            gameDisp.blit(cur,(self.x,self.y))
        
        elif not self.Alive:
            gameOver("bad")
        
#------------------------------------------------------------------------------
# CREATE MENU FUNCTIONS
#------------------------------------------------------------------------------

def drawgrid(main,hover):                              #draws main grid
    for i in main:
        for j in i:
            if j:
                j.draw()
    
    for a in hover:
        for b in a:
            if b:
                b.draw()

def pageturn():                                                #turns page forward
    global page,highlight,selGame
    
    if page<pagelim:
        page+=1
    
    highlight=None
    selGame=None

def pageback():                                                # turns page back
    global page,highlight,selGame
    
    if page>0:
        page-=1
    
    highlight=None
    selGame=None

def choosegrid():                                              #draws selecting grid
    buttonImg(rightButtonI,rightButtonA,1096,286,pageturn)
    buttonImg(leftButtonI,leftButtonA,840,286,pageback)
    
    if page == 0:
        selectable(floorImg,floorImgSelect,840,116,Floor)
        selectable(wallImg,wallImgSelect,925,116,Wall)
    elif page == 1:
        selectable(cobwebImg,cobwebImgSelect,840,116,Cobweb)
        selectable(fireGrate[0],fireGrateSelect,925,116,FireGrate)
    elif page == 2:
        selectable(coinImg,coinImgSelect,840,116,Coin)
        selectable(gemImg,gemImgSelect,925,116,Gem)

def maingrid(main,hover):                                    #handles events (creating new blocks) on main grid
    global cnt
    
    mouse=pygame.mouse.get_pos()
    mCell = ((mouse[0]-100)//64,(mouse[1]-100)//64)
    click=pygame.mouse.get_pressed()
    
    if 100<=mouse[0]<740 and 100<=mouse[1]<620 and highlight:
        if click[0]==1 and cnt==0 and type(main[mCell[1]][mCell[0]])!=Zone:
            cnt+=1
            if type(highlight) == Void:
                main[mCell[1]][mCell[0]] = Void(100+64*mCell[0],100+64*mCell[1])
                hover[mCell[1]][mCell[0]] = None
            elif highlight.bottom:
                main[mCell[1]][mCell[0]] = highlight.assign(100+64*mCell[0],100+64*mCell[1])
            elif main[mCell[1]][mCell[0]].isWalkable:
                hover[mCell[1]][mCell[0]] = highlight.assign(100+64*mCell[0],100+64*mCell[1])
        elif click[0]==0:
            cnt=0

def getout():                                                           #exits game loops
    
    global createExit,loadExit,testExit,creditExit
    
    testExit = True
    createExit = True
    loadExit = True
    creditExit = True
    
    pygame.mixer.music.stop()
    
def snapshot():
    global counter
    counter+=1
    pygame.image.save(gameDisp,".\Snapshot\snap{a}.png".format(a=counter))

#------------------------------------------------------------------------------
# CREATE MENU LOOP
#------------------------------------------------------------------------------

def game_create():                                             #create screen loop
    
    global page,createExit,mainGridFloor,hoverGrid,pagelim,highlight,hpos,counter
    
    mainGridFloor=[[Void(100+(j*64),100+(i*64)) for j in range(10)] for i in range(8)]
    mainGridFloor[0][-1]=Zone(676,100,"End")
    mainGridFloor[-1][0]=Zone(100,548,"Start")
    hoverGrid=[[None for j in range(10)] for i in range(8)]
    createExit=False
    page=0
    pagelim=2
    highlight = Floor(840,116)
    hpos=(840,116)
    counter=0
    
    while not createExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        gameDisp.fill(black)
        gameDisp.blit(bgroundCreate,(0,0))
        
        drawgrid(mainGridFloor,hoverGrid)
        choosegrid()
        maingrid(mainGridFloor,hoverGrid)
        
        buttonImg(saveButtonI,saveButtonA,1015,400,save_and_load)
        buttonImg(backButtonI,backButtonA,1015,540,getout)
        selectable(eraseButtonI,eraseButtonC,820,540,Void)
        buttonImg(camButtonI,camButtonA,820,400,snapshot)
        
        pygame.display.update()
        clock.tick(40)

#------------------------------------------------------------------------------
# LOAD MODE CLASSES
#------------------------------------------------------------------------------

class SavedGame:   
    def __init__(self,BufferMain,BufferHover,identifier):
        self.MainGrid=BufferMain
        self.HoverGrid=BufferHover
        self.time=time.localtime()
        self.identifier=identifier
    
    def save(self):
        f=open("savedgames.dat","rb+")
        
        saved={"identifier":self.identifier,"maingrid":self.MainGrid,
               "hovergrid":self.HoverGrid,"time":self.time}              #arrangement!!!
        
        m=readlines(f)
        for q in m:
            if q["identifier"] == self.identifier:
                m.remove(q)
                break
            
        f.close()
        
        os.remove("savedgames.dat")
        
        m.append(saved)
        
        f2=open("savedgames.dat","wb")
        for i in m:
            pickle.dump(i,f2)
        
        f2.close()


    @classmethod
    def NoOfGames(cls):                          #imp in figuring out pages
        f=open("savedgames.dat","rb")
        m=readlines(f)
        if len(m)>11:
            SavedGame.delete(m[0]["identifier"])
        
        return len(m)
    
    @staticmethod
    def load(key):
        f=open("savedgames.dat","rb")
        
        for i in readlines(f):
            if i["identifier"] == key:
                f.close()
                return SavedGame(i["maingrid"],i["hovergrid"],i["identifier"])
        f.close()
    
    @staticmethod
    def loadallAsRawList():
        f=open("savedgames.dat","rb")
        m=readlines(f)

        f.close()
        return m
    
    @staticmethod
    def delete(key):
        f=open("savedgames.dat","rb")
        q=readlines(f)
        for i in q:
            if i["identifier"] == key:
                q.remove(i)
        f.close()
        
        os.remove("savedgames.dat")
        
        f2=open("savedgames.dat","wb")
        for j in q:
            pickle.dump(j,f2)
        
        f2.close()

#------------------------------------------------------------------------------
# TRANSITION FUNCTION
#------------------------------------------------------------------------------

def entrypopup(msg):
    def _GiveName():
        if s.get() != "":
            root.destroy()
    
    def _Cancel():
        
        global cancel
        
        s.set("")
        cancel=True
        root.destroy()
    
    global cancel
    
    cancel=False
    root=tk.Tk()
    s=tk.StringVar()
    tk.Label(root,text=msg).grid(row=0,column=0)
    tk.Entry(root,textvariable=s).grid(row=0,column=1)
    tk.Button(root,text="OK",command=_GiveName).grid(row=1,column=0)
    tk.Button(root,text="Cancel?",command=_Cancel).grid(row=1,column=1)
    root.mainloop()
    
    return s.get()

def save_and_load():
    
    m=entrypopup("What would you like to name your game?:")
    
    if not cancel:
        new = SavedGame(mainGridFloor,hoverGrid,m)
        new.save()
        game_load()

def renamegame():
    b=selGame
    deletegame()
    m=entrypopup("What would you like to rename this game to?:")
    x=SavedGame(b["maingrid"],b["hovergrid"],m)
    x.save()    
    
    getout()

def deletegame():
    
    i=selGame["identifier"]
    
    SavedGame.delete(i)
    getout()

#------------------------------------------------------------------------------
# LOAD GAME LOOP
#------------------------------------------------------------------------------

def showlist(pd):
    global cnt,selected,selGame
    
    buttonImg(rightButtonI,rightButtonA,1116,620,pageturn)
    buttonImg(leftButtonI,leftButtonA,100,620,pageback)
    
    listOfBarsInPage=[x for x in pd.keys() if x[0] == page]
    
    for i in listOfBarsInPage:
        lbx=100
        lby=100 + i[1]*(173)
        gameDisp.blit(loadBarImg,(lbx,lby))
        name=pd[i]["identifier"]
        
        nov = pd[i]["time"]
        timestamp = "Last Updated:{a}/{b}/{c} at {d}:{e}:{f}".format(
                a=nov.tm_mday,
                b=nov.tm_mon,
                c=nov.tm_year,
                d=nov.tm_hour,
                e=nov.tm_min,
                f=nov.tm_sec
                )
        
        
        message_display("Name:"+name,"ARCADE_N.ttf",black,50,lbx+170,lby+15)
        message_display(timestamp,"ARCADE_I.ttf",grey,25,lbx+170,lby+70)
        
        mouse=pygame.mouse.get_pos()
        w=loadBarImg.get_rect().size[0]
        h=loadBarImg.get_rect().size[1]
        click=pygame.mouse.get_pressed()
        
        if lbx+w>mouse[0]>lbx and lby+h>mouse[1]>lby:
            if click[0] == 1 and cnt==0:
                cnt+=1
                selGame=pd[i]
                selected=(lbx,lby)
            elif click[0]==0:
                cnt=0
        
    if selGame:
        gameDisp.blit(coverImg,selected)

def game_load():
    
    global page,pagelim,loadExit,selected,selGame
    
    loadExit = False
    page=0
    pagelim=4
    selGame=None
    
    allGames=SavedGame.loadallAsRawList()
    
    pageDict={}
    for i in range(len(allGames)):
        pageDict[(i//3,i%3)] = allGames[i]
    
    numGames = SavedGame.NoOfGames()
    if numGames > 0:
        selGame = allGames[0]
        selected=(100,100)
    
    while not loadExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisp.fill(black)
        gameDisp.blit(bgroundLoad,(0,0))
        
        buttonImg(playButtonI,playButtonA,544,620,load_and_test)
        buttonImg(backButtonLoadI,backButtonLoadA,18,18,getout)
        
        buttonImg(trashButtonI,trashButtonA,450,620,deletegame)
        buttonImg(editButtonI,editButtonA,766,620,renamegame)
        
        showlist(pageDict)
        
        pygame.display.update()
        clock.tick(40)

#------------------------------------------------------------------------------
# TRANSITION FUNCTION
#------------------------------------------------------------------------------

def trans_by_x(grid,x):
    for i in grid:
        for j in i:
            if j:
                j.x+=x

def load_and_test():
    
    newMain = copy.deepcopy(selGame["maingrid"])
    newHover = copy.deepcopy(selGame["hovergrid"])
    
    trans_by_x(newMain,220)
    trans_by_x(newHover,220)
    
    game_test(newMain,newHover)

def gameOver(key):
    
    global testExit
    
    if key.upper()=="GOOD":
        msg="YOU WON!!"
    elif key.upper()=="BAD":
        msg="YOU DIED!!"
    
    gameDisp.blit(bgroundShaded,(0,0))
    message_display(msg,"ARCADE_N.ttf",white,60,320,20)
    pygame.display.update()
    
    time.sleep(2)
    testExit=True

def scoredisp(char,x,y):
    s=char.score
    message_display("SCORE:{a}".format(a=s),"ARCADE_N.ttf",yellow,50,x,y)
    
#------------------------------------------------------------------------------
# TEST LOOP
#------------------------------------------------------------------------------

def game_test(main,hover):
    
    global testExit
    
    testExit = False
    bobby=Character(320,548,(320,100),(960,612),main,hover)
    
    while not testExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisp.fill(black)
        gameDisp.blit(bgroundTest,(0,0))
        
        buttonImg(backButtonLoadI,backButtonLoadA,18,18,getout)
        
        drawgrid(main,hover)
        bobby.draw()
        
        scoredisp(bobby,100,632)
        
        if bobby.main_block():
            bobby.main_block().evoke(bobby,main)
        
        if bobby.hover_block():
            bobby.hover_block().evoke(bobby,hover)
        
        pygame.display.update()
        clock.tick(40)

#------------------------------------------------------------------------------
# CREDITS
#------------------------------------------------------------------------------

def game_credits():
    
    pygame.mixer.music.play(-1)
    
    global creditExit
    
    creditExit=False
    count=2060
    
    while not creditExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        count-=1
        y=count//2
        
        gameDisp.fill(black)
        gameDisp.blit(bgroundLoad,(0,0))
        
        gameDisp.blit(credit,(0,y))
        
        buttonImg(backButtonLoadI,backButtonLoadA,18,18,getout)

        pygame.display.update()
        clock.tick(40)

game_menu()

pygame.quit()
quit()