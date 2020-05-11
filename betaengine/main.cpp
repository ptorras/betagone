#include "Board.h"

int main()
{
	Board test_board;
	Board newboard;

	test_board.setEnpassantSquare(32);
	test_board.m_wpieces = 0x00000300000000ff;
	test_board.m_pwn	 = 0x0004030000000000;
	test_board.m_bpieces = 0xff04000000000000;
	test_board.show();
	std::cout << "Test bitscan_fw: " << bitscan_forward(0x00000300000000ff) << std::endl;
	std::cout << "Test bitscan_fw: " << bitscan_forward(0x0004030000000000) << std::endl;
	std::cout << "Test bitscan_rv: " << bitscan_reverse(0x0004030000000000) << std::endl;
	std::cout << "Test bitscan_rv: " << bitscan_reverse(0x0004030000000000) << std::endl;

	std::cout << std::endl << std::endl;
	std::vector<Move> testmove = test_board.get_moves();

	test_board.show();

	return 0;
}