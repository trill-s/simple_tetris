import pygame
import random
import math
import copy

W, H = 15, 20
TILE = 40
GAME_RES = W * TILE+5*TILE, H * TILE
FPS = 60
anim_cnt_l, anim_cnt_r, anim_speed, anim_limit_l, anim_limit_r = 0, 0, 60, 2000, 2000
acc_limit = 200

pygame.init()
game_sc = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()
field = []
score = 0

class Block:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
        ]

    def __init__(self,_lr):
    	self.lr = _lr
    	if _lr == 0:
    		self.x = 3*TILE
    	elif _lr == 1:
    		self.x = 8*TILE
    	self.y = 0
    	self.type = random.randint(0,len(self.figures)-1)
    	self.rotation = 0

    def image(self):
    	return self.figures[self.type][self.rotation]

    def coords(self):
    	return [[self.x+i%4*TILE,self.y+math.floor(i/4)*TILE] for i in self.image()]

    def rotate(self):
    	self.rotation = (self.rotation+1)%len(self.figures[self.type])

    def rotate_back(self):
    	self.rotation = (self.rotation-1)%len(self.figures[self.type])

    def collides_with_left_border(self):
    	for x,y in self.coords():
    		if x < 0:
    			return True
    		else:
    			continue
    	return False

    def collides_with_right_border(self):
    	for x,y in self.coords():
    		if x >= W*TILE:
    			return True
    		else:
    			continue
    	return False

    def collides_down(self):
    	for x,y in self.coords():
    		if y >= H*TILE or [x,y] in field:
    			return True
    		else:
    			continue
    	return False

    def collides_up(self):
    	for x,y in self.coords():
    		if y <= 0:
    			return True
    	return False

    def collides_figure(self, other_figure):
    	for x,y in self.coords():
    		if [x,y] in other_figure.coords():
    			return True
    	return False

score_font = pygame.font.Font(pygame.font.get_default_font(), 20)
message_font = pygame.font.Font(pygame.font.get_default_font(), 30)

first_round = True
newBlock_l = True
newBlock_r = True
ends = False
while True:
	if not ends:
		if newBlock_l == True:
			anim_speed += 1
			if first_round:
				next_figure_l = Block(0)
				anim_speed = 60
			figure_l = copy.deepcopy(next_figure_l)
			next_figure_l = Block(0)
			limit_l = anim_limit_l
			newBlock_l = False

		if newBlock_r == True:
			anim_speed += 1
			if first_round:
				next_figure_r = Block(1)
				first_round = False
			figure_r = copy.deepcopy(next_figure_r)
			next_figure_r = Block(1)
			limit_r = anim_limit_r
			newBlock_r = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					figure_l.x -= TILE
					if figure_l.collides_with_left_border() or figure_l.collides_down() or figure_l.collides_figure(figure_r):
						figure_l.x += TILE
				elif event.key == pygame.K_d:
					figure_l.x += TILE
					if figure_l.collides_with_right_border()  or figure_l.collides_down() or figure_l.collides_figure(figure_r):
						figure_l.x -= TILE
				elif event.key == pygame.K_w:
					figure_l.rotate()
					if figure_l.collides_with_left_border() or figure_l.collides_with_right_border() or figure_l.collides_down() or figure_l.collides_figure(figure_r):
						figure_l.rotate_back()
				elif event.key == pygame.K_s:
					limit_l = acc_limit
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					figure_r.x -= TILE
					if figure_r.collides_with_left_border() or figure_r.collides_down() or figure_r.collides_figure(figure_l):
						figure_r.x += TILE
				elif event.key == pygame.K_RIGHT:
					figure_r.x += TILE
					if figure_r.collides_with_right_border()  or figure_r.collides_down() or figure_r.collides_figure(figure_l):
						figure_r.x -= TILE
				elif event.key == pygame.K_UP:
					figure_r.rotate()
					if figure_r.collides_with_left_border() or figure_r.collides_with_right_border() or figure_r.collides_down() or figure_r.collides_figure(figure_l):
						figure_r.rotate_back()
				elif event.key == pygame.K_DOWN:
					limit_r = acc_limit


		#go down
		anim_cnt_l += anim_speed
		anim_cnt_r += anim_speed
		if anim_cnt_l>=limit_l:
			figure_l.y+=TILE
			anim_cnt_l=0
			if figure_l.collides_figure(figure_r):
				figure_l.y-=TILE
			#block rests
			if figure_l.collides_down():
				figure_l.y -= TILE
				for x,y in figure_l.coords():
					field.append([x,y])
					newBlock_l = True

					if figure_l.collides_up():
						ends = True

					#if any row is full
					for y in range(H):
						isempty = False
						for x in range(W):
							if [x*TILE,y*TILE] in field:
								isempty = False
							else:
								isempty = True
								break
						if not isempty:
							score+=10
							for x in range(W):
								field.remove([x*TILE,y*TILE])
							for j in range(y-1, -1, -1):
								for i in range(W):
									if [i*TILE,j*TILE] in field:
										field.remove([i*TILE,j*TILE])
										field.append([i*TILE, j*TILE+TILE])
		if anim_cnt_r>=limit_r:
			figure_r.y+=TILE
			anim_cnt_r=0
			if figure_r.collides_figure(figure_l):
				figure_r.y-=TILE
			if figure_r.collides_down():
				figure_r.y -= TILE
				for x,y in figure_r.coords():
					field.append([x,y])
					newBlock_r = True

					if figure_r.collides_up():
						ends = True

					#if any row is full
					for y in range(H):
						isempty = False
						for x in range(W):
							if [x*TILE,y*TILE] in field:
								isempty = False
							else:
								isempty = True
								break
						if not isempty:
							score+=10
							for x in range(W):
								field.remove([x*TILE,y*TILE])
							for j in range(y-1, -1, -1):
								for i in range(W):
									if [i*TILE,j*TILE] in field:
										field.remove([i*TILE,j*TILE])
										field.append([i*TILE, j*TILE+TILE])
	else:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
				field = []
				score = 0
				ends = False
				newBlock_l = True
				newBlock_r = True
				first_round = True

	game_sc.fill(pygame.Color('black'))

	#draw grid
	for x in range(W):
		for y in range(H):
			rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
			pygame.draw.rect(game_sc, (40,40,40), rect, 1)

	#draw field
	for x,y in field:
		field_rect = pygame.Rect(x, y, TILE, TILE)
		pygame.draw.rect(game_sc, 'white', field_rect)

	#draw figures
	for i in range(4):
		figure_l_rect = pygame.Rect(figure_l.coords()[i][0], figure_l.coords()[i][1], TILE, TILE)
		pygame.draw.rect(game_sc, 'pink', figure_l_rect)
	for i in range(4):
		figure_r_rect = pygame.Rect(figure_r.coords()[i][0], figure_r.coords()[i][1], TILE, TILE)
		pygame.draw.rect(game_sc, 'gray', figure_r_rect)

	#draw next
	for i in range(4):
		next_l_rect = pygame.Rect(W*TILE+2*TILE+0.5*(next_figure_l.coords()[i][0]-(W/2-2)*TILE), 0.5*(TILE+TILE+next_figure_l.coords()[i][1]), TILE/2, TILE/2)
		pygame.draw.rect(game_sc, 'pink', next_l_rect)
	for i in range(4):
		next_r_rect = pygame.Rect(W*TILE+4*TILE+0.5*(next_figure_l.coords()[i][0]-(W/2-2)*TILE), 0.5*(TILE+TILE+next_figure_l.coords()[i][1]), TILE/2, TILE/2)
		pygame.draw.rect(game_sc, 'white', next_r_rect)

	#draw message
	if ends:
		message_surface1 = message_font.render(f"Scored {score}.",True,"pink","black")
		game_sc.blit(message_surface1,dest=(TILE,H/2*TILE-TILE))

		message_surface2 = message_font.render("Hit return to start again.",True,"pink","black")
		game_sc.blit(message_surface2,dest=(TILE,H/2*TILE+TILE))

	score_surface = score_font.render(f"{score}",True,"pink")
	game_sc.blit(score_surface,dest=(W*TILE+2.3*TILE,(H-1)*TILE))

	pygame.display.flip()
	clock.tick(FPS)