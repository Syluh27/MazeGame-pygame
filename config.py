import pygame

# Configuración de pantalla
ANCHO_CELDA = 40
ALTO_CELDA = 40
ANCHO = 600
ALTO = 600

# Colores
COLOR_PARED = (0, 0, 0)  # Negro
COLOR_CAMINO = (200, 200, 200)  # Gris claro
COLOR_JUGADOR = (0, 255, 0)  # Verde
COLOR_SALIDA = (255, 0, 0)  # Rojo

# Fuente de texto
pygame.font.init()
FUENTE = pygame.font.SysFont('Arial', 30)

# Rutas de sonido
SONIDO_MOVIMIENTO = "assets/move.wav"
SONIDO_SALIDA = "assets/win.wav"
SONIDO_PARED = "assets/wall.wav"
MUSICA_FONDO = "assets/background.ogg"

# Volumen de sonidos
VOLUMEN_MOVIMIENTO = 0.9
VOLUMEN_PARED = 0.5
VOLUMEN_SALIDA = 0.6
VOLUMEN_MUSICA = 0.5
