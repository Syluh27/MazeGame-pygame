class Laberinto:
    def __init__(self):
        self.matriz = [
            list("##########"),
            list("#P.......#"),
            list("#.####.#.#"),
            list("#.#..#.#.#"),
            list("#.#.##.#.#"),
            list("#.#....#E#"),
            list("##########")
        ]

    def es_pared(self, x, y):
        return self.matriz[y][x] == "#"
