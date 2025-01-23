# jugador.py
class Jugador:
    def __init__(self, laberinto):
        self.x = 1  # Posición inicial X
        self.y = 1  # Posición inicial Y
        self.laberinto = laberinto

    def mover(self, dx, dy):
        """ Mueve al jugador si no hay pared en la dirección. """
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        if not self.laberinto.es_pared(nuevo_x, nuevo_y):  # Si no es una pared
            self.x = nuevo_x
            self.y = nuevo_y
