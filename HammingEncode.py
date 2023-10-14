#!/usr/bin/env python3
#
# Author: Dylan Boland
#
# Modules that will be useful
import argparse
import os
import sys
import re
import random
from functools import reduce

# ==== Some General-info Strings ====
# Tags - define these here so they can be quickly and easily changed
errorTag   = """\t***Error: """
successTag = """\t***Success: """
infoTag    = """\t***Info: """

helpMsg    = infoTag + """This script implements a (11, 5) Hamming-encoding scheme.
This means that 5 parity bits are generated for 11 message (data) bits, producing a codeword
of 16 bits.

The script can be called in two ways:

==== First way: Encode a message word ====
    
    py HammingEncode.py --encode_msg=1 --msg_bits=00110001110

==== Second way: decode a codeword and correct any single-bit errors or detect any multi-bit errors ====

    py HammingEncode.py --decode_msg=1 --codeword_bits=0010101110101110
"""

noArgsMsg  = errorTag + """No input arguments were specified."""

noMsgWordSuppliedMsg = errorTag + """No message word was supplied"""

noCodewordSuppliedMsg = errorTag + """No codeword was supplied"""

encodeDecodeArgConflictMsg = errorTag + """The --encode_msg and --decode_msg switches should
not be used at the same time"""

noEncodeDecodeArgSuppliedMsg = """The --encode_msg or --decode_msg switch should be supplied.
If the --encode_msg switch is used, then the --msg_bits switch should also be supplied. An example
of how the script would be called is:
    py HammingEncode.py --encode_msg --msg_bits=<list_of_message_bits>
    
If the --decode_msg switch is used, then the --codeword_bits switch should also be supplied. An example
of how the script would be called in this case is:
    py HammingEncode.py --decode_msg --codeword_bits=<list_of_codeword_bits>"""

encodingDoneMsg = """The message word is: {}

The encoded message (using a Hamming code) is: {}"""

errorInjectionMsg = """Injecting a {} into the codeword"""

singleBitErrorPositionMsg = """Flipping bit {}"""

corruptedCodewordMsg = """The corrupted codeword is {}"""

multiBitErrorPositionMsg = """Flipping bits {} and {}"""

errorIdentifiedMsg = """Bit {} is in error - correcting it"""

multiBitErrorIdentifiedMsg = """The codeword contains multiple errors"""

correctedCodewordMsg = """The corrected codeword is {}"""

retrievedBitsMsg = """The retrieved message bits are {}"""

incorrectMsgWordLen = """The message word supplied does not have the correct number of bits.
It should contain {} bits"""

# Function to handle the input arguments
def parseArguments():
    parser = argparse.ArgumentParser(description = "TODO")
    parser.add_argument('--encode_msg', type = bool, help = helpMsg)
    parser.add_argument('--decode_msg', type = bool, help = helpMsg)
    parser.add_argument('--msg_bits', type = list, help = helpMsg)
    parser.add_argument('--codeword_bits', type = list, help = helpMsg)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArguments() # parse the input arguments (if there are any)
    if len(sys.argv) == 1:
        print(noArgsMsg)
        exit()
    
    # ==== Check if a message is to be encoded ====
    if args.encode_msg:
        encodeMsg = True
        # ==== Check if the message bits have been supplied ====
        if args.msg_bits:
            msgBitsSupplied = True
            msg_bits = [int(i) for i in args.msg_bits]
        else:
            msgBitsSupplied = False
            print(noMsgWordSuppliedMsg)
    else:
        encodeMsg = False
    
    # ==== Check if a message is to be decoded ====
    if args.decode_msg:
        decodeMsg = True
        # ==== Check if the code-word bits have been supplied ====
        if args.codeword_bits:
            codewordBitsSupplied = True
            codeword = [int(i) for i in args.codeword_bits]
        else:
            codewordBitsSupplied = False
            print(noCodewordSuppliedMsg)
    else:
        decodeMsg = False
    
    # ==== Check for Argument Conflicts ====
    if decodeMsg and encodeMsg:
        print(encodeDecodeArgConflictMsg)
        exit()
    elif encodeMsg and not msgBitsSupplied:
        print(noMsgWordSuppliedMsg)
        exit()
    elif decodeMsg and not codewordBitsSupplied:
        print(noCodewordSuppliedMsg)
        exit()
    elif not (encodeMsg or decodeMsg):
        print(noEncodeDecodeArgSuppliedMsg)
        exit()
        
    if encodeMsg:
        msgWordLen = 11 # number of bits in the message word
        print(msg_bits)
        if len(msg_bits) != msgWordLen:
            print(incorrectMsgWordLen.format(msgWordLen))
            exit()
        p1 = msg_bits[1] ^ msg_bits[4] ^ msg_bits[8] ^ msg_bits[0] ^ msg_bits[3] ^ msg_bits[6] ^ msg_bits[10]
        p2 = msg_bits[2] ^ msg_bits[5] ^ msg_bits[9] ^ msg_bits[0] ^ msg_bits[3] ^ msg_bits[6] ^ msg_bits[10]
        p3 = msg_bits[1] ^ msg_bits[2] ^ msg_bits[3] ^ msg_bits[7] ^ msg_bits[8] ^ msg_bits[9] ^ msg_bits[10]
        p4 = msg_bits[4] ^ msg_bits[5] ^ msg_bits[6] ^ msg_bits[7] ^ msg_bits[8] ^ msg_bits[9] ^ msg_bits[10]
        p0 = p1 ^ p2 ^ msg_bits[0] ^ msg_bits[1] ^ msg_bits[2] ^ msg_bits[3] ^ msg_bits[4] ^ msg_bits[5] ^ msg_bits[6] ^ msg_bits[7] ^ msg_bits[8] ^ msg_bits[9] ^ msg_bits[10]
        codeword = [p0, p1, p2, msg_bits[0], p3, msg_bits[1], msg_bits[2], msg_bits[3], p4, msg_bits[4], msg_bits[5], msg_bits[6], msg_bits[7], msg_bits[8], msg_bits[9], msg_bits[10]]
        codewordLen = len(codeword)
        print(encodingDoneMsg.format(msg_bits, codeword))
        
        errorTypes = ["Single-bit error", "Multi-bit error"]
        errorType = random.choice(errorTypes)
        print(errorInjectionMsg.format(errorType))
        # ==== Insert error ====
        if errorType == "Single-bit error":
            bitErrPosition = random.randint(0, codewordLen - 1)
            codeword[bitErrPosition] = codeword[bitErrPosition] ^ 1
            print(singleBitErrorPositionMsg.format(bitErrPosition))
        else:
            firstBitErrPosition = random.randint(0, codewordLen - 1)
            secondBitErrPosition = random.randint(0, codewordLen - 1)
            while (secondBitErrPosition == firstBitErrPosition):
                secondBitErrPosition = random.randint(0, codewordLen - 1)
            codeword[firstBitErrPosition] = codeword[firstBitErrPosition] ^ 1
            codeword[secondBitErrPosition] = codeword[secondBitErrPosition] ^ 1
            print(multiBitErrorPositionMsg.format(firstBitErrPosition, secondBitErrPosition))
        print(corruptedCodewordMsg.format(codeword))
    elif decodeMsg:
        codewordLen = 16 # the number of bits in the coreword
        if len(codeword) != codewordLen:
            print(incorrectMsgWordLen)
            exit()
    
    # ==== Error detection and correction ====
    setBitPositions = [i for i, bit in enumerate(codeword) if bit]
    xorSetBitPositions = reduce(lambda x, y: x ^ y, setBitPositions)

    if xorSetBitPositions != 0:
        # ==== Check for Uncorrectable Errors ====
        blockParity = reduce(lambda x, y: x ^ y, codeword)
        # If there's an error *and* the overall block parity is 0, then this indicates
        # that there have been multiple errors (bit flips)
        if blockParity == 0:
            print(multiBitErrorIdentifiedMsg)
        else:
            print(errorIdentifiedMsg.format(xorSetBitPositions))
            bitToCorrect = xorSetBitPositions
            codeword[bitToCorrect] = codeword[bitToCorrect] ^ 1
            print(correctedCodewordMsg.format(codeword))
            msgWord = [codeword[3], codeword[5], codeword[6], codeword[7], codeword[9], codeword[10], codeword[11], codeword[12], codeword[13], codeword[14], codeword[15]]
            print(retrievedBitsMsg.format(msgWord))
