from stockfish_hook.Wrapper import Wrapper
from betavision import *
import matplotlib.pyplot as plt

def main():
    # Generar l'objecte de visio

    # Generar el motor de joc
    engine = Wrapper("./stockfish_hook/stockfish-11-win/Windows/stockfish_20011801_x64.exe", 1)

    # Generar l'objecte de control

    # Carregar els fitxer de test corresponent
    test = "00003"

    board_image_prior = plt.imread("./betatest/tests/" + test + "_prior.png")
    board_image_post = plt.imread("./betatest/tests/" + test + "_post.png")

    with open("./betatest/tests/" + test + "_prior.fen") as file_fen:
        board_fen_prior = file_fen.read()

    with open("./betatest/tests/" + test + "_post.fen") as file_fen:
        board_fen_post = file_fen.read()

    plt.figure()
    plt.imshow(board_image_prior)
    plt.show()

    plt.figure()
    plt.imshow(board_image_post)
    plt.show()

    # Detectar la posicio del tauler

    # Verificar que les posicions son compatibles

    # Calcular la millor jugada

    # Calcular la ruta a seguir

    # Fer la ruta


if __name__ == "__main__":
    main()