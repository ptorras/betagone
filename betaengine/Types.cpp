#include "Types.h"

void U64show(U64 bitboard)
{
	for (int row = 0; row < 8; row++)
	{
		U64 mask = 0x0100000000000000 >> row * 8;
		std::cout << 8 - row << "|" ;
		for (int col = 0; col < 8; col++)
		{
			std::cout << static_cast<char>((0 != (mask & bitboard)) * ('0'-'.') + '.') << ' ';
			mask = mask << 1;
		}
		std::cout << std::endl;
	}
	std::cout << "-+---------------" << std::endl;
	std::cout << " |a b c d e f g h" << std::endl << std::endl;
}


#ifdef _WIN64

inline int bitscan_forward(U64 bitboard)
{
	assert(bitboard);
	unsigned long value = 0;
	_BitScanForward64(&value, bitboard);
	return (int)(value);
}

inline int bitscan_reverse(U64 bitboard)
{
	assert(bitboard);
	unsigned long value = 0;
	_BitScanReverse64(&value, bitboard);
	return (int)(value);
}

#else

inline int bitscan_forward(U64 bitboard)
{
	assert(bitboard);
	return (int)(_CountLeadingZeros64(bitboard);
}

inline int bitscan_reverse(U64 bitboard)
{
	assert(bitboard);
	unsigned long value = 0;
	_BitScanReverse64(&value, bitboard);
	return (int)(value);
}

#endif