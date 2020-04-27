#pragma once

#include <string>
#include <vector>

#include "Types.h"


typedef U16 Move;

class Board
{
public:
	/////////// Constructors ///////////
	Board();
	Board(const Board& board);
	Board(std::string fen);	// Constructor a partir de text FEN

	/////////// Destructors ///////////
	~Board() {}

	/////////// Operadors ///////////
	Board& operator=(const Board& board);

	/////////// Setters & Getters ///////////
	inline void setEnpassantSquare(int square) { m_status = m_status & !(EPS); m_status |= ((square << 4) & EPS); }
	inline U8	getEnpassantSquare()			{ return (m_status & EPS) >> 4; }

	/////////// Metodes ///////////
	void initialize_magicboards();	// Inicialitza les taules precalculades
	void show();					// Printar el tauler


public:
	// UTILITZA LERF MAPPING (Little Endian Row File, o dit altrament, bit menys significatiu
	// identificat amb index menys significatiu i numerant les caselles per files)

	/*
   FILA
	8|
	7|
	6|
	5|          INDEX
	4|
	3| ...
	2| 08 09 10 11 12 13 14 15
	1| 00 01 02 03 04 05 06 07
	-+------------------------
	 |  a  b  c  d  e  f  g  h  COLUMNA
	*/

	// Constants de treball
	static const U16 WKC = 0x0001;		// Enroc curt del blanc
	static const U16 WQC = 0x0002;		// Enroc llarg del blanc
	static const U16 BKC = 0x0004;		// Enroc curt del negre
	static const U16 BQC = 0x0008;		// Enroc curt del negre

	static const U16 WC = WKC | WQC;	// Enroc blanc en general
	static const U16 BC = BKC | BQC;	// Enroc negre en general

	static const U16 EPS = 0x03F0;		// Mascara per extreure la casella al pas
	static const U16 TRN = 0x0C00;		// Mascara per extreure el torn de joc

	static const U16 TRN_WHT = 0x0400;	// Torn del blanc
	static const U16 TRN_WHT = 0x0800;	// Torn del negre

	// Inicialitzacions
	static const U64 INIT_WP = 0x000000000000ffff;	// Inicialitzacio de peces blanques
	static const U64 INIT_BP = 0xffff000000000000;	// Inicialitzacio de peces negres
	static const U64 INIT_K  = 0x1000000000000010;	// Inicialitzacio de reis
	static const U64 INIT_Q  = 0x0800000000000008;	// Inicialitzacio de dames
	static const U64 INIT_R  = 0x8100000000000081;	// Inicialitzacio de torres
	static const U64 INIT_B  = 0x4200000000000024;	// Inicialitzacio d'alfils
	static const U64 INIT_N  = 0x2400000000000042;	// Inicialitzacio de cavalls
	static const U64 INIT_P  = 0x00ff00000000ff00;	// Inicialitzacio de peons

	// Direccions
	static const U8 DIR_NORTH = 0;
	static const U8 DIR_NORTHEAST = 1;
	static const U8 DIR_EAST = 2;
	static const U8 DIR_SOUTHEAST = 3;
	static const U8 DIR_SOUTH = 4;
	static const U8 DIR_SOUTHWEST = 5;
	static const U8 DIR_WEST = 6;
	static const U8 DIR_NORTHWEST = 7;

	// Limits
	static const U64 m_boardgen_limits[8];

	// Taules amb moviments precalculats
	static U64 m_sliding_attacks[8][64];
	static U64 m_knight_moves[64];
	static U64 m_king_moves[64];
	static bool m_defined_tables;

	// Especificacio del torn, la casella al pas i enrocs
	U16 m_status;

	// Bitboards de les peces
	U64 m_wpieces;	// Peces blanques
	U64 m_bpieces;	// Peces blanques

	U64 m_king;		// Reis
	U64 m_queen;	// Dames
	U64 m_rook;		// Torres
	U64 m_bishp;	// Alfils
	U64 m_knght;	// Cavalls
	U64 m_pwn;		// Peons
};