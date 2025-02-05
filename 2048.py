import pygame
import random
pygame.init()

# draw  different color
# addblock 
# death
# score 

def move_left(board):
	b=[]
	for line in board:
		newline=[x for x in line if x!=0]
		for i in range(len(newline)-1):
			if newline[i]==newline[i+1]:
				newline[i]*=2
				newline[i+1]=0
		newline=[x for x in newline if x!=0]
		# print("newline",newline)
		line=newline+[0]*(4-len(newline))
		b.append(line)
	return b

def move(board,direction):
	if direction==0: #left
		board=move_left(board)
	elif direction==2: #right
		for i in range(4):
			board[i]=board[i][::-1]
		board=move_left(board)
		for i in range(4):
			board[i]=board[i][::-1]
	elif direction==1: #up
		board2=[[0 for i in range(4)] for j in range(4)]
		for i in range(4):
			for j in range(4):
				board2[j][i]=board[i][j]
		board2=move_left(board2)
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
		board2=move_left(board2)
		for i in range(4):
			board2[i]=board2[i][::-1]
		for i in range(4):
			for j in range(4):
				board[j][i]=board2[i][j]
	board=add_block(board)
	return board

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

def draw(screen,board):
	for i in range(4):
		for j in range(4):
			pygame.draw.rect(screen,(153,153,255),(stripsize*(i+1)+tilesize*i,stripsize*(j+1)+tilesize*j,tilesize,tilesize))
			if board[i][j]!=0:
				text=font.render(str(board[i][j]),True,(0,0,0))
				text_rect = text.get_rect(center=(stripsize*(i+1)+tilesize*i+tilesize//2,stripsize*(j+1)+tilesize*j+tilesize//2))
				screen.blit(text, text_rect)

def init():
	board=[[0 for i in range(4)] for j in range(4)]
	board=add_block(board,2)
	print(board)
	return board

def death(board):
	#0 check
	
	#same
	for i in range(4)
tilesize=150
stripsize=20
height=4*tilesize+5*stripsize
width=4*tilesize+5*stripsize
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("2048")
clock=pygame.time.Clock()
board=init()
font=pygame.font.Font(None,36)
running=True

while running:
	screen.fill((255, 230, 204))
	#motion
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_w or event.key ==pygame.K_UP:
				board=move(board,0)
			elif event.key==pygame.K_s or event.key ==pygame.K_DOWN:
				board=move(board,2)
			elif event.key==pygame.K_a or event.key ==pygame.K_LEFT:
				board=move(board,1)
			elif event.key==pygame.K_d or event.key ==pygame.K_RIGHT:
				board=move(board,3)

		elif event.type==pygame.QUIT:
			running=False

	draw(screen,board)

	pygame.display.flip()
	clock.tick(60)
