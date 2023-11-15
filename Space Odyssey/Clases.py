import pygame, sys, random
from constantes import *
from Configuracion import *

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('Imagenes\\nave_jugador.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = ANCHO_VENTANA//2
		self.rect.centery = ALTO_VENTANA-50
		self.velocidad_x = 0
		self.vida = 100

	def update(self):
		self.velocidad_x = 0
		teclas = pygame.key.get_pressed()
		if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
			self.velocidad_x = -5
		elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
			self.velocidad_x = 5

		self.rect.x += self.velocidad_x
		if self.rect.right > ANCHO_VENTANA:
			self.rect.right = ANCHO_VENTANA
		elif self.rect.left < 0:
			self.rect.left = 0

	def disparar(self):
		bala = Balas(self.rect.centerx, self.rect.top)
		grupo_jugador.add(bala)
		grupo_balas_jugador.add(bala)
		sonido_disparo.play()
#-------------------------------------------------------------------------------------------------------------------
class Enemigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/nave_enemigo.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(1, ANCHO_VENTANA-50)
		self.rect.y = random.randrange(-50, -10)
		self.velocidad_y = random.randrange(2,5)
		self.velocidad_x = 2

	def update(self):
		#self.time = random.randrange(-1, pygame.time.get_ticks()//2500)
		self.rect.x += self.velocidad_x
		self.rect.y = self.velocidad_y
		if self.rect.x >= ANCHO_VENTANA or self.rect.y >= ALTO_VENTANA:
			self.rect.x = random.randrange(1, ANCHO_VENTANA - 50)
			self.rect.y = random.randrange(-50, -10)

	def disparar_enemigos(self):
		bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
		grupo_jugador.add(bala)
		grupo_balas_enemigos.add(bala)
		sonido_disparo.play()
#-------------------------------------------------------------------------------------------------------------------
lista_explosion = []
for i in range(1,11):
	explosion = pygame.image.load(f'explosion/{i}.png')
	lista_explosion.append(explosion)

class Explosion(pygame.sprite.Sprite):
	def __init__(self, position):
		super().__init__()
		self.image = lista_explosion[0]
		img_scale = pygame.transform.scale(self.image, (20,20))	
		self.rect = img_scale.get_rect()
		self.rect.center = position
		self.time = pygame.time.get_ticks()
		self.velocidad_explo = 30
		self.frames = 0 
		
	def update(self):
		tiempo = pygame.time.get_ticks()
		if tiempo - self.time > self.velocidad_explo:
			self.time = tiempo 
			self.frames+=1
			if self.frames == len(lista_explosion):
				self.kill()
			else:
				position = self.rect.center
				self.image = lista_explosion[self.frames]
				self.rect = self.image.get_rect()
				self.rect.center = position
#-------------------------------------------------------------------------------------------------------------------
class Balas(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/bala_jugador.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.velocidad = -18

	def update(self):
		self.rect.y +=  self.velocidad
		if self.rect.bottom <0:
			self.kill()
#-------------------------------------------------------------------------------------------------------------------
class Balas_enemigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/bala_enemigo.png').convert_alpha()
		self.image = pygame.transform.rotate(self.image, 180)
		self.rect = self.image.get_rect()
		self.rect.centerx = x 
		self.rect.y = random.randrange(10, ANCHO_VENTANA)
		self.velocidad_y = 4

	def update(self):
		self.rect.y +=  self.velocidad_y 
		if self.rect.bottom > ALTO_VENTANA:
			self.kill()
#-------------------------------------------------------------------------------------------------------------------
class Boton():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def check_for_input(self, posicion):
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def cambiar_color(self, posicion):
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
#-------------------------------------------------------------------------------------------------------------------
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

pygame.mixer.init()
sonido_disparo = pygame.mixer.Sound('Sonidos\laser.wav')