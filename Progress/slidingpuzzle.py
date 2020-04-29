import random
import copy


def check1(i,j):
    global size
    a=[]
    if i-1>=0:a.append((i-1,j))
    if i+1<=size-1:a.append((i+1,j))
    if j-1>=0:a.append((i,j-1))
    if j+1<=size-1:a.append((i,j+1))
    return a


def check2(i,j):
    global size
    a=[]   
    if j+1<=size-1:a.append('j')
    if j-1>=0:a.append('k')
    if i+1<=size-1:a.append('r')
    if i-1>=0:a.append('f')
    return a


def shuffle(self):
    global x,y
    moveto=[]
    for _ in range(1000):
        moveto=check1(x,y)
        i,j=random.choice(moveto)
        self[x][y],self[i][j]=self[i][j],self[x][y]
        x,y=i,j
    return self


def prompt(self):
    print("Enter your move(",end='')
    for i in range(len(self)):
        a=self[i]
        print(dict.get(a),'-',a,end='')
        if i!=len(self)-1:print(end=',')
    print(")>",end='')


def move(self):
    global x,y,sum
    moveto=[]
    moveto=check2(x,y)
    prompt(moveto)
    step=input()
    while(step not in dict or step not in moveto):
        print('Invalid Enter!Please enter again:',end='')
        step=input()
    if step=='j':
        self[x][y],self[x][y+1]=self[x][y+1],self[x][y]
        y+=1
    elif step=='k':
        self[x][y],self[x][y-1]=self[x][y-1],self[x][y]
        y-=1
    elif step=='r':
        self[x][y],self[x+1][y]=self[x+1][y],self[x][y]
        x+=1
    elif step=='f':
        self[x][y],self[x-1][y]=self[x-1][y],self[x][y]
        x-=1
    sum+=1
    return self


def pprint(self):
    global size
    for i in range(0,size):
        for j in range(0,size):
            if puzzle[i][j]==0:print(' ',end='\t')
            else:print(puzzle[i][j],end='\t')
        print()
    print()

dict={'f':'down','r':'up','k':'right','j':'left'}
print('Welcome to 8-puzzle game, you need to repeatedly slide an adjacent tile, one at a time, to the currently unoccupied space (the empty space) until all numbers appear sequentially, ordered from left to right, top to bottom.\nEnter the four letters used for left, right, up and down directions > j k r f ')

while(1):
    print("Enter “1” for 8-puzzle, “2” for 15-puzzle or “q” to end the game: ",end='')
    sum=0
    start=input()
    if start=='q':break
    while(start!='1' and start!='2'):
        print('Invalid Enter!Please enter again:')
        start=input()
    if start=='1':size=3
    elif start=='2':size=4
    x=y=size-1
    if size==3:final=[[1,2,3],[4,5,6],[7,8,0]]   
    elif size==4:final=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    puzzle=copy.deepcopy(final)
    shuffle(puzzle)
    pprint(puzzle)
    while(final!=puzzle):
        puzzle=move(puzzle)
        pprint(puzzle)
    print(f'Congratulations! You solved the puzzle in {sum} moves! ')