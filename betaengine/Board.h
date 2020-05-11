#pragma once

#include <string>
#include <vector>

#include "Types.h"


typedef U16 Move;
namespace Movevar {
	const U16 OGSQ = 0x003F;	// Origin square (bits 0-5)
	const U16 DTSQ = 0x0FC0;	// Destination square (bits 6-11)
	const U16 CAST = 0x3000;	// Castling (bits 12-13)
	const U16 PROM = 0xC000;	// Promotion (bits 14-15)

	const U16 KSCAST = 0x1000;	// Enroc curt		| AIXO VA A L'ESPAI DE CASTLING
	const U16 QSCAST = 0x2000;	// Enroc llarg		|

	const U16 WHCAST = 0x0040;	// Enroc del blanc  | AIXO VA A L'ESPAI DE DESTINACIO
	const U16 BKCAST = 0x0080;	// Enroc del negre  |

	const U16 QUEENPROM = 0x0000;	// Promocio a dama		->  Si un peo acaba a vuitena es considera
	const U16 ROOKPROM	= 0x4000;	// Promocio a torre			el cas de coronacio i es recupera la
	const U16 BSHPPROM  = 0x8000;	// Promocio a alfil			peça en questio
	const U16 KNGHTPROM	= 0xC000;	// Promocio a cavall

	inline int  getOriginSquare(Move move)		{ return (int)(move & OGSQ); }
	inline int  getDestinationSquare(Move move)	{ return (int)((move & DTSQ) >> 6); }

	inline void setOriginSquare(Move& move, int origin) { move |= (origin & OGSQ); }
	inline void setDestinationSquare(Move& move, int destination) { move |= ((destination << 6) & DTSQ); }
	inline void setCastling(Move& castling, U16 castling_type, U16 color) { castling |= castling_type; castling |= color; }
}

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
	inline void setEnpassantSquare(int square) { m_status = m_status & ~EPS; m_status |= (((square & 0x003F) << 4) & EPS); }
	inline U8	getEnpassantSquare()		   { return (m_status & EPS) >> 4; }

	/////////// Metodes ///////////
	inline int  rowcol2index(int row, int col)	{ return (row << 3) | col; }
	inline void index2rowcol(int index, int& row, int& col) { row = (index & 0x0FC0) >> 3; col = (index & 0x003F); }

	void initialize_magicboards();	// Inicialitza les taules precalculades
	void show();					// Printar el tauler

	U64 wpawn_moves();				// Moviments de peons blancs
	U64 bpawn_moves();				// Moviments de peons negres

	U64 bishp_moves(U64 blockers, int square);	// Moviments d'Alfil
	U64 rook_moves(U64 blockers, int square);	// Moviments de Torre

	std::vector<Move> get_moves();	// Generacio de moviments del torn actual

public:
	// UTILITZA LERF MAPPING (Little Endian Row File, o dit altrament, bit menys significatiu
	// identificat amb index menys significatiu i numerant les caselles per files)

	// FILA
	// ...         
	// 4|			INDEX
	// 3| ...
	// 2| 08 09 10 11 12 13 14 15
	// 1| 00 01 02 03 04 05 06 07
	// -+------------------------
	//  |  a  b  c  d  e  f  g  h  COLUMNA

	// Status
	// +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
	// |15 |14 |13 |12 |11 |10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
	// +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
	// |     Buits     | Torn  |     Casella al Pas    |    Enrocs     |
	// +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

	// Constants de treball
	static const U16 WKC = 0x0001;		// Enroc curt del blanc
	static const U16 WQC = 0x0002;		// Enroc llarg del blanc
	static const U16 BKC = 0x0004;		// Enroc curt del negre
	static const U16 BQC = 0x0008;		// Enroc curt del negre

	static const U16 WC = WKC | WQC;	// Enroc blanc en general
	static const U16 BC = BKC | BQC;	// Enroc negre en general

	static const U16 EPS = 0x03F0;		// Mascara per extreure la casella al pas
	static const U16 TRN = 0x0C00;		// Mascara per extreure el torn de joc

	static const U16 TRN_WHT = 0x0400;	// Mascara per veure si es torn del blanc
	static const U16 TRN_BLK = 0x0800;	// Mascara per veure si es torn del negre

	// Inicialitzacions
	static const U64 INIT_WP = 0x000000000000ffff;	// Inicialitzacio de peces blanques
	static const U64 INIT_BP = 0xffff000000000000;	// Inicialitzacio de peces negres
	static const U64 INIT_K  = 0x1000000000000010;	// Inicialitzacio de reis
	static const U64 INIT_Q  = 0x0800000000000008;	// Inicialitzacio de dames
	static const U64 INIT_R  = 0x8100000000000081;	// Inicialitzacio de torres
	static const U64 INIT_B  = 0x2400000000000024;	// Inicialitzacio d'alfils
	static const U64 INIT_N  = 0x4200000000000042;	// Inicialitzacio de cavalls
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