#pragma once

#include <string>
#include "Types.h"




class Board
{
public:
	/////////// Constructors ///////////
	// Constructor per defecte
	Board();

	// Constructor de copia
	Board(const Board& board);

	// Constructor a partir de text FEN
	Board(std::string fen);

	/////////// Destructors ///////////
	// Destructor
	~Board();

	/////////// Operadors ///////////
	// Operador d'assignacio
	Board& operator=(const Board& board);


private:
	// Especificacio del torn, la casella al pas i enrocs
	U8 m_torn;		// A qui li toca
	U8 m_enps;		// Casella al pas
	U8 m_castle;	// Simbolitza tots dos enrocs


	// Bitboards de les peces
	U64 m_wpc;		// Peces blanques
	U64 m_bpc;		// Peces negres

	U64 m_king;		// Reis
	U64 m_queen;	// Dames
	U64 m_bishp;	// Alfils
	U64 m_knght;	// Cavalls
	U64 m_pwn;		// Peons
};

