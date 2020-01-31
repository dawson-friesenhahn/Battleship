'''
Battleship, as written by Dawson Friesenhahn. 
Start date: July 2, 2013. 
Finish date: Functional by end of July, but always adding updates!
Dictionaries:
        userships: the state of all quadrants in which the user's ships are contained, global
        compships: the state of all quadrants in which the computer's ships are contained, global
        butdict: all quadrants, used to change the state of quadrant using butdict[COORDINATES].button.config()
        compshiplenghts: shows coordinates of each ship, with key being ship length, and value being list of coordinates that haven't yet been shot
        usershiplengths: '' ''
                
Tuples:
        alpha: characters, global
        num: 0-9 characters, global
        coord: all possible coordinates from A0 to J9, global
        ships: lengths of ships, global
        

Lists:
        compshotstaken:  coordinates the computer has shot at, prevents duplicate shots
        shipsplaced: whether or not user ship of corresponding length has been placed, global
        compshipsplaced: whether or not comp ship of corresponding length has been placed
        needs_to_shoot: coordinates remaining for the computer to sink the ship it has currently hit
        cshipsr: lengths of the remaining computer ships
        ushipsr: lengths of the remaining user ships
        
        
        
Other variables:
        c_column: int variable that is the position of the current quadrant, global, but only used in quadrant class gridding
        c_row: '' ''
        view: str variable, used to save which gameboard is currently being displayed, global
        hit: boolean variable, tells whether or not the computer is in the middle of sinking a ship
        direct: str variable, used during user ship placement to determine ship orientation
        



'''





from random import randint
import Tkinter as tk
from time import sleep
from tkMessageBox import showinfo, showwarning
root= tk.Tk()
root.title('Battleship')
root.resizable(0,0)
alpha= ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
num= ('0','1','2','3','4','5','6','7','8','9')
coord= []
c_column= 2
c_row= 2
hit= False
view= 'user'
ships= (2,3,3,4,5) #lengths of all ships
shipsplaced=[False, False, False, False, False]
compshipsplaced=[False, False, False, False, False]
needs_to_shoot= []
compshotstaken= []
compshiplengths= {}
usershiplengths= {}
shiplength= 0
direct= 'updwn'

for i in ships:
        compshiplengths[i]= []
        usershiplengths[i]= []
compshiplengths[7]= []
usershiplengths[7]= []

for a in alpha:
        for b in num:
                coord.append(a+b)
coord= tuple(coord) #tuple of all possible coordinates
userships= {}
compships= {}
butdict= {}
for a in coord:
        userships[a]= 0 #creates dictionary of all coordinates, sets
        compships[a]= 0
#                       #them all equal to zero(nothing there)


def check():
        lists= []
        for a in userships:
                lists.append(userships[a])
        if 1 not in lists:
                gameover(False)
                return
        lists= []
        for a in compships:
                lists.append(compships[a])
        if 1 not in lists:
                gameover(True)
                return
        
        


class quadrant(object):	
	def clicked(self): #check if enemy ship is next to current location, if not display sunk
                if False not in shipsplaced:
                        global compships
                        global compshiplengths
                        if compships[self.coord]==1: #ship is there
                                compships[self.coord]= 2
                                for i in compshiplengths:
                                        if self.coord in compshiplengths[i]:
                                                compshiplengths[i].remove(self.coord)
                                                if compshiplengths[i]== []:
                                                        if i!=7:
                                                                showinfo('Good Shot', 'You sunk the enemy\'s ship that was '+ str(i)+ ' units long.')
                                                        else:
                                                                showinfo('Good Shot', 'You sunk the enemy\'s ship that was 3 units long.')
                        else: #ship isnt there
                                compships[self.coord]= 3
                        updateboard()#move up a few lines so that the showinfo shows up after the box turns red i
                        compTakeShot()
                        check()
                else:
                        placeUserShips(self.coord)
                        
                        
	def __init__(self, coord):
                global c_column
                global c_row
                self.coord= coord
		self.button= tk.Button(root, width= 1, height= 1, bg= 'BLUE', command= self.clicked)
		self.button.grid(column= c_column, row= c_row)
		c_column+=1
		if c_column>11:
                        c_row+=1
                        c_column=2

#creates all hundred quadrants
for a in coord: 
        butdict[a]= quadrant(a)

class label(object):
        def __init__(self, text, mrow, mcolumn):
                self.label= tk.Label(root, text= text)
                self.label.grid(row= mrow, column= mcolumn)

def updateboard():
        if view== 'comp':
                which_board.label.config(text='Where you\'ve shot')
                root.update()
                for a in compships:
                                if compships[a]== 0: #nothing there
                                        butdict[a].button.config(bg= 'blue', state= 'normal')
                                elif compships[a]== 1: #computer ship is there.
                                        butdict[a].button.config(bg= 'blue', state= 'normal')
                                elif compships[a]== 2: #user shot here and got a hit
                                        butdict[a].button.config(bg= 'red', state= 'disabled')
                                elif compships[a]== 3: #user shot here and got a miss
                                        butdict[a].button.config(bg= 'white', state= 'disabled')
        else:
                which_board.label.config(text= 'Your ships')
                root.update()
                for a in userships:
                        if userships[a]== 0: #nothing there
                                butdict[a].button.config(bg= 'blue')
                        elif userships[a]== 1: #user ship is located here
                                butdict[a].button.config(bg='#777777')
                        elif userships[a]==2: #computer shot here and got a hit
                                butdict[a].button.config(bg= 'red')
                        elif userships[a]==3: #computer shot here and missed
                                butdict[a].button.config(bg= 'white')
                if False not in shipsplaced:
                        for a in butdict:
                                butdict[a].button.config(state= 'disabled')
                
                        

def chgview():
        global view
        global butdict
        if view== 'user':
                view= 'comp'
                updateboard()
        else:
                view= 'user'
                updateboard()

def changeDirection():                                
        global direct
        if direct== 'updwn':
                direct= 'lftright'
                changedir.config(text= 'Left-Right')
        elif direct== 'lftright':
                direct= 'updwn'
                changedir.config(text= 'Up-Down')


def compTakeShot():
        global hit
        global compshotstaken
        global shiplength
        if not hit:
                shot= alpha[randint(0,9)]+num[randint(0,9)]
                a= 0
                while shot in compshotstaken: 
                        shot= alpha[randint(0,9)]+num[randint(0,9)]
                        a+=1
                        if a>100:
                                which_board.label.config(text= 'Max number of shots reached. Quitting game...')
                                root.update()
                                sleep(3)
                                root.quit()
                                break
                compshotstaken.append(shot)
                global userships
                if userships[shot]== 1: #comp got a hit
                        userships[shot]= 2
                        hit= True
                        letter= alpha.index(shot[0])
                        number= int(shot[1])
                        global needs_to_shoot
                        for i in usershiplengths:
                                if shot in usershiplengths[i]:
                                        needs_to_shoot= usershiplengths[i]
                                        needs_to_shoot.remove(shot)
                                        if i!= 7:
                                                shiplength= i
                                        else:
                                                shiplength= 3
                else:
                        userships[shot]= 3  #comp missed
                updateboard()
                return
        elif hit:
                print 'hit is true, needs_to_shoot=', needs_to_shoot
                try:
                        shot= needs_to_shoot[0]
                except:
                        hit= False
                        showwarning('Warning', 'The enemy just sunk your ship that was '+str(shiplength)+' units long. Be careful!')
                        shiplength= 0
                        return
                userships[shot]= 2
                needs_to_shoot.remove(shot)
                compshotstaken.append(shot)
                updateboard()
                        
                
def placeUserShips(begin): #delete widgets by calling WIDGETNAME.grid_forget()
        global shipsplaced
        global usershiplengths
        global userships
        print shipsplaced
        for a in range(0,5):
                if shipsplaced[a]==True:
                        continue
                else:
                        if direct== 'updwn':
                                tobeplaced= []
                                try:
                                        pos= alpha.index(begin[0]) #returns value of letter in alphabet, a= 1, b=2
                                except:
                                        instruct.config(text= 'Coordinate pair not valid.')
                                        root.update()
                                        sleep(3)
                                        instruct.config(text= 'Type starting coordinates for current ship. Length= '+str(ships[a]))
                                        root.update()
                                        break 
                                number= begin[1]
                                if pos> 10- ships[a]:
                                        instruct.config(text= 'Ship placement at given location not allowed.')
                                        root.update()
                                        sleep(3)
                                        instruct.config(text= 'Type starting coordinates for current ship. Length= '+str(ships[a]))
                                        root.update()
                                        break 
                                for b in range(pos, pos+ships[a]):
                                        shiploc= alpha[b]+number
                                        if userships[shiploc]!= 1:
                                                tobeplaced.append(shiploc)
                                        else:
                                                instruct.config(text= 'Ship placement at given location not allowed.')
                                                root.update()
                                                sleep(3)
                                                instruct.config(text= 'Click on the starting quadrant for current ship. Length= '+str(ships[a]))
                                                root.update()
                                                return
                                for i in tobeplaced:
                                        usershiplengths[ships[a]].append(i)
                                        userships[i]= 1
                                if a!=4:
                                        instruct.config(text= 'Type starting coordinates for current ship. Length= '+str(ships[a]))
                                        root.update()
                                shipsplaced[a]= True
                                break
                        elif direct== 'lftright':
                                pos= int(begin[1])
                                letter= begin[0]
                                lists=[]
                                tobeplaced= []
                                if pos> 10-ships[a]:
                                        instruct.config(text= 'Ship placement at given location not allowed.')
                                        root.update()
                                        sleep(3)
                                        instruct.config(text= 'Type starting coordinates for current ship. Length= '+str(ships[a]))
                                        root.update()
                                        break
                                for b in range(pos, pos+ships[a]):
                                        shiploc= letter+str(b)
                                        if userships[shiploc]!=1:
                                                tobeplaced.append(shiploc)
                                        else:
                                                instruct.config(text= 'Ship placement at given location not allowed.')
                                                root.update()
                                                sleep(3)
                                                instruct.config(text= 'Type starting coordinates for current ship. Length= '+str(ships[a]))
                                                root.update()
                                                return
                                for i in tobeplaced:
                                        usershiplengths[ships[a]].append(i)
                                        userships[i]= 1
                                if a!=4:
                                        instruct.config(text= 'Click starting quadrant for current ship. Length= '+str(ships[a+1]))
                                        root.update()
                                shipsplaced[a]= True
                                break
        if False not in shipsplaced:
                global view
                changedir.grid_forget()
                change_board.config(state= 'normal', relief= 'raised')
                toremove= []
                print usershiplengths
                for c in range(3,6):
                        usershiplengths[7].append(usershiplengths[3][c])
                        toremove.append(usershiplengths[3][c])
                for c in toremove:
                        usershiplengths[3].remove(c)
                print usershiplengths
                view= 'comp'
        updateboard()

def showInstruct():
        showinfo('Instructions', 'Welcome to Battleship!\
\nTo place your ships, toggle whether you want your ships to be Up-Down or Left-Right, then click in the box that you want your ship to start in.\
\n \nOnce you have placed your ships, you can start taking some shots at the enemy by clicking in the quadrant you think the enemy ship might be in.\
The quadrant will turn Red if you got a hit, and White if you missed.\
\n \nYou may want to check on your ships every so often by changing the view. The red squares show where the enemy has scored a hit,\
and the gray where your ships are still ok. \n \n The first team to eleminate the enemy wins!\
\n \n Created by Dawson Friesenhahn using Python v2.7.5 and Tkinter. www.python.org \
\n \nFor questions, comments, suggestions, or bug reports, email me anytime at dawsonfriesenhahn@gmail.com\
\n \n July 2013')
        
       
a= label('A', 2,1)
b= label('B', 3,1)
c= label('C', 4,1)
d= label('D', 5,1)
e= label('E', 6,1)
f= label('F', 7,1)
g= label('G', 8,1)
h= label('H', 9,1)
i= label('I', 10,1)
j= label('J', 11,1)
l0= label('0', 1,2)
l1= label('1', 1,3)
l2= label('2', 1,4)
l3= label('3', 1,5)
l4= label('4', 1,6)
l5= label('5', 1,7)
l6= label('6', 1,8)
l7= label('7', 1,9)
l8= label('8', 1,10)
l9= label('9', 1, 11)
which_board= label('', 4, 12)
change_board= tk.Button(root, text= 'Click to change view', command= chgview)
change_board.grid(row=5, column= 12)
change_board.config(state= 'disabled', relief= 'sunken')
instruct= tk.Label(root, text= 'Click starting quadrant for current ship. Length= 2')
instruct.grid(row=6, column= 12, columnspan= 5)
changedir= tk.Button(root, text= 'Up-Down', command= changeDirection)
changedir.grid(row= 8, column= 13, columnspan= 2)
infobut= tk.Button(root, text= 'Help', command= showInstruct)
infobut.grid(row= 11, column= 17)


def gameover(win):
        if win:
                mtext= 'Congratulations! You won! Restart the program to try again!' #win = True or false when called
        else:
                mtext= 'You lost. Restart the program to try again!'
                global view
                view= 'user'
                updateboard()
        showinfo('Game Over', mtext)
        root.quit()


def place(position):
        global compships
        global compshipslengths
        shipcoords= []
        length= ships[position]
        direction= randint(0,1)
        if direction== 0: #up-down
                print 'up-down'
                startpos= randint(0, 9-length)
                number= num[randint(0,9)]
                for a in range(startpos, startpos+length):
                        shipcoords.append(alpha[a]+number)
        elif direction== 1: #left-right
                print 'left-right'
                letter= alpha[randint(0,9)]
                number= num[randint(0,9-length)]
                for a in range(int(number), int(number)+length):
                        shipcoords.append(letter+num[a])
        for i in shipcoords:
                if compships[i]==1:
                        print 'returning False'
                        shipcoords=[]
                        return False
        for a in shipcoords:
                compships[a]= 1
                compshiplengths[length].append(a)
        updateboard()
        print length, shipcoords
        print 'placed ship'
        return True
        

def placeCompShips():
        global compshipsplaced
        global compshiplengths
        pos= 0
        while False in compshipsplaced:
                if place(pos)== False:
                        continue
                compshipsplaced[pos]= True
                print 'incrementing pos'
                pos+= 1
        toremove= []
        for a in range(3,6):
                print a
                compshiplengths[7].append(compshiplengths[3][a])
                toremove.append(compshiplengths[3][a])
        for a in toremove:
                compshiplengths[3].remove(a)
                
        print compshiplengths

        
if __name__ == '__main__':                
        placeCompShips()
        root.mainloop()
		



		
