#include "Board.h"

int main()
{
	Board test_board;
	Board newboard;

	test_board.setEnpassantSquare(32);
	std::cout << static_cast<int>(test_board.getEnpassantSquare()) << std::endl;

	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTH][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTHEAST][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_EAST][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTHEAST][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTH][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTHWEST][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_WEST][63]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTHWEST][63]);

	U64show(test_board.m_king_moves[63]);
	U64show(test_board.m_king_moves[28]);
	U64show(test_board.m_king_moves[40]);

	U64show(test_board.m_knight_moves[63]);
	U64show(test_board.m_knight_moves[28]);
	U64show(test_board.m_knight_moves[40]);

	test_board.show();

	return 0;
}