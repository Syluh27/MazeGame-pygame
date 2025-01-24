import pygame
import sys
import random
from config import *

# Inicializar Pygame y el mixer para el sonido
pygame.init()
pygame.mixer.init()

# Cargar sonidos
sonido_movimiento = pygame.mixer.Sound(SONIDO_MOVIMIENTO)
sonido_salida = pygame.mixer.Sound(SONIDO_SALIDA)
sonido_pared = pygame.mixer.Sound(SONIDO_PARED)
pygame.mixer.music.load(MUSICA_FONDO)

# Ajustar volúmenes
pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
sonido_movimiento.set_volume(VOLUMEN_MOVIMIENTO)
sonido_pared.set_volume(VOLUMEN_PARED)
sonido_salida.set_volume(VOLUMEN_SALIDA)

# Iniciar la música en bucle
pygame.mixer.music.play(-1)

# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Laberinto")


class Laberinto:
    def __init__(self, ancho=15, alto=15):
        self.ancho = ancho
        self.alto = alto
        self.matriz = self.generar_laberinto()
        self.x_salida, self.y_salida = self.encontrar_salida()

    def generar_laberinto(self):
        matriz = [["#" for _ in range(self.ancho)] for _ in range(self.alto)]
        start_x, start_y = 1, 1
        matriz[start_y][start_x] = "S"
        self.dibujar_camino(start_x, start_y, matriz)
        salida_x, salida_y = random.randint(1, self.ancho - 2), random.randint(1, self.alto - 2)
        matriz[salida_y][salida_x] = "E"
        return matriz

    def dibujar_camino(self, x, y, matriz):
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < self.ancho - 1 and 0 < ny < self.alto - 1 and matriz[ny][nx] == "#":
                matriz[ny][nx] = "."
                matriz[y + dy][x + dx] = "."
                self.dibujar_camino(nx, ny, matriz)

    def encontrar_salida(self):
        for y, fila in enumerate(self.matriz):
            for x, celda in enumerate(fila):
                if celda == "E":
                    return x, y
        return None, None


class Jugador:
    def __init__(self, lab):
        self.x = 1
        self.y = 1
        self.laberinto = lab

    def mover(self, dx, dy):
        nueva_x = self.x + dx
        nueva_y = self.y + dy
        if self.laberinto.matriz[nueva_y][nueva_x] == "#":
            sonido_pared.play()
        else:
            sonido_movimiento.play()
            self.x += dx
            self.y += dy


def dibujar_laberinto(pantalla, lab, jugador):
    for fila in range(len(lab.matriz)):
        for col in range(len(lab.matriz[fila])):
            x = col * ANCHO_CELDA
            y = fila * ALTO_CELDA
            if lab.matriz[fila][col] == "#":
                pygame.draw.rect(pantalla, COLOR_PARED, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif lab.matriz[fila][col] == ".":
                pygame.draw.rect(pantalla, COLOR_CAMINO, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif lab.matriz[fila][col] == "E":
                pygame.draw.rect(pantalla, COLOR_SALIDA, (x, y, ANCHO_CELDA, ALTO_CELDA))

    x = jugador.x * ANCHO_CELDA
    y = jugador.y * ALTO_CELDA
    pygame.draw.rect(pantalla, COLOR_JUGADOR, (x, y, ANCHO_CELDA, ALTO_CELDA))


def mostrar_mensaje(pantalla, mensaje, color, posicion):
    texto = FUENTE.render(mensaje, True, color)

    # Centrar el mensaje en la pantalla
    texto_rect = texto.get_rect(center=(ANCHO // 2, posicion[1]))

    pantalla.blit(texto, texto_rect)


def pantalla_opciones():
    pantalla.fill((0, 0, 0))
    mostrar_mensaje(pantalla, "¡Felicidades! Has encontrado la salida.", (0, 255, 0), (ANCHO // 2, 250))
    mostrar_mensaje(pantalla, "Presiona R para repetir o Q para salir.", (255, 255, 255), (ANCHO // 2, 300))
    pygame.display.flip()
    sonido_salida.play()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    jugar()
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def jugar():
    lab = Laberinto()
    jugador = Jugador(lab)
    corriendo = True
    while corriendo:
        pantalla.fill((0, 0, 0))
        dibujar_laberinto(pantalla, lab, jugador)

        if lab.matriz[jugador.y][jugador.x] == "E":
            pantalla_opciones()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    jugador.mover(0, -1)
                elif evento.key == pygame.K_s:
                    jugador.mover(0, 1)
                elif evento.key == pygame.K_a:
                    jugador.mover(-1, 0)
                elif evento.key == pygame.K_d:
                    jugador.mover(1, 0)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    jugar()
