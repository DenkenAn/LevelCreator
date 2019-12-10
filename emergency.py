# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 21:25:50 2019

@author: Aman Aadi
"""

if __name__ == "__main__":
    print("This is the emergency library, used for clearing the list of saved games and storing unused code")

f=open("savedgames.dat","wb")
f.close()

#==============================================================================
# UNUSED/WIP CODE
#==============================================================================

'''
class list function and this

used in Character class for better movement

'''


#    @property
#    def effectivegrid(self):
#        self.egrid=((self.x+10,self.y+10),
#                       (self.x+54,self.y+10),
#                       (self.x+54,self.y+54),
#                       (self.x+10,self.y+54))
#        
#        return self.egrid
#    
#    def draw(self):
#
#        keys=pygame.key.get_pressed()
#        
#        efList=self.genFList()
#        
#        typ = classifylist(efList)
#        
#        print(typ)
#        
#        if typ == "scalar":
#            coord=efList[0]
#            try:
#                if (keys[pygame.K_LEFT] and self.__BoundLeft+self.vel<=self.x) and self.mainGrid[coord[1]][coord[0]-1].isWalkable:
#                    self.Walking=True
#                    self.Facing="L"
#                    self.x-=self.vel
#                elif (keys[pygame.K_RIGHT] and self.x<=self.__BoundRight-self.size[0]-self.vel) and self.mainGrid[coord[1]][coord[0]+1].isWalkable:
#                    self.Walking=True
#                    self.Facing="R"
#                    self.x += self.vel
#                elif keys[pygame.K_UP] and self.y>=self.__BoundUp+self.vel and self.mainGrid[coord[1]-1][coord[0]].isWalkable:
#                    self.Walking=True
#                    self.Facing="U"
#                    self.y-=self.vel
#                elif keys[pygame.K_DOWN] and self.y<=self.__BoundDown-self.size[0]-self.vel and self.mainGrid[coord[1]+1][coord[0]].isWalkable:
#                    self.Walking=True
#                    self.Facing="D"
#                    self.y+=self.vel
#            except:
#                pass
#        
#        elif typ == "dual L-R":
#            coord1=set(efList)[0]
#            coord2=set(efList)[1]
#            condU=self.mainGrid[coord1[1]-1][coord1[0]].isWalkable and self.mainGrid[coord2[1]-1][coord2[0]].isWalkable
#            condD=self.mainGrid[coord1[1]+1][coord1[0]].isWalkable and self.mainGrid[coord2[1]+1][coord2[0]].isWalkable
#            try:
#                if (keys[pygame.K_LEFT] and self.__BoundLeft+self.vel<=self.x):
#                    self.Walking=True
#                    self.Facing="L"
#                    self.x-=self.vel
#                elif (keys[pygame.K_RIGHT] and self.x<=self.__BoundRight-self.size[0]-self.vel):
#                    self.Walking=True
#                    self.Facing="R"
#                    self.x += self.vel
#                elif keys[pygame.K_UP] and self.y>=self.__BoundUp+self.vel and condU:
#                    self.Walking=True
#                    self.Facing="U"
#                    self.y-=self.vel
#                elif keys[pygame.K_DOWN] and self.y<=self.__BoundDown-self.size[0]-self.vel and condD:
#                    self.Walking=True
#                    self.Facing="D"
#                    self.y+=self.vel
#            except:
#                pass
#        
#        elif typ == "dual U-D":
#            coord1=set(efList)[0]
#            coord2=set(efList)[1]
#            condL=self.mainGrid[coord1[1]][coord1[0]-1].isWalkable and self.mainGrid[coord2[1]][coord2[0]-1].isWalkable
#            condR=self.mainGrid[coord1[1]][coord1[0]+1].isWalkable and self.mainGrid[coord2[1]][coord2[0]+1].isWalkable
#            try:
#                if keys[pygame.K_UP] and self.y>=self.__BoundUp+self.vel:
#                    self.Walking=True
#                    self.Facing="U"
#                    self.y-=self.vel
#                elif keys[pygame.K_DOWN] and self.y<=self.__BoundDown-self.size[0]-self.vel:
#                    self.Walking=True
#                    self.Facing="D"
#                    self.y+=self.vel
#                elif (keys[pygame.K_LEFT] and self.__BoundLeft+self.vel<=self.x) and condL:
#                    self.Walking=True
#                    self.Facing="L"
#                    self.x-=self.vel
#                elif (keys[pygame.K_RIGHT] and self.x<=self.__BoundRight-self.size[0]-self.vel) and condR:
#                    self.Walking=True
#                    self.Facing="R"
#                    self.x += self.vel
#            except:
#                pass
#        
#        elif typ == "quad":
#            try:
#                if (keys[pygame.K_LEFT] and self.__BoundLeft+self.vel<=self.x):
#                    self.Walking=True
#                    self.Facing="L"
#                    self.x-=self.vel
#                elif (keys[pygame.K_RIGHT] and self.x<=self.__BoundRight-self.size[0]-self.vel):
#                    self.Walking=True
#                    self.Facing="R"
#                    self.x += self.vel
#                elif keys[pygame.K_UP] and self.y>=self.__BoundUp+self.vel:
#                    self.Walking=True
#                    self.Facing="U"
#                    self.y-=self.vel
#                elif keys[pygame.K_DOWN] and self.y<=self.__BoundDown-self.size[0]-self.vel:
#                    self.Walking=True
#                    self.Facing="D"
#                    self.y+=self.vel
#            
#            except:
#                pass
#            
#        else:
#            pass
#        
#        if self.Walking:
#            if self.WalkCount<27:
#                cur=charSpriteDict[self.Facing][self.WalkCount//3]
#                gameDisp.blit(cur,(self.x,self.y))
#                self.WalkCount+=1
#            else:
#                gameDisp.blit(charSpriteDict[self.Facing][0],(self.x,self.y))
#                self.Walking=False
#                self.WalkCount=0
#        else:
#            gameDisp.blit(charSpriteDict[self.Facing][0],(self.x,self.y))
#            self.WalkCount=0
#        
#        self.Walking=False
#        pygame.display.update()
#    
#    def cellX(self,x):
#        return (x-self.__BoundLeft)//self.size[0]
#    
#    def cellY(self,y):
#        return (y-self.__BoundUp)//self.size[0]
#    
#    def genFList(self):
#        curx=self.cellX(x)
#        cury=self.cellY(y)
#        return (curx,cury)
#        flist=[]
#        
#        for i in self.effectivegrid:
#            try:
#                xval=self.cellX(self.x)
#                yval=self.cellY(self.y)
#                
#                flist.append((xval,yval))
#            except:
#                flist.append(False)
#        return flist

'''
TO ADD

edit button
more traps/collectable
browse
credits
walking function
SavedGame class efficiency
createloop efficiency and independence
'''