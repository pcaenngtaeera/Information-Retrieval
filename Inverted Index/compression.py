#!/usr/bin/env python

from struct import pack, unpack


def encode(integer):
    """
    Encodes the

    Uses integer operations instead of bit shifts for efficiency. The integer "128"
    is equivalent to "1000 0000" and is used a mask. The algorithm focuses on adding
    byte-values to the <bytes> until the value can fit into a single byte. The last
    byte is given a "continuation bit" to let the decoder know it is the final byte.

    :param integer: an integer
    :return: a variable-byte encoded integer
    """
    bytes = []
    while True:
        print(integer % 128)
        bytes.insert(0, integer % 128)  # adds the byte-value to the front of the list
        if integer < 128:  # we have already the final byte
            break
        integer = integer // 128  # next byte
    bytes[-1] += 128  # add a "continuation bit" to the front of a byte
    return pack('%dB' % len(bytes), *bytes)


def decode(filestream):
    """
    Decodes an integer from a <filestream> by reading bytes until a "continuation bit" is encountered.

    Build an integer by iterating adding byte-values using the opposite operation of <encode>.
    The byte-values are unpacked one at a time until a "continuation" bit is reached.

    :param filestream: a filestream
    :return: an integer decoded from the filestream
    """
    integer = 0
    byte = unpack('B', filestream.read(1))[0]
    while True:
        if byte < 128:  # byte is missing the "continuation bit"
            integer = 128 * integer + byte
            byte = unpack('B', filestream.read(1))[0]  # read next byte
        else:  # any byte-value over 128 will have the "continuation bit"
            integer = 128 * integer + (byte - 128)
            return integer
