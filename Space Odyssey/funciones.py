import pygame, sys, os, json
from constantes import *
from Configuracion import *
from Clases import *
#-------------------------------------------------------------------------------------------------------------------
def obtener_fuente(tamaño):
    """
    brief: Devuelve una fuente pygame con el tamaño especificado.
    Parametros:
    - tamaño: Tamaño de la fuente.
    Retorna:
    - Objeto de fuente pygame.
    """
    return pygame.font.Font("assets/font.ttf", tamaño)
#-------------------------------------------------------------------------------------------------------------------
def inicializar():
    """
    Inicializa pygame y el mixer de música.
    """
    pygame.init()
    pygame.mixer.init()
#-------------------------------------------------------------------------------------------------------------------
def pantalla_nickname():
    """
    brief: Muestra una pantalla para que el jugador ingrese su nickname.

    Retorna:
    - El nickname ingresado por el jugador.
    """
    inicializar()
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    # Variables
    input_box = pygame.Rect(300, 250, 400, 30)
    color_inactive = pygame.Color(LIGHTSKYBLUE3)
    color_active = pygame.Color(DODGERBLUE2)
    color = color_inactive
    active = False
    text = ''
    user_data_file = 'user_data.json'

    def load_user_data():
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as json_file:
                return json.load(json_file)
        return {'nicknames': []}

    def save_user_data(nickname):
        user_data = load_user_data()
        if 'nicknames' not in user_data:
            user_data['nicknames'] = []
        user_data['nicknames'].append(nickname)
        with open(user_data_file, 'w') as json_file:
            json.dump(user_data, json_file)

    # Ciclo principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif boton_flecha.rect.collidepoint(event.pos):
                    running = False  # Salgo del bucle y termino la funcion
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        save_user_data(text)
                        running = False
                        return text  # Devuelve el nombre del usuario

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(COLOR_AZUL_OCURO)
        
        text_surface = obtener_fuente(20).render("Ingresa tu nickname", True, pygame.Color('white'))
        screen.blit(text_surface, (310, 180))
        text_surface_2 = obtener_fuente(20).render("para guardar tu puntaje", True, pygame.Color('white'))
        screen.blit(text_surface_2, (270, 210))
        
        txt_surface = obtener_fuente(20).render(text, True, color)
        width = max(400, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        boton_flecha = Boton(image=pygame.image.load("Imagenes\\arrow_back.png"), pos=(40, 40),
                                text_input="", font=obtener_fuente(3), base_color=COLOR_BLANCO, hovering_color=LIGHTBLUE)
        boton_flecha.cambiar_color(pygame.mouse.get_pos())
        boton_flecha.update(screen)

        pygame.display.flip()
#-------------------------------------------------------------------------------------------------------------------
def actualizar_puntajes(nickname, score):
    """
    brief: Actualiza los puntajes en el archivo JSON de usuarios.

    Parametros:
    - nickname: Nombre del jugador.
    - score: Puntuación del jugador.
    """
    user_data_file = 'user_data_leaderboard.json'
    def load_user_data():
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as json_file:
                return json.load(json_file)
        return {'users': []}

    def save_user_data(user_data):
        with open(user_data_file, 'w') as json_file:
            json.dump(user_data, json_file)

    user_data = load_user_data()
    users = user_data.get('users', [])
    user_index = next((i for i, user in enumerate(users) if user['nickname'] == nickname), None)

    if user_index is not None:
        if score > users[user_index]['score']:
            users[user_index]['score'] = score
    else:
        users.append({'nickname': nickname, 'score': score})

    users.sort(key=lambda x: x['score'], reverse=True)

    user_data['users'] = users[:5]
    save_user_data(user_data)
#-------------------------------------------------------------------------------------------------------------------
def reproducir_musica(soundtrack):
    """
    brief: Reproduce la música de fondo del juego.

    Parametros:
    - soundtrack: Ruta del archivo de música.
    """
    pygame.mixer.music.load(soundtrack)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
#-------------------------------------------------------------------------------------------------------------------
def pausar_musica():
    """
    brief: Pausa la reproducción de la música.
    """
    pygame.mixer.music.pause()
#-------------------------------------------------------------------------------------------------------------------
def reanudar_musica():
    """
    brief: Reanuda la reproducción de la música.
    """
    pygame.mixer.music.unpause()
#-------------------------------------------------------------------------------------------------------------------
def detener_musica():
    """
    brief: Detiene la reproducción de la música.
    """
    pygame.mixer.music.stop()
#-------------------------------------------------------------------------------------------------------------------
def ajustar_volumen_musica(volumen):
    """
    brief: Ajusta el volumen de la música.

    Parámetros:
    - volumen: Volumen deseado (0.0 - 1.0).
    """
    pygame.mixer.music.set_volume(volumen)