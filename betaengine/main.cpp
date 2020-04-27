#include "Board.h"

int main()
{
	Board test_board;

	test_board.setEnpassantSquare(32);
	std::cout << U8toint(test_board.getEnpassantSquare()) << std::endl;

	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTH][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTHEAST][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_EAST][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTHEAST][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTH][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_SOUTHWEST][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_WEST][28]);
	U64show(test_board.m_sliding_attacks[test_board.DIR_NORTHWEST][28]);

	test_board.show();

	return 0;
}