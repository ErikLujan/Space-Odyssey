import pygame, sys, json, os
from funciones import *
from Configuracion import *
from Clases import *
#-------------------------------------------------------------------------------------------------------------------
def reiniciar_juego():
    """
    brief: Reinicia los valores del juego a sus estados iniciales.
    """
    global score, jugador, running, enemigo

    score = 0
    jugador.vida = 100
    running = True

    grupo_enemigos.empty()
    grupo_balas_jugador.empty()
    grupo_jugador.empty()

    # Crear nuevos enemigos
    for _ in range(CANTIDAD_ENEMIGOS):
        nuevo_enemigo = Enemigos(random.randrange(ANCHO_VENTANA, ANCHO_VENTANA + 200), random.randrange(10, ALTO_VENTANA - 50))
        grupo_enemigos.add(nuevo_enemigo)
    grupo_jugador.add(jugador)
#-------------------------------------------------------------------------------------------------------------------
def game_over():
    """
    brief: Muestra la pantalla de Game Over con opciones de volver al menú principal o jugar de nuevo.
    """
    global score, running

    menu_boton = Boton(None, (500, 380), "MENU", obtener_fuente(36), WHITE, LIGHTBLUE)
    jugar_denuevo_boton = Boton(None, (495, 450), "JUGAR DENUEVO", obtener_fuente(26), WHITE, LIGHTBLUE)

    pausar_musica()

    nombre_jugador = None  # Inicializar el nombre del jugador fuera del bucle

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_boton.check_for_input((x, y)):
                    sonido_click.play()
                    # Obtener el nombre del jugador desde la pantalla de ingreso de nombre
                    if nombre_jugador is None:
                        nombre_jugador = pantalla_nickname()
                        actualizar_puntajes(nombre_jugador, score)
                    reiniciar_juego()
                    menu_principal()

                elif jugar_denuevo_boton.check_for_input((x, y)):
                    sonido_click.play()
                    reiniciar_juego()
                    jugar()

        pantalla.fill(COLOR_NEGRO)

        game_over_text = obtener_fuente(42).render("Game Over", True, WHITE)
        text_rect = game_over_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 4))
        pantalla.blit(game_over_text, text_rect)

        score_text = obtener_fuente(34).render(f"Puntaje: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(500, 270))
        pantalla.blit(score_text, score_rect)

        menu_boton.cambiar_color(pygame.mouse.get_pos())
        jugar_denuevo_boton.cambiar_color(pygame.mouse.get_pos())
        menu_boton.update(pantalla)
        jugar_denuevo_boton.update(pantalla)

        pygame.display.flip()
#-------------------------------------------------------------------------------------------------------------------
def pantalla_pausa():
    """
    brief: Muestra la pantalla de pausa durante el juego.
    """
    pausar_musica()
    seguir_ejecutando = True

    while seguir_ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    seguir_ejecutando = False

        pantalla.fill(COLOR_NEGRO)

        pausa_texto = obtener_fuente(42).render("Estas en Pausa", True, WHITE)
        texto_rect = pausa_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 4))
        pantalla.blit(pausa_texto, texto_rect)

        volver_menu_boton = Boton(None, (500, 380), "Volver al Menu", obtener_fuente(26), WHITE, LIGHTBLUE)
        reanudar_boton = Boton(None, (495, 450), "Reanudar Partida", obtener_fuente(26), WHITE, LIGHTBLUE)

        for boton in [volver_menu_boton, reanudar_boton]:
            boton.cambiar_color(pygame.mouse.get_pos())
            boton.update(pantalla)

            if boton.check_for_input(pygame.mouse.get_pos()):
                if boton.text_input == "Volver al Menu":
                    if pygame.mouse.get_pressed()[0]:
                        pygame.mixer.music.unpause()
                        sonido_click.play()
                        menu_principal()
                elif boton.text_input == "Reanudar Partida":
                    if pygame.mouse.get_pressed()[0]:
                        reanudar_musica()
                        sonido_click.play()
                        seguir_ejecutando = False 
                        #return

        pygame.display.flip()
#-------------------------------------------------------------------------------------------------------------------
def jugar():
    """
    brief: Muestra la pantalla de puntajes más altos con los mejores jugadores.
    """
    global score, running, enemigo, jugador
    reproducir_musica("Sonidos/soundtrack.mp3")
    ajustar_volumen_musica(0.2)

    enemigo = Enemigos(300, 10)
    grupo_enemigos.add(enemigo)

    while running:
        reloj.tick(FPS)
        pantalla.blit(background_gameplay, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bala_jugador = Balas(jugador.rect.centerx, jugador.rect.y)
                    grupo_balas_jugador.add(bala_jugador)
                elif event.key == pygame.K_ESCAPE:
                    pantalla_pausa()

        grupo_enemigos.update()
        grupo_jugador.update()
        grupo_balas_jugador.update()
        grupo_balas_enemigos.update()
        grupo_jugador.draw(pantalla)
        grupo_balas_jugador.draw(pantalla)
        grupo_balas_enemigos.draw(pantalla)
        grupo_enemigos.draw(pantalla)

        while len(grupo_enemigos) < CANTIDAD_ENEMIGOS:
            nuevo_enemigo = Enemigos(random.randrange(ANCHO_VENTANA, ANCHO_VENTANA + 200),random.randrange(10, ALTO_VENTANA - 50))
            if not pygame.sprite.spritecollideany(nuevo_enemigo, grupo_enemigos):
                nuevo_enemigo.velocidad_x = 2
                grupo_enemigos.add(nuevo_enemigo)
    
        # Colision de las balas del jugador con el enemigo
        colision_uno = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
        for i in colision_uno:
            score += 10
            enemigo.disparar_enemigos()
            enemigo = Enemigos(300, 10)
            grupo_enemigos.add(enemigo)
            grupo_jugador.add(enemigo)
            explosion = Explosion(i.rect.center)
            grupo_jugador.add(explosion)
            sonido_explosion.set_volume(0.1)
            sonido_explosion.play()

        # Colision de las balas del enemigo con el jugador
        colision_dos = pygame.sprite.spritecollide(jugador, grupo_balas_enemigos, True)
        for j in colision_dos:
            jugador.vida -= 10
            if jugador.vida <= 0:
                game_over()
            explosion1 = Explosion(j.rect.center)
            grupo_jugador.add(explosion1)
            sonido_golpe.set_volume(0.1)
            sonido_golpe.play()
    
        # Colision del jugador con el enemigo
        golpes = pygame.sprite.spritecollide(jugador, grupo_enemigos, False)
        for golpe in golpes:
            jugador.vida -= 100
            enemigos = Enemigos(10, 10)
            grupo_jugador.add(enemigos) 
            grupo_enemigos.add(enemigos)
            if jugador.vida <= 0:
                game_over()

        texto_puntuacion(pantalla, ('  PUNTAJE: ' + str(score) + '  '), 30, ANCHO_VENTANA - 85, 2)
        barra_vida(pantalla, ANCHO_VENTANA - 285, 0, jugador.vida)

        pygame.display.flip()
    pygame.mixer.music.stop()
#-------------------------------------------------------------------------------------------------------------------
def tablon_puntajes():
    """
    brief: Muestra la pantalla de puntajes más altos con los mejores jugadores.
    """
    user_data_file = 'user_data_leaderboard.json'

    def load_user_data():
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as json_file:
                return json.load(json_file)
        return {'users': []}

    user_data = load_user_data()
    user_scores = [(user['nickname'], user['score']) for user in user_data.get('users', [])]

    # Ordenar la lista de puntajes en orden descendente
    user_scores.sort(key=lambda x: x[1], reverse=True)

    while True:
        puntajes_mouse_posicion = pygame.mouse.get_pos()
        pantalla.fill(COLOR_AZUL_OCURO)

        titulo_txt = obtener_fuente(32).render("Jugadores con mas puntos", True, COLOR_BLANCO)
        titulo_rect = titulo_txt.get_rect(center=(ANCHO_VENTANA // 2, 100))
        pantalla.blit(titulo_txt, titulo_rect)

        for i, (user_nickname, score) in enumerate(user_scores[:5]):
            jugador_txt = obtener_fuente(24).render(f"{i + 1}. {user_nickname} - {score} puntos", True, COLOR_BLANCO)
            jugador_rect = jugador_txt.get_rect(center=(ANCHO_VENTANA // 2, 200 + i * 55))
            pantalla.blit(jugador_txt, jugador_rect)

        puntajes_boton_atras = Boton(image=None, pos=(500, 530), text_input="ATRAS", font=obtener_fuente(30), base_color=COLOR_BLANCO, hovering_color=COLOR_VERDE)
        puntajes_boton_atras.cambiar_color(puntajes_mouse_posicion)
        puntajes_boton_atras.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if puntajes_boton_atras.check_for_input(puntajes_mouse_posicion):
                    sonido_click.play()
                    menu_principal()

        pygame.display.update()
#-------------------------------------------------------------------------------------------------------------------
def menu_principal():
    """
    brief: Muestra el menú principal del juego con opciones para jugar, ver puntajes o salir.
    """

    detener_musica()
    reproducir_musica('Sonidos\sountrack_menu.mp3')
    ajustar_volumen_musica(0.1)

    while True:
        pantalla.blit(fondo_menu, (0, 0))
        menu_mouse_posicion = pygame.mouse.get_pos()
        menu_txt = obtener_fuente(80).render("SPACE", True, GOLD3)
        menu_txt_2 = obtener_fuente(65).render("ODYSSEY", True, GOLD3)
        menu_rect = menu_txt.get_rect(center=(500, 80))
        menu_rect_2 = menu_txt_2.get_rect(center=(500, 160))

        boton_jugar = Boton(image=pygame.image.load("assets/Jugar Rect.png"), pos=(500, 270),
                            text_input="JUGAR", font=obtener_fuente(65), base_color=COLOR_BLANCO, hovering_color=LIGHTBLUE)
        boton_puntajes = Boton(image=pygame.image.load("assets/Puntajes Rect.png"), pos=(500, 400),
                            text_input="PUNTAJES", font=obtener_fuente(65), base_color=COLOR_BLANCO, hovering_color=LIGHTBLUE)
        boton_salir = Boton(image=pygame.image.load("assets/Salir Rect.png"), pos=(500, 530),
                            text_input="SALIR", font=obtener_fuente(65), base_color=COLOR_BLANCO, hovering_color=LIGHTBLUE)

        pantalla.blit(menu_txt, menu_rect)
        pantalla.blit(menu_txt_2, menu_rect_2)

        for boton in [boton_jugar, boton_puntajes, boton_salir]:
            boton.cambiar_color(menu_mouse_posicion)
            boton.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.check_for_input(menu_mouse_posicion):
                    sonido_click.play()
                    reiniciar_juego()
                    jugar()
                if boton_puntajes.check_for_input(menu_mouse_posicion):
                    sonido_click.play()
                    tablon_puntajes()
                if boton_salir.check_for_input(menu_mouse_posicion):
                    sonido_click.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
#-------------------------------------------------------------------------------------------------------------------
inicializar()
menu_principal()