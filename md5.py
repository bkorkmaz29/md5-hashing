from bitarray import bitarray
from math import floor, sin
import struct


class MD5(object):
    def __init__(self):
        self._string = None
        self._buffers = None
    
    def generate_hash(self, input_string):
        # Main function for generating MD5 hash
        self._string = input_string
        self._buffers = {
            'A': 0x67452301,
            'B': 0xEFCDAB89,
            'C': 0x98BADCFE,
            'D': 0x10325476,
        }
        
        # Converting input string to bit array
        bit_array = bitarray(endian="big")
        bit_array.frombytes(self._string.encode("utf-8"))

        padded_ba, og_length = self._pad_ba(bit_array)
        extended_ba = self._extend_ba(padded_ba, og_length)
        self._process(extended_ba)

        return self._buffers_to_hex()
   
    def _pad_ba(self, bit_array):
        # Saving original length of bit array for extending
        original_length = len(bit_array)
        # Extending the bit array with single 1 bit
        bit_array.append(1)
        
        # Padding the bit array until the length is 64 bits fewer than 512
        while len(bit_array) % 512 != 448:
            bit_array.append(0)

        # Converting to little endian for the rest of the algorithm
        padded_ba = bitarray(endian="little")
        padded_ba.frombytes(bit_array.tobytes())
        return padded_ba, original_length

    def _extend_ba(self, bit_array, original_length):
        # Extending the padded bit array with a 64-bit little endian
        # representation of the original message length.
        length = original_length % pow(2, 64)
        ba_length = bitarray(endian="little")
        ba_length.frombytes(struct.pack("<Q", length))

        # Extending the bit array by the length
        result = bit_array.copy()
        result.extend(ba_length)
        return result

    def _process(self, bit_array):
        # Auxiliary functions
        F = lambda b, c, d: (b & c) | (~b & d)
        G = lambda b, c, d: (b & d) | (c & ~d)
        H = lambda b, c, d: b ^ c ^ d
        I = lambda b, c, d: c ^ (b | ~d)
        
        # Modular addition
        mod_add = lambda a, b: (a + b) % pow(2, 32)
        
        # Left rotating x by n bits
        left_rotate = lambda x, n: (x << n) | (x >> (32 - n))
        
        # K table
        K = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        # Number of 512 bit chunks 
        N = len(bit_array) // 512

        # Process chunks of 512 bits.
        for chunk_index in range(N):
            # Breaking the chunk into 16 words of 32 bits in list M.
            start = chunk_index * 512
            M = [bit_array[start 
                                + (x * 32): start + (x * 32) + 32] for x in range(16)]

            # Converting the bitarrays to integers.
            M = [int.from_bytes(word.tobytes(), byteorder="little")
                 for word in M]

            # Initializing hash values for A,B,C,D
            A = self._buffers['A']
            B = self._buffers['B']
            C = self._buffers['C']
            D = self._buffers['D']

            for i in range(64):
                if 0 <= i <= 15:
                    s = [7, 12, 17, 22]
                    g = i
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    s = [5, 9, 14, 20]
                    g = ((5 * i) + 1) % 16
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    s = [4, 11, 16, 23]
                    g = ((3 * i) + 5) % 16
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    s = [6, 10, 15, 21]
                    g = (7 * i) % 16
                    temp = I(B, C, D)

                # Modular addition
                temp = mod_add(temp, M[g])
                temp = mod_add(temp, K[i])
                temp = mod_add(temp, A)
                temp = left_rotate(temp, s[i % 4])
                temp = mod_add(temp, B)

                # Swapping registers for next operation
                A, D, C, B = D, C, B, temp

            # Updating the buffers
            self._buffers['A'] = mod_add(self._buffers['A'], A)
            self._buffers['B'] = mod_add(self._buffers['B'], B)
            self._buffers['C'] = mod_add(self._buffers['C'], C)
            self._buffers['D'] = mod_add(self._buffers['D'], D)
            
    def _buffers_to_hex(self):
        # Converting buffers to little endian then to 32-bit HEX
        return b''.join(x.to_bytes(length=4, byteorder='little') for x in self._buffers.values()).hex()
