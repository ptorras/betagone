#include "Board.h"

U64 Board::m_sliding_attacks[][64] = {0};
U64 Board::m_knight_moves[] = {0};
U64 Board::m_king_moves[] = {0};

const U64 Board::m_boardgen_limits[8] = {
		0xffffffffffffff00,		// North
		0xfefefefefefefe00,		// Northeast
		0xfefefefefefefefe,		// East
		0x00fefefefefefefe,		// Southeast
		0x00ffffffffffffff,		// South
		0x007f7f7f7f7f7f7f,		// Southwest
		0x7f7f7f7f7f7f7f7f,		// West
		0x7f7f7f7f7f7f7f00		// Northwest
};

bool Board::m_defined_tables = false;


void Board::initialize_magicboards()
{
	if (m_defined_tables) return;

	// Garantir que els contenidors tenen zeros

	for (int i = 0; i < 64; i++)
	{
		m_knight_moves[i] = 0;
		m_king_moves[i] = 0;

		for (int j = 0; j < 8; j++)
		{
			m_sliding_attacks[j][i] = 0;
		}
	}

	// Calcular els sliding attacks per a cada direccio i casella. Es fa amb un algorisme
	// dumb7fill perque tots dos adjectius apliquen a un servidor

	// No es un algorisme extremadament eficient ni tampoc esta implementat de la millor manera
	// pero aixo es un offset que s'executa nomes un cop al entrar al programa, pel que no te massa
	// sentit que sigui focus de massa esforços

	U64 squaremask = 0x0000000000000001;

	for (int position = 0; position < 64; position++)
	{
		U64 currentmask = squaremask << position;

		// Per a cada direccio es calculen els sliding attacks fins trobar el final del tauler
		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask << (8 * i);					// Operacio de bit twiddling per trobar la casella que pertoqui.
			if (!(auxmask & m_boardgen_limits[DIR_NORTH])) break;	// Si dona la volta o surt del rang que toca, sortir del loop.
			m_sliding_attacks[DIR_NORTH][position] |= auxmask;		// Fer la operacio or.
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask << i;
			if (!(auxmask & m_boardgen_limits[DIR_EAST])) break;
			m_sliding_attacks[DIR_EAST][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask >> (8 * i);
			if (!(auxmask & m_boardgen_limits[DIR_SOUTH])) break;
			m_sliding_attacks[DIR_SOUTH][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask >> i;
			if (!(auxmask & m_boardgen_limits[DIR_WEST])) break;
			m_sliding_attacks[DIR_WEST][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask << (9 * i);
			if (!(auxmask & m_boardgen_limits[DIR_NORTHEAST])) break;
			m_sliding_attacks[DIR_NORTHEAST][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask >> (7 * i);
			if (!(auxmask & m_boardgen_limits[DIR_SOUTHEAST])) break;
			m_sliding_attacks[DIR_SOUTHEAST][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask << (7 * i);
			if (!(auxmask & m_boardgen_limits[DIR_NORTHWEST])) break;
			m_sliding_attacks[DIR_NORTHWEST][position] |= auxmask;
		}

		for (int i = 1; i < 8; i++)
		{
			U64 auxmask = currentmask >> (9 * i);
			if (!(auxmask & m_boardgen_limits[DIR_SOUTHWEST])) break;
			m_sliding_attacks[DIR_SOUTHWEST][position] |= auxmask;

		}
	}

	// Calcul de les caselles de moviment dels cavalls
	for (int pos = 0; pos < 64; pos++)
	{
		/*
		DIRECCIONS
		+---+---+---+---+---+
		|   | 8 |   | 1 |   |	
		+---+---+---+---+---+	Es calculen directament aplicant un or
		| 7 |   |   |   | 2 |   entre la mascara d'atacs i un bitshift
		+---+---+---+---+---+	de cada direccio.
		|   |   | C |   |   |	
		+---+---+---+---+---+	Mateixa idea que dumb7fill en sliding
		| 6 |   |   |   | 3 |	attacks, pero aplicada al cavall
		+---+---+---+---+---+
		|   | 5 |   | 4 |   |
		+---+---+---+---+---+
		  ----> shifts a l'esquerra

		*/
		U64 currentmask = squaremask << pos;
		U64 currentrow = (U64)(0x00000000000000ff) << (8*(pos / 8));

		m_knight_moves[pos] |= (currentmask << 17) & (currentrow << 16) ? (currentmask << 17) : 0;
		m_knight_moves[pos] |= (currentmask << 10) & (currentrow << 8)  ? (currentmask << 10) : 0;
		m_knight_moves[pos] |= (currentmask >> 6)  & (currentrow >> 8)  ? (currentmask >> 6)  : 0;
		m_knight_moves[pos] |= (currentmask >> 15) & (currentrow >> 16) ? (currentmask >> 15) : 0;

		m_knight_moves[pos] |= (currentmask >> 17) & (currentrow >> 16) ? (currentmask >> 17) : 0;
		m_knight_moves[pos] |= (currentmask >> 10) & (currentrow >> 8)  ? (currentmask >> 10) : 0;
		m_knight_moves[pos] |= (currentmask << 6)  & (currentrow << 8)  ? (currentmask << 6)  : 0;
		m_knight_moves[pos] |= (currentmask << 15) & (currentrow << 16) ? (currentmask << 15) : 0;
	}

	// Calcul de les caselles de moviment del rei
	for (int pos = 0; pos < 64; pos++)
	{
		/*
		DIRECCIONS
		+---+---+---+
		| 8 | 1 | 2 |
		+---+---+---+
		| 7 | R | 3 |
		+---+---+---+
		| 6 | 5 | 4 |
		+---+---+---+

		  ----> shifts a l'esquerra
		*/

		U64 currentmask = squaremask << pos;
		U64 currentrow = (U64)(0x00000000000000ff) << (8 * (pos / 8));

		m_king_moves[pos] |= (currentmask << 8) & (currentrow << 8) ? (currentmask << 8) : 0;
		m_king_moves[pos] |= (currentmask << 9) & (currentrow << 8) ? (currentmask << 9) : 0;
		m_king_moves[pos] |= (currentmask << 1) &  currentrow		? (currentmask << 1) : 0;
		m_king_moves[pos] |= (currentmask >> 7) & (currentrow >> 8) ? (currentmask >> 7) : 0;

		m_king_moves[pos] |= (currentmask >> 8) & (currentrow >> 8) ? (currentmask >> 8) : 0;
		m_king_moves[pos] |= (currentmask >> 9) & (currentrow >> 8) ? (currentmask >> 9) : 0;
		m_king_moves[pos] |= (currentmask >> 1) &  currentrow		? (currentmask >> 1) : 0;
		m_king_moves[pos] |= (currentmask << 7) & (currentrow << 8) ? (currentmask << 7) : 0;
	}

	m_defined_tables = true;
}

Board::Board()
{
	m_status = WKC | WQC | BKC | BQC | TRN_WHT;

	m_wpieces = INIT_WP;
	m_bpieces = INIT_BP;

	m_king  = INIT_K;
	m_queen = INIT_Q;
	m_rook  = INIT_R;
	m_bishp = INIT_B;
	m_knght = INIT_N;
	m_pwn   = INIT_P;

	// Nomes en cas de nova construccio
	initialize_magicboards();
}

Board::Board(const Board& board)
{
	m_status = board.m_status;

	m_wpieces = board.m_wpieces;
	m_bpieces = board.m_bpieces;

	m_king  = board.m_king;
	m_queen = board.m_queen;
	m_rook  = board.m_rook;
	m_bishp = board.m_bishp;
	m_knght = board.m_knght;
	m_pwn   = board.m_pwn;
}

Board::Board(std::string fen)
{
	m_status = WKC | WQC | BKC | BQC | TRN_WHT;

	m_wpieces = INIT_WP;
	m_bpieces = INIT_BP;

	m_king  = INIT_K;
	m_queen = INIT_Q;
	m_rook  = INIT_R;
	m_bishp = INIT_B;
	m_knght = INIT_N;
	m_pwn   = INIT_P;
}


Board& Board::operator=(const Board& board)
{
	if (&board != this)
	{
		m_status = board.m_status;

		m_wpieces = board.m_wpieces;
		m_bpieces = board.m_bpieces;

		m_king  = board.m_king;
		m_queen = board.m_queen;
		m_rook  = board.m_rook;
		m_bishp = board.m_bishp;
		m_knght = board.m_knght;
		m_pwn   = board.m_pwn;
	}
	return *this;
}

void Board::show()
{
	int increment = 0;

	for (int row = 0; row < 8; row++)
	{
		U64 mask = 0x0100000000000000 >> (8 * row);
		std::cout << 8 - row << "|";
		for (int col = 0; col < 8; col++)
		{
			if ((m_wpieces | m_bpieces) & mask)
			{
				if		(m_wpieces & mask)	increment = 0; else increment = 'a' - 'A';
				if		(m_king & mask)		std::cout << static_cast<char>('K' + increment);
				else if (m_queen & mask)	std::cout << static_cast<char>('Q' + increment);
				else if (m_rook & mask)		std::cout << static_cast<char>('R' + increment);
				else if (m_bishp & mask)	std::cout << static_cast<char>('B' + increment);
				else if (m_knght & mask)	std::cout << static_cast<char>('N' + increment);
				else if (m_pwn & mask)		std::cout << static_cast<char>('P' + increment);
			}
			else
			{
				std::cout << '.';
			}
		std::cout << ' ';
			mask = mask << 1;
		}
		if (row != 7) std::cout << std::endl;
	}
	std::cout << std::endl << "-+---------------";
	std::cout << std::endl << "#|a b c d e f g h" << std::endl;
}

U64 Board::bpawn_moves()
{
	U64 firstrow = 0x00ff000000000000, moves = 0x0000000000000000, bpawn = m_pwn & m_bpieces;
	U64 acolumn = 0x0101010101010101, hcolumn = 0x8080808080808080, square = 0x0000000000000001;
	U64 freesq = ~(m_wpieces | m_bpieces);

	moves |= (firstrow & bpawn & (freesq << 8) & (freesq << 16)) >> 16;
	moves |= (bpawn >> 8) & freesq;
	moves |= (m_wpieces | (square << getEnpassantSquare())) & ((bpawn & ~acolumn) >> 9);
	moves |= (m_wpieces | (square << getEnpassantSquare())) & ((bpawn & ~hcolumn) >> 7);

	return moves;
}

U64 Board::wpawn_moves()
{
	U64 firstrow = 0x000000000000ff00, moves = 0x0000000000000000, wpawn = m_pwn & m_wpieces;
	U64 acolumn = 0x0101010101010101, hcolumn = 0x8080808080808080, square = 0x0000000000000001;
	U64 freesq = ~(m_wpieces | m_bpieces);

	moves |= (firstrow & wpawn & (freesq >> 8) & (freesq >> 16)) << 16;
	moves |= (wpawn << 8) & freesq;
	moves |= (m_bpieces | (square << getEnpassantSquare())) & ((wpawn & ~acolumn) << 7);
	moves |= (m_bpieces | (square << getEnpassantSquare())) & ((wpawn & ~hcolumn) << 9);

	return moves;
}


std::vector<Move> Board::get_moves()
{
	U64 enemy = 0, ally = 0;

	U64 enemy_attacks	 = 0x0000000000000000;	// Mascara amb totes les caselles atacades per alguna peça rival
	U64 attacking_pieces = 0x0000000000000000;	// Mascara amb la casella de les peces atacants
	U64 block_squares	 = 0x0000000000000000;	// Mascara amb les caselles de bloqueig d'atacs


	int attacks = 0;	// Multiples atacs contra el rei

	if ((m_status & TRN) == TRN_WHT)
	{
		enemy = m_bpieces;
		ally  = m_wpieces;

		enemy_attacks |= (enemy & m_pwn & ~0x0101010101010101) >> 9;
		enemy_attacks |= (enemy & m_pwn & ~0x8080808080808080) >> 7;

		attacking_pieces |= enemy & m_pwn & (m_king & ally << 9);
		attacking_pieces |= enemy & m_pwn & (m_king & ally << 7);

		if (attacking_pieces) attacks += 1;
	}
	else
	{
		enemy = m_wpieces;
		ally  = m_bpieces;

		enemy_attacks |= (enemy & m_pwn & ~0x0101010101010101) << 7;
		enemy_attacks |= (enemy & m_pwn & ~0x8080808080808080) << 9;

		attacking_pieces |= enemy & m_pwn & (m_king & ally >> 9);
		attacking_pieces |= enemy & m_pwn & (m_king & ally >> 7);

		if (attacking_pieces) attacks += 1;
	}

	U64 blockers = ally | enemy;

	// Primer s'han de mirar els possibles atacs contra el rei i 
	// les jugades legals

	U64 kingmask = ally & m_king;
	int kingpos = bitscan_forward(kingmask);

	// Eliminar el rei per considerar les sliding en tot el seu rang
	m_king = m_king & ~kingmask;
	ally   = ally & ~kingmask;

	U64 sliding_mask = 0x0000000000000001;

	for (int i = 0; i < 64; i++)
	{
		if (enemy & sliding_mask & ~m_pwn)	// Casella amb peca enemiga
		{
			// Cavall
			if (enemy & m_knght & sliding_mask & ~m_pwn)
			{
				enemy_attacks |= (m_knight_moves[i] & ~enemy);
				if (enemy_attacks & kingmask)
				{
					attacking_pieces |= sliding_mask;
					attacks += 1;
				}
			}

			// Alfil
			else if (enemy & m_bishp & sliding_mask)
			{
				U64 movemask = bishp_moves(blockers, i);

				movemask = movemask & ~(enemy);	// Verificar que el rival no es pot menjar les seves propies peces

				if (movemask & kingmask)
				{
					attacking_pieces |= sliding_mask;
					attacks += 1;

					// TODO: Calcular mascara de bloquejos

				}
				enemy_attacks |= movemask;
			}

			// Torre
			else if (enemy & m_rook & sliding_mask)
			{
				U64 movemask = rook_moves(blockers, i);

				movemask = movemask & ~(enemy);	// Verificar que el rival no es pot menjar les seves propies peces

				if (movemask & kingmask)
				{
					attacking_pieces |= sliding_mask;
					attacks += 1;

					// TODO: Calcular mascara de bloquejos

				}
				enemy_attacks |= movemask;
			}

			// Dama
			else if (enemy & m_queen & sliding_mask)
			{
				U64 movemask = bishp_moves(blockers, i);
				movemask |= rook_moves(blockers, i);

				movemask = movemask & ~(enemy);	// Verificar que el rival no es pot menjar les seves propies peces

				if (movemask & kingmask)
				{
					attacking_pieces |= sliding_mask;
					attacks += 1;

					// TODO: Calcular mascara de bloquejos

				}
				enemy_attacks |= movemask;
			}

			// Rei
			else if (enemy & m_king & sliding_mask)
			{
				U64 movemask = m_king_moves[i] & ~enemy;
				enemy_attacks |= movemask;

				// el rei no hauria de poder fer escac. Nomes necessitem saber la seva area d'influencia
			}
		}
		sliding_mask = sliding_mask << 1;
	}
	/*
	std::cout << "ATTACK MASK: " << std::endl;
	U64show(enemy_attacks); 
	std::cout << std::endl << "ATTACKING PIECES: " << std::endl;
	U64show(attacking_pieces);
	*/

	// Recolocar el rei a la casella corresponent
	m_king |= kingmask;
	ally |= kingmask;

	std::vector<Move> moves;

	if (attacks > 0)
	{
		// Si el rei esta en jaque, prendre les mesures adients
		if (attacks > 1)
		{
			// Un escac doble nomes es pot evadir movent el rei

		}
		else
		{

		}

	}
	else
	{
		// Sino es pot moure qualsevol peça sempre que no estigui clavada
	}

	
	return moves;
}


U64 Board::bishp_moves(U64 blockers, int square)
{
	U64 movemask = 0x0000000000000000;
	for (int dir = 0; dir < 4; dir++)
	{
		U64 blockade = m_sliding_attacks[2 * dir + 1][square] & blockers;
		if (blockade)
		{
			int block = 0;
			if ((dir * 2 + 1) != DIR_SOUTHEAST && (dir * 2 + 1) != DIR_SOUTHWEST)
			{
				block = bitscan_forward(blockade);
			}
			else
			{
				block = bitscan_reverse(blockade);
			}
			movemask |= m_sliding_attacks[2 * dir + 1][square] & ~(m_sliding_attacks[2 * dir + 1][block]);
		}
		else
		{
			movemask |= m_sliding_attacks[2 * dir + 1][square];
		}
	}
	return movemask;
}

U64 Board::rook_moves(U64 blockers, int square)
{
	U64 movemask = 0x0000000000000000;
	for (int dir = 0; dir < 4; dir++)
	{
		U64 blockade = m_sliding_attacks[2 * dir][square] & blockers;
		if (blockade)
		{
			int block = 0;
			if ((dir * 2) != DIR_SOUTH && (dir * 2) != DIR_WEST)
			{
				block = bitscan_forward(blockade);
			}
			else
			{
				block = bitscan_reverse(blockade);
			}
			movemask |= m_sliding_attacks[2 * dir][square] & ~(m_sliding_attacks[2 * dir][block]);
		}
		else
		{
			movemask |= m_sliding_attacks[2 * dir][square];
		}
	}
	return movemask;
}