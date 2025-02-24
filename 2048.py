import pygame
import random
from os.path import isfile

pygame.init()
class Button:
    def __init__(self, color, hovercolor, x, y, width, height, text=''):
        self.color = color
        self.hovercolor=hovercolor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        pos=pygame.mouse.get_pos()
        if self.isOver(pos):
            pygame.draw.rect(screen, self.hovercolor, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
    
def print_board(board):
    for i in board:
        print(*i)
    print("--------")
def move_left(board):
    b=[]
    s=0
    for line in board:
        newline=[x for x in line if x!=0]
        for i in range(len(newline)-1):
            if newline[i]==newline[i+1]:
                newline[i]*=2
                s+=newline[i]
                newline[i+1]=0
        newline=[x for x in newline if x!=0]
        line=newline+[0]*(4-len(newline))
        b.append(line)
    return b,s

def move(board,direction):
    if direction==0: #left
        board,s=move_left(board)
    elif direction==2: #right
        for i in range(4):
            board[i]=board[i][::-1]
        board,s=move_left(board)
        for i in range(4):
            board[i]=board[i][::-1]
    elif direction==1: #up
        board2=[[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                board2[j][i]=board[i][j]
        board2,s=move_left(board2)
        for i in range(4):
            for j in range(4):
                board[j][i]=board2[i][j]
    else:#down
        board2=[[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                board2[j][i]=board[i][j]
        for i in range(4):
            board2[i]=board2[i][::-1]
        board2,s=move_left(board2)
        for i in range(4):
            board2[i]=board2[i][::-1]
        for i in range(4):
            for j in range(4):
                board[j][i]=board2[i][j]
    board=add_block(board)
    return board,s

def add_block(board,n=1):
    # Find empty location
    empty=[]
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                empty.append([i,j])
    # r
    if len(empty)==0:
        return board
    # Get n empty location
    r=random.sample(empty,k=n)
    # write number into selected location
    for x,y in r:
        board[x][y]=random.choices([2,4],weights=[0.7,0.3])[0]
    return board

def drawtile(screen,board):
    for i in range(4):
        for j in range(4):

            pygame.draw.rect(screen,block_colors.get(board[i][j],(255,255,255)),(stripsize*(i+1)+tilesize*i,stripsize*(j+1)+tilesize*j+topsize,tilesize,tilesize))
            if board[i][j]!=0:
                text=font.render(str(board[i][j]),True,(0,0,0))
                text_rect = text.get_rect(center=(stripsize*(i+1)+tilesize*i+tilesize//2,stripsize*(j+1)+tilesize*j+tilesize//2+topsize))
                screen.blit(text, text_rect)

def drawtop(score):
    text=big_font.render("2048",True,(0,0,0))
    screen.blit(text, (20,20))
    
    text_score_y_diff=15
    # draw current score
    center=(400,50)
    rectheight=70
    padding=10
    w,h=score_font.size(str(score))
    w2,h=score_font.size("Current:/")
    w=max(w,w2)
    pygame.draw.rect(screen,(234,231,218),(center[0]-(w+2*padding)/2,center[1]-rectheight/2,w+2*padding,rectheight))
    
    scoretext=score_font.render(str(score),True,(0,0,0))
    text_rect = scoretext.get_rect(center=(center[0],center[1]+text_score_y_diff))
    screen.blit(scoretext, text_rect)
    
    scoretext=score_font.render("Current:",True,(0,0,0))
    text_rect = scoretext.get_rect(center=(center[0],center[1]-text_score_y_diff))
    screen.blit(scoretext, text_rect)
    
    
    # draw best score
    center=(500,50)
    w,h=score_font.size(str(hs))
    w2,h=score_font.size("Best:/")
    w=max(w,w2)
    pygame.draw.rect(screen,(234,231,218),(center[0]-(w+2*padding)/2,center[1]-rectheight/2,w+2*padding,rectheight))
    
    scoretext=score_font.render(str(hs),True,(0,0,0))
    text_rect = scoretext.get_rect(center=(center[0],center[1]+text_score_y_diff))
    screen.blit(scoretext, text_rect)

    scoretext=score_font.render("Best:",True,(0,0,0))
    text_rect = scoretext.get_rect(center=(center[0],center[1]-text_score_y_diff))
    screen.blit(scoretext, text_rect)

def init(d=False):
    if d:
        return [[1,2,3,4],[5,6,7,8],[9,1,2,3],[1,2,3,3]]
    board=[[0 for i in range(4)] for j in range(4)]
    board=add_block(board,2)
    print(board)
    return board

def death(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]==0: #0 check
                return False
            if j!=3: #right check
                if board[i][j]==board[i][j+1]:
                    return False
            if i!=3: #down check
                if board[i][j]==board[i+1][j]:
                    return False
    return True

def draw_death():
	# 半透
    s = pygame.Surface((width,height))  # the size of your rect
    s.set_alpha(150)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
    restart_button.draw()
    exit_button.draw()
topsize=100
tilesize=150
stripsize=20
height=4*tilesize+5*stripsize+topsize
width=4*tilesize+5*stripsize
buttonwidth=155
buttonheight=70
y_diff=10
restart_button=Button((200,200,200),(255,255,255),width/2-buttonwidth/2,height/2-buttonheight-y_diff,buttonwidth,buttonheight,"Restart")
exit_button=Button((200,200,200),(255,255,255),width/2-buttonwidth/2,height/2+y_diff,buttonwidth,buttonheight,"Exit")
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("2048")
clock=pygame.time.Clock()
board=init()
score=0
font=pygame.font.Font(None,36)
big_font=pygame.font.SysFont("gurmukhi",80)
score_font=pygame.font.Font(None,24)
running=True
block_colors = {
    0: (205, 193, 180),      # Empty tile
    2: (238, 228, 218),      # Light beige
    4: (237, 224, 200),      # Beige
    8: (242, 177, 121),      # Light orange
    16: (245, 149, 99),      # Darker orange
    32: (246, 124, 95),      # Reddish-orange
    64: (246, 94, 59),       # Red
    128: (237, 207, 114),    # Yellow
    256: (237, 204, 97),     # Golden yellow
    512: (237, 200, 80),     # Gold
    1024: (237, 197, 63),    # Dark gold
    2048: (237, 194, 46),    # Deep gold
    4096: (60, 58, 50),      # Dark grayish
    8192: (40, 38, 30),      # Darker gray
    16384: (20, 18, 10),     # Almost black
    32768: (0, 0, 0),        # Black
    65536: (255, 0, 0),      # Bright red (custom for extreme cases)
}

if not isfile("score.txt"):
    with open("score.txt","w") as f:
        f.write('0')
with open("score.txt","r") as f:
    hs=int(f.read())

m={pygame.K_w:0,pygame.K_UP:0,pygame.K_s:2,pygame.K_DOWN:2,pygame.K_a:1,pygame.K_LEFT:1,pygame.K_d:3,pygame.K_RIGHT:3}

while running:
    screen.fill((250,248,240))
    #motion
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key in m.keys() and not death(board):
                board,s=move(board,m[event.key])
                score+=s
                break
        elif event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            if restart_button.isOver(pos) and death(board):
                score=0
                board=init()
            if exit_button.isOver(pos) and death(board):
                running=False

        

    drawtile(screen,board)
    drawtop(score)
    if death(board):
        draw_death()
        if score>hs:
            with open('score.txt',"w") as f:
                hs=score
                f.write(str(hs))
    pygame.display.flip()
    clock.tick(60)

