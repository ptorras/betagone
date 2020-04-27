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
	U64 squaremask = 0x0000000000000001;

	for (int position = 0; position < 64; position++)
	{
		U64 currentmask = squaremask << position;
		bool overflow[8] = { true, true, true, true, true, true, true, true };

		for (int i = 1; i < 8; i++)
		{
			for (int ovf = 0; ovf < 8; ovf++)
				if ((currentmask & m_boardgen_limits[ovf]) == false)
					overflow[ovf] = false;

			if (overflow[DIR_NORTH]) m_sliding_attacks[DIR_NORTH][position] |= currentmask << (8 * i);
			if (overflow[DIR_SOUTH]) m_sliding_attacks[DIR_SOUTH][position] |= currentmask >> (8 * i);
			if (overflow[DIR_WEST])  m_sliding_attacks[DIR_WEST][position]  |= currentmask >> i;
			if (overflow[DIR_EAST])  m_sliding_attacks[DIR_EAST][position]  |= currentmask << i;

			if (overflow[DIR_NORTHEAST]) m_sliding_attacks[DIR_NORTHEAST][position] |= currentmask << (9 * i);
			if (overflow[DIR_SOUTHEAST]) m_sliding_attacks[DIR_SOUTHEAST][position] |= currentmask >> (7 * i);
			if (overflow[DIR_NORTHWEST]) m_sliding_attacks[DIR_NORTHWEST][position] |= currentmask << (7 * i);
			if (overflow[DIR_SOUTHWEST]) m_sliding_attacks[DIR_SOUTHWEST][position] |= currentmask >> (9 * i);
		}
	}
	m_defined_tables = true;
}

Board::Board()
{
	m_status = WKC | WQC | BKC | BQC;

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
	m_status = WKC & WQC & BKC & BQC;

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
		std::cout << std::endl;
	}
	std::cout << std::endl << "-+---------------";
	std::cout << std::endl << "#|a b c d e f g h" << std::endl;
}