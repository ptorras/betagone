from stockfish_hook.Wrapper import Wrapper
from betavision import *
import matplotlib.pyplot as plt
from betacontrol.Route import Route
import numpy as np


def main():

    # Carregar els fitxer de test corresponent
    test = "00006"

    board_image_prior = plt.imread("../datasets/early-test/" + test + "_prior.png")
    board_image_post = plt.imread("../datasets/early-test/" + test + "_post.png")

    with open("../datasets/positions/" + test + "_prior.fen") as file_fen:
        board_fen_prior = file_fen.read()

    with open("../datasets/positions/" + test + "_post.fen") as file_fen:
        board_fen_post = file_fen.read()

    plt.figure()
    plt.imshow(board_image_prior)
    plt.show()

    plt.figure()
    plt.imshow(board_image_post)
    plt.show()

    # Generar l'objecte de visio


    # Generar el motor de joc
    engine = Wrapper("./stockfish_hook/stockfish-11-win/Windows/stockfish_20011801_x64.exe", 1)

    # Generar l'objecte de control
    route_maker = Route(board_fen_post)
    matrix = route_maker.route_matrix(np.array([2, 3]), np.array([7,8]), True)
    route = route_maker.route_segment(np.array([2, 3]), np.array([7,8]), True)

    print(matrix)

    # Detectar la posicio del tauler



    # Verificar que les posicions son compatibles


    # Calcular la millor jugada
    move = engine.process_position(board_fen_post)
    strmove = engine.translate_move(move)
    print(move)
    engine.shutdown()

    # Calcular la ruta a seguir

    # Fer la ruta


if __name__ == "__main__":
    main()