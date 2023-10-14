This script implements a (11, 5) Hamming-encoding scheme.
This means that 5 parity bits are generated for 11 message (data) bits, producing a codeword
of 16 bits.

The script can be called in two ways:

==== First way: Encode a message word ====
    
    py HammingEncode.py --encode_msg=1 --msg_bits=00110001110

==== Second way: Decode a codeword and correct any single-bit errors or detect any multi-bit errors ====

    py HammingEncode.py --decode_msg=1 --codeword_bits=0010101110101110
