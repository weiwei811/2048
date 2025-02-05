import pygame
import random
from os.path import isfile

pygame.init()

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
		# print("newline",newline)
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
	if not death(board):
		board=add_block(board)
	return board,s

def add_block(board,n=1):
	empty=[]
	for i in range(4):
		for j in range(4):
			if board[i][j]==0:
				empty.append([i,j])
	r=random.sample(empty,k=n)
	for x,y in r:
		board[x][y]=random.choices([2,4],weights=[0.7,0.3])[0]
	return board

def drawtile(screen,board):
	for i in range(4):
		for j in range(4):

			pygame.draw.rect(screen,block_colors[board[i][j]],(stripsize*(i+1)+tilesize*i,stripsize*(j+1)+tilesize*j+topsize,tilesize,tilesize))
			if board[i][j]!=0:
				text=font.render(str(board[i][j]),True,(0,0,0))
				text_rect = text.get_rect(center=(stripsize*(i+1)+tilesize*i+tilesize//2,stripsize*(j+1)+tilesize*j+tilesize//2+topsize))
				screen.blit(text, text_rect)

def drawtop(score):
	text=big_font.render("2048",True,(0,0,0))
	screen.blit(text, (20,20))


	center=(400,50)
	rectheight=70
	padding=10
	w,h=font.size(str(score))
	pygame.draw.rect(screen,(234,231,218),(center[0]-(w+2*padding)/2,center[1]-rectheight/2,w+2*padding,rectheight))
	
	scoretext=font.render(str(score),True,(0,0,0))
	text_rect = scoretext.get_rect(center=center)
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
	pass

topsize=100
tilesize=150
stripsize=20
height=4*tilesize+5*stripsize+topsize
width=4*tilesize+5*stripsize
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("2048")
clock=pygame.time.Clock()
board=init()
score=0
font=pygame.font.Font(None,36)
big_font=pygame.font.SysFont("gurmukhi",80)
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
		if event.type==pygame.KEYDOWN:
			if event.key in m.keys():
				board,s=move(board,m[event.key])
				score+=s

		elif event.type==pygame.QUIT:
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
