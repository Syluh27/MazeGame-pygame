import pygame
import sys
import random

# Constantes para la interfaz gráfica
ANCHO_CELDA = 40
ALTO_CELDA = 40
COLOR_PARED = (0, 0, 0)      # Negro
COLOR_CAMINO = (200, 200, 200)  # Gris claro
COLOR_JUGADOR = (0, 255, 0)  # Verde
COLOR_SALIDA = (255, 0, 0)   # Rojo
COLOR_TEXTO = (255, 255, 255) # Blanco para el texto
ANCHO = 800
ALTO = 600

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Laberinto")

# Fuente para mostrar texto
fuente = pygame.font.SysFont('Arial', 30)

# Clase para el Laberinto
class Laberinto:
    def __init__(self, nivel=1, ancho=15, alto=15):
        self.nivel = nivel
        self.ancho = ancho
        self.alto = alto
        self.matriz = self.generar_laberinto()
        self.x_salida, self.y_salida = self.encontrar_salida()

    def generar_laberinto(self):
        # Generar un laberinto aleatorio usando el algoritmo de recursión para laberintos
        matriz = [["#" for _ in range(self.ancho)] for _ in range(self.alto)]
        start_x, start_y = 1, 1
        matriz[start_y][start_x] = "S"  # S de Start
        self.dibujar_camino(start_x, start_y, matriz)
        salida_x, salida_y = random.randint(1, self.ancho - 2), random.randint(1, self.alto - 2)
        matriz[salida_y][salida_x] = "E"  # E de Exit
        return matriz

    def dibujar_camino(self, x, y, matriz):
        """Algoritmo recursivo para generar caminos en el laberinto"""
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Abajo, Arriba, Derecha, Izquierda
        random.shuffle(direcciones)

        for dx, dy in direcciones:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < self.ancho - 1 and 0 < ny < self.alto - 1 and matriz[ny][nx] == "#":
                matriz[ny][nx] = "."  # Marca la celda como parte del camino
                matriz[y + dy][x + dx] = "."  # Marca la celda intermedia como parte del camino
                self.dibujar_camino(nx, ny, matriz)

    def encontrar_salida(self):
        for y, fila in enumerate(self.matriz):
            for x, celda in enumerate(fila):
                if celda == "E":
                    return x, y
        return None, None

# Clase para el Jugador
class Jugador:
    def __init__(self, lab):
        self.x = 1
        self.y = 1
        self.laberinto = lab

    def mover(self, dx, dy):
        nueva_x = self.x + dx
        nueva_y = self.y + dy
        if self.laberinto.matriz[nueva_y][nueva_x] != "#":  # Verifica si no es pared
            self.x += dx
            self.y += dy

# Función para dibujar el laberinto en pantalla
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
                pygame.draw.rect(pantalla, COLOR_PARED, (x, y, ANCHO_CELDA, ALTO_CELDA), 3)

    x = jugador.x * ANCHO_CELDA
    y = jugador.y * ALTO_CELDA
    pygame.draw.rect(pantalla, COLOR_JUGADOR, (x, y, ANCHO_CELDA, ALTO_CELDA))

# Función para mostrar un mensaje en pantalla
def mostrar_mensaje(pantalla, mensaje, color, posicion):
    texto = fuente.render(mensaje, True, color)
    pantalla.blit(texto, posicion)

# Función para la pantalla de inicio
def pantalla_inicio():
    pantalla.fill((0, 0, 0))
    mostrar_mensaje(pantalla, "Bienvenido al Laberinto", (255, 255, 255), (250, 250))
    mostrar_mensaje(pantalla, "Presiona ENTER para empezar", (255, 255, 255), (250, 300))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False  # Comienza el juego

# Función para mostrar el temporizador
def mostrar_temporizador(pantalla, tiempo_inicial):
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial
    minutos = (tiempo_transcurrido // 60000) % 60
    segundos = (tiempo_transcurrido // 1000) % 60
    tiempo = f"{minutos:02}:{segundos:02}"
    mostrar_mensaje(pantalla, f"Tiempo: {tiempo}", (255, 255, 255), (10, 10))

# Función para mostrar el menú de opciones después de completar el laberinto
def pantalla_opciones():
    pantalla.fill((0, 0, 0))
    mostrar_mensaje(pantalla, "¡Felicidades! Has encontrado la salida.", (0, 255, 0), (200, 250))
    mostrar_mensaje(pantalla, "Presiona R para repetir o Q para salir.", (255, 255, 255), (200, 300))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False  # Reinicia el juego
                    jugar()
                elif evento.key == pygame.K_q:
                    esperando = False  # Sale del juego
                    pygame.quit()
                    sys.exit()

# Función principal del juego
def jugar():
    pantalla_inicio()  # Pantalla de inicio

    nivel = 1  # Iniciar en nivel 1
    lab = Laberinto(nivel)
    jugador = Jugador(lab)

    corriendo = True
    tiempo_inicial = pygame.time.get_ticks()  # Iniciar temporizador
    while corriendo:
        pantalla.fill((0, 0, 0))  # Fondo negro
        dibujar_laberinto(pantalla, lab, jugador)
        mostrar_temporizador(pantalla, tiempo_inicial)  # Mostrar el temporizador

        if lab.matriz[jugador.y][jugador.x] == "E":  # Si llega a la salida
            pantalla_opciones()  # Mostrar opciones de reiniciar o salir

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    jugador.mover(0, -1)  # Arriba
                elif evento.key == pygame.K_s:
                    jugador.mover(0, 1)   # Abajo
                elif evento.key == pygame.K_a:
                    jugador.mover(-1, 0)  # Izquierda
                elif evento.key == pygame.K_d:
                    jugador.mover(1, 0)   # Derecha
                elif evento.key == pygame.K_q:
                    corriendo = False  # Salir del juego

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    jugar()
