from typing import List
from .aes_utilities import *

State = List[List[int]]  # 4x4 matrix of bytes
Key = List[List[int]]    # 4x4 matrix of bytes

def add_round_key(state: State, key: Key) -> None:
    """XOR the state matrix with the round key matrix (in-place)."""
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]


def sub_bytes(state: State) -> None:
    """Substitute each byte in the state with its corresponding S-box value (in-place)."""
    for i in range(4):
        for j in range(4):
            state[i][j] = Sbox[state[i][j]]


def shift_rows(s: State) -> None:
    """Cyclically shift the rows of the state to the left by their row index (in-place)."""
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def mix_single_column(a: List[int]) -> None:
    """Mix one column of the state using the AES MixColumns transformation (in-place)."""
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(state: State) -> None:
    """Apply the MixColumns transformation to each column of the state (in-place)."""
    for i in range(4):
        mix_single_column(state[i])


def inv_shift_rows(s: State) -> None:
    """Inverse cyclically shift the rows of the state to the right by their row index (in-place)."""
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def inv_sub_bytes(state: State) -> None:
    """Substitute each byte in the state with its corresponding inverse S-box value (in-place)."""
    for i in range(4):
        for j in range(4):
            state[i][j] = InvSbox[state[i][j]]


def inv_mix_columns(state: State) -> None:
    """Apply the inverse MixColumns transformation to each column of the state (in-place)."""
    for i in range(4):
        u = xtime(xtime(state[i][0] ^ state[i][2]))
        v = xtime(xtime(state[i][1] ^ state[i][3]))
        state[i][0] ^= u
        state[i][1] ^= v
        state[i][2] ^= u
        state[i][3] ^= v
    mix_columns(state)
