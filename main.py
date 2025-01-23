import curses
import sys
import time
from laberinto import Laberinto
from jugador import Jugador

def jugar(stdscr):
    """Función principal del juego."""
    curses.curs_set(0)  # Oculta el cursor en la terminal
    stdscr.nodelay(1)   # Permite que getch() no bloquee la ejecución
    stdscr.timeout(100) # Refresca la pantalla cada 100ms

    lab = Laberinto()
    jugador = Jugador(lab)

    while True:
        stdscr.clear()

        # Borra la posición anterior del jugador, cambiándola a un espacio vacío.
        lab.matriz[jugador.y][jugador.x] = "."

        # Actualiza el laberinto en la pantalla
        for fila in range(len(lab.matriz)):
            for col in range(len(lab.matriz[fila])):
                if fila == jugador.y and col == jugador.x:
                    stdscr.addstr(fila, col, "P")  # Marca la posición del jugador
                else:
                    stdscr.addstr(fila, col, lab.matriz[fila][col])  # Resto del laberinto

        stdscr.addstr("\nUsa W (arriba), A (izquierda), S (abajo), D (derecha) para moverte. Presiona Q para salir.")

        tecla = stdscr.getch()  # Espera una tecla

        if tecla == ord("w"):
            jugador.mover(0, -1)  # Arriba
        elif tecla == ord("s"):
            jugador.mover(0, 1)   # Abajo
        elif tecla == ord("a"):
            jugador.mover(-1, 0)  # Izquierda
        elif tecla == ord("d"):
            jugador.mover(1, 0)   # Derecha
        elif tecla == ord("q"):
            print("¡Juego terminado!")
            sys.exit()

        # Verifica si el jugador llegó a la salida
        if lab.matriz[jugador.y][jugador.x] == "E":
            stdscr.clear()
            for fila in lab.matriz:
                stdscr.addstr("".join(fila) + "\n")
            stdscr.addstr("\n🎉 ¡Felicidades! Has encontrado la salida del laberinto. 🎉\n")
            stdscr.refresh()  # Asegura que la pantalla se actualice
            time.sleep(2)  # Espera 2 segundos antes de salir
            sys.exit()

        stdscr.refresh()  # Actualiza la pantalla después de cada movimiento

if __name__ == "__main__":
    curses.wrapper(jugar)  # Llama a la función con soporte para `curses`
