#pragma once

#include <iostream>
#include <cassert>

// Tipus de longitud fixa
#define U64 uint64_t
#define U32 uint32_t
#define U16 uint16_t
#define U8  uint8_t

void U64show(U64 bitboard);

// per a les operacions BSF i BSR fer servir les intrinsics corresponents enmascarades
// en una crida que permeti fer servir la versio arm i la versio windows

inline int bitscan_forward(U64 bitboard);
inline int bitscan_reverse(U64 bitboard);