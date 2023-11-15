import pygame
from constantes import *
from Clases import *

pygame.mixer.init()

background_gameplay = pygame.image.load('assets\\background_gameplay.png')
sonido_disparo = pygame.mixer.Sound('Sonidos\laser.wav')
sonido_explosion = pygame.mixer.Sound('Sonidos\explosion.wav')
sonido_golpe = pygame.mixer.Sound('Sonidos\golpe.wav')
sonido_click = pygame.mixer.Sound('Sonidos\click_sound.mp3')
icono = pygame.image.load("assets\icon.png")

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Space Odyssey")
pygame.display.set_icon(icono)
fondo_menu = pygame.image.load("assets/gui_background.png")

CANTIDAD_ENEMIGOS = 5

running = True
FPS = 60
reloj = pygame.time.Clock()
score = 0
vida = 100

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

jugador = Jugador()
grupo_jugador.add(jugador)
grupo_balas_jugador.add(jugador)

def texto_puntuacion(frame, text, size, x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, WHITE, BLACK)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame, text_rect)

def barra_vida(frame, x,y, nivel):
	longitud = 100
	alto = 20
	fill = int((nivel/100)*longitud)
	border = pygame.Rect(x,y, longitud, alto)
	fill = pygame.Rect(x,y,fill, alto)
	pygame.draw.rect(frame, (255,0,55),fill)
	pygame.draw.rect(frame, COLOR_GRIS, border,4)