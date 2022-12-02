from bitarray import bitarray
from math import floor, sin
import struct


class MD5(object):
    def _init_(self):
        self._string = None
        self._buffers = {
            'A': None,
            'B': None,
            'C': None,
            'D': None,
        }

    def _generate_hash(self, input_string):
        self._buffers = {
            'A': 0x67452301,
            'B': 0xEFCDAB89,
            'C': 0x98BADCFE,
            'D': 0x10325476,
        }
        self._string = input_string
        bit_array = self._string_to_ba()
        extended_ba = self._extend_ba(bit_array)
        #processed_ba = self._process(extended_ba)

        return self._buffers_to_hex()

    def _string_to_ba(self):
        # Converting the input string into a bit array
        ba = bitarray(endian="big")
        ba.frombytes(self._string.encode("utf-8"))
        return ba

    def _extend_ba(self, ba):
        # Saving the original length
        origLength = len(ba)

        # Extending bit array
        ba.append(1)
        while len(ba) % 512 != 448:
            ba.append(0)

        paddedBa = bitarray(endian="little")
        paddedBa.frombytes(ba.tobytes())

        # Input length in 64 bits.
        length = origLength % pow(2, 64)
        lengthBitArray = bitarray(endian="little")
        lengthBitArray.frombytes(struct.pack("<Q", length))

        # Extending the bit array by the length
        result = paddedBa.copy()
        result.extend(lengthBitArray)
        return result

    def _process(self, preprocessedBa):
        # K table
        K = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        # Number of 512 bit chunks 
        N = len(preprocessedBa) // 512
        # Process chunks of 512 bits.
        for chunk_index in range(N):
            # Breaking the chunk into 16 words of 32 bits in list M.
            start = chunk_index * 512
            M = [preprocessedBa[start +
                                (x * 32): start + (x * 32) + 32] for x in range(16)]

            # Convert the bitarrays to integers.
            M = [int.from_bytes(word.tobytes(), byteorder="little")
                 for word in M]

            # Caching A,B,C,D
            A = self._buffers['A']
            B = self._buffers['B']
            C = self._buffers['C']
            D = self._buffers['D']

            for i in range(64):
                if 0 <= i <= 15:
                    s = [7, 12, 17, 22]
                    g = i
                    tmp = self.__F(B, C, D)
                elif 16 <= i <= 31:
                    s = [5, 9, 14, 20]
                    g = ((5 * i) + 1) % 16
                    tmp = self.__G(B, C, D)
                elif 32 <= i <= 47:
                    s = [4, 11, 16, 23]
                    g = ((3 * i) + 5) % 16
                    tmp = self.__H(B, C, D)
                elif 48 <= i <= 63:
                    s = [6, 10, 15, 21]
                    g = (7 * i) % 16
                    tmp = self.__I(B, C, D)

                # Summing all
                tmp = self.__modAdd(tmp, M[g])
                tmp = self.__modAdd(tmp, K[i])
                tmp = self.__modAdd(tmp, A)
                tmp = self.__leftRotate(tmp, s[i % 4])
                tmp = self.__modAdd(tmp, B)

                # Swapping registers
                A, D, C, B = D, C, B, tmp

            # Updating the buffers
            self._buffers['A'] = self.__modAdd(self._buffers['A'], A)
            self._buffers['B'] = self.__modAdd(self._buffers['B'], B)
            self._buffers['C'] = self.__modAdd(self._buffers['C'], C)
            self._buffers['D'] = self.__modAdd(self._buffers['D'], D)

    def _buffers_to_hex(self):
        # Converting buffers to LE and then TO 32-bit HEX
        return b''.join(x.to_bytes(length=4, byteorder='little') for x in self._buffers.values()).hex()

    def __F(self, b: int, c: int, d: int):
        return (b & c) | (~b & d)

    def __G(self, b: int, c: int, d: int):
        return (b & d) | (c & ~d)

    def __H(self, b: int, c: int, d: int):
        return b ^ c ^ d

    def __I(self, b: int, c: int, d: int):
        return c ^ (b | ~d)

    def __leftRotate(self, x: int, n: int):
        return (x << n) | (x >> (32 - n))

    def __modAdd(self, a: int, b: int):
        return (a + b) % pow(2, 32)
