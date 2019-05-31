# coding: utf-8
import pygame
import random

# 子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# 子弹方向
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		self.rect.left, self.rect.right = 0, 0
		self.speed = 10
		self.being = False
		self.stronger = False
	# 改变子弹方向
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')
	# 移动
	def move(self):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3):
			self.being = False

# 我方角色类
class mylead(pygame.sprite.Sprite):
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		self.leads = ['./images/mylead/lead_T1_0.png', './images/mylead/lead_T1_1.png', './images/mylead/lead_T1_2.png']
		self.level = 0
		# 载入
		self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		self.rect = self.lead_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		self.speed = 8
		self.being = True
		self.life = 3
		self.protected = False
		self.bullet = Bullet()
	# 射击
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('mylead class -> direction value error.')
		if self.level == 0:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 1:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 2:
			self.bullet.speed = 12
			self.bullet.stronger = True
		elif self.level == 3:
			self.bullet.speed = 16
			self.bullet.stronger = True
		else:
			raise ValueError('mylead class -> level value error.')
	def up_level(self):
		if self.level < 3:
			self.level += 1
		try:
			self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		except:
			self.lead = pygame.image.load(self.leads[-1]).convert_alpha()
	# 向上
	def move_up(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 0, -1
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		is_move = True
		# 地图顶端
		if self.rect.top < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向下
	def move_down(self, leadGroup, brickGroup, ironGroup, myhome):
     #def move_down(self, leadGroup, brickGroup, ironGroup):
		self.direction_x, self.direction_y = 0, 1
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图底端
		if self.rect.bottom > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向左
	def move_left(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = -1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 96), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 96), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图左端
		if self.rect.left < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向右
	def move_right(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 144), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 144), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图右端
		if self.rect.right > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 死后重置
	def reset(self):
		self.level = 0
		self.protected = False
		self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		self.rect = self.lead_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		self.speed = 8
# 敌方角色类
class enemylead(pygame.sprite.Sprite):
	def __init__(self, x=None, kind=None, is_red=None):
		pygame.sprite.Sprite.__init__(self)
		self.born = True
		self.times = 90
		if kind is None:
			self.kind = random.randint(0, 3)
		else:
			self.kind = kind
		# 所有角色
		self.leads1 = ['./images/enemylead/enemy_1_0.png', './images/enemylead/enemy_1_1.png', './images/enemylead/enemy_1_2.png', './images/enemylead/enemy_1_3.png']
		self.leads2 = ['./images/enemylead/enemy_2_0.png', './images/enemylead/enemy_2_1.png', './images/enemylead/enemy_2_2.png', './images/enemylead/enemy_2_3.png']
		self.leads3 = ['./images/enemylead/enemy_3_0.png', './images/enemylead/enemy_3_1.png', './images/enemylead/enemy_3_2.png', './images/enemylead/enemy_3_3.png']
		self.leads4 = ['./images/enemylead/enemy_4_0.png', './images/enemylead/enemy_4_1.png', './images/enemylead/enemy_4_2.png', './images/enemylead/enemy_4_3.png']
		self.leads = [self.leads1, self.leads2, self.leads3, self.leads4]
		if is_red is None:
			self.is_red = random.choice((True, False, False, False, False))
		else:
			self.is_red = is_red
		if self.is_red:
			self.color = 3
		else:
			self.color = random.randint(0, 2)
		self.blood = self.color
		self.lead = pygame.image.load(self.leads[self.kind][self.color]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
		self.rect = self.lead_0.get_rect()
		if x is None:
			self.x = random.randint(0, 2)
		else:
			self.x = x
		self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
		self.can_move = True
		self.speed = max(3 - self.kind, 1)
		self.direction_x, self.direction_y = 0, 1
		self.being = True
		self.bullet = Bullet()
	# 射击
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('enemylead class -> direction value error.')
	# 随机移动
	def move(self, leadGroup, brickGroup, ironGroup, myhome):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		is_move = True
		if self.direction_x == 0 and self.direction_y == -1:
			self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
			if self.rect.top < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 0 and self.direction_y == 1:
			self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
			if self.rect.bottom > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == -1 and self.direction_y == 0:
			self.lead_0 = self.lead.subsurface((0, 96), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 96), (48, 48))
			if self.rect.left < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 1 and self.direction_y == 0:
			self.lead_0 = self.lead.subsurface((0, 144), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 144), (48, 48))
			if self.rect.right > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		else:
			raise ValueError('enemylead class -> direction value error.')
		if pygame.sprite.spritecollide(self, brickGroup, False, None) \
			or pygame.sprite.spritecollide(self, ironGroup, False, None) \
			or pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		return is_move
	# 重新载入角色
	def reload(self):
		self.lead = pygame.image.load(self.leads[self.kind][self.color]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
