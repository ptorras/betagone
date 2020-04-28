#include "Board.h"

int main()
{
	Board test_board;
	Board newboard;

	test_board.setEnpassantSquare(32);
	std::cout << static_cast<int>(test_board.getEnpassantSquare()) << std::endl;

	for (int i = 0; i < 64; i++)
	{
		U64show(test_board.m_knight_moves[i]);
	}

	test_board.show();

	return 0;
}