import tkinter as tk
from Board import *
from PIL import Image, ImageTk
import time
import os

class PlayInterface:
    PIECE_CROP = {
        Board.WKING: (0, 0, 256, 256),
        Board.BKING: (0, 256, 256, 512),
        Board.WQUEEN: (256, 0, 512, 256),
        Board.BQUEEN: (256, 256, 512, 512),
        Board.WBSHP: (512, 0, 768, 256),
        Board.BBSHP: (512, 256, 768, 512),
        Board.WKNGHT: (768, 0, 1024, 256),
        Board.BKNGHT: (768, 256, 1024, 512),
        Board.WROOK: (1024, 0, 1280, 256),
        Board.BROOK: (1024, 256, 1280, 512),
        Board.WPAWN: (1280, 0, 1536, 256),
        Board.BPAWN: (1280, 256, 1546, 512)
    }

    def __init__(self):
        # Main Window Elements
        self.main_window = tk.Tk()
        self.main_window.minsize(width=640, height=480)
        self.main_window.title("BetaEngine Chess Interface")
        self.main_window.iconbitmap(bitmap='./assets/icon64.ico')
        self.main_window.bind('<Configure>', self.onResize)

        # Board
        self.lightsqcolor = "lawn green"
        self.darksqcolor = "DarkOrange3"
        self.bordercolor = "NavajoWhite3"
        self.bgcolor = 'ghost white'

        self.pieceset = Image.open("./assets/chess_set.png")
        self.bpadding = 20
        self.rowpad = self.bpadding
        self.colpad = self.bpadding
        self.reverse = False
        self.board_data = Board()
        self.pieces = []

        self.board_space = tk.Canvas(master=self.main_window,
                                     width=480,
                                     height=480,
                                     highlightthickness=0, bg=self.bgcolor)
        self.board_space.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # Game Info sidebar
        self.game_info = tk.Frame(master=self.main_window,
                                  width=160,
                                  height=480,
                                  highlightthickness=0, bg='red')
        self.game_info.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # Menu Bar
        self.menubar = tk.Menu(master=self.main_window)
        self.filebar = tk.Menu(self.menubar, tearoff=False)
        self.filebar.add_command(label="New Game", command=self.onNewgame)
        self.filebar.add_command(label="Set from FEN", command=self.onSetFen)
        self.filebar.add_command(label="Exit", command=self.onQuit)
        self.menubar.add_cascade(label="File", menu=self.filebar)

        self.boardbar = tk.Menu(self.menubar, tearoff=False)
        self.boardbar.add_checkbutton(label="Reverse Board", command=self.onReverseBoard, variable=self.reverse,
                                      onvalue=True, offvalue=False)
        self.menubar.add_cascade(label="Board", menu=self.boardbar)

        self.main_window.config(menu=self.menubar)

        # Selection
        self.selected_piece = False
        self.selected_square = [0, 0]

        # Perform all this stuff
        self.draw_chessboard()

        self.main_window.mainloop()


    def draw_chessboard(self):
        self.board_space.delete("all")
        self.pieces = []
        self.main_window.update_idletasks()

        dim_x = self.board_space.winfo_width()
        dim_y = self.board_space.winfo_height()

        self.colpad = self.bpadding
        self.rowpad = self.bpadding

        boardsize = min(dim_x, dim_y) - (2 * self.bpadding)
        sqsize = int(boardsize / 8)

        if dim_x > dim_y:
            self.colpad = int((dim_x - boardsize) / 2)
        else:
            self.rowpad = int((dim_y - boardsize) / 2)

        color = 'w'

        # Draw Border
        self.board_space.create_rectangle(self.colpad - self.bpadding, self.rowpad - self.bpadding,
                                          self.colpad + boardsize + self.bpadding, self.rowpad + boardsize + self.bpadding,
                                          fill=self.bordercolor, outline=self.bordercolor)

        # Draw Board
        for row in range(8):
            if self.reverse:
                self.board_space.create_text(self.colpad - (self.bpadding / 2),
                                             self.rowpad + (row * sqsize) + (sqsize / 2), text=str(1 + row))
            else:
                self.board_space.create_text(self.colpad - (self.bpadding / 2),
                                             self.rowpad + (row * sqsize) + (sqsize/2), text=str(8 - row))

            for col in range(8):
                self.board_space.create_rectangle(self.colpad + row * sqsize, self.rowpad + col * sqsize,
                                                  self.colpad + (row+1) * sqsize, self.rowpad + (col+1) * sqsize,
                                                  fill=(self.lightsqcolor if color == 'w' else self.darksqcolor),
                                                  outline=(self.lightsqcolor if color == 'w' else self.darksqcolor))

                if color == 'w': color = 'b'
                else:color = 'w'

            if color == 'w': color = 'b'
            else: color = 'w'

        # Letters for columns
        for i in range(8):
            if self.reverse:
                self.board_space.create_text(self.colpad + (i * sqsize) + (sqsize / 2),
                                             self.rowpad + boardsize + (self.bpadding / 2), text=chr(ord('h') - i))
            else:
                self.board_space.create_text(self.colpad + (i * sqsize) + (sqsize/2),
                                             self.rowpad + boardsize + (self.bpadding/2), text=chr(ord('a') + i))

        # Draw Pieces
        for row in range(8):
            for col in range(8):
                if self.board_data.board[row, col] != Board.EMPTY:
                    current_piece = self.pieceset.crop(self.PIECE_CROP[self.board_data.board[row, col]])
                    current_piece.thumbnail((sqsize, sqsize))
                    current_piece = ImageTk.PhotoImage(current_piece)

                    self.pieces.append(current_piece)

                    ypos = 7 - row if not self.reverse else row
                    self.board_space.create_image(self.colpad + (7-col) * sqsize,
                                                  self.rowpad + ypos * sqsize, image=current_piece, anchor=tk.NW)


    def onNewgame(self):
        self.board_data = Board()
        self.draw_chessboard()
        self.main_window.mainloop()

    def onSetFen(self):
        pass

    def onReverseBoard(self):
        self.reverse = not self.reverse
        self.draw_chessboard()
        self.main_window.mainloop()

    def onResize(self, event):
        self.draw_chessboard()

    def onQuit(self):
        self.main_window.quit()