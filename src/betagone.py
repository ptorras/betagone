from stockfish_hook.Wrapper import Wrapper
from betavision import Vision
import matplotlib.pyplot as plt
from betacontrol.Route import Route
import numpy as np
import cv2

def main():

    # Carregar els fitxer de test corresponent
    test = "00008"

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
    tauler_buit = cv2.imread("../datasets/pieces-full/empty.png")
    vision_object = Vision.PieceDetector(tauler_buit, "./betavision/checkpoints/checkpoint.pth")

    # Generar el motor de joc
    engine = Wrapper("./stockfish_hook/stockfish-11-win/Windows/stockfish_20011801_x64.exe", 1)

    # Generar l'objecte de control
    route_maker = Route(board_fen_post)

    # Detectar la posicio del tauler
    position = vision_object.detect_pieces(board_image_post)

    # Verificar que les posicions son compatibles
    if engine.check_compatible(board_fen_prior, position) is None:
        print("Posicio Incompatible")
        exit(-1)

    # Calcular la millor jugada
    move = engine.process_position(position)
    strmove = engine.translate_move(move)
    engine.move(move)
    print(strmove)
    engine.shutdown()

    # Calcular la ruta a seguir
    ruta, magnet = route_maker.route_calculate(strmove)
    route_maker.draw_route(ruta, board_image_post, magnet)

    # Fer la ruta
    pass

if __name__ == "__main__":
    main()