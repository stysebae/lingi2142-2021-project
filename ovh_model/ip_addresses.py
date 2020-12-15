"""
LINGI2142: Computer Networks: Configuration and Management
File: ip_addresses.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file contains IP addresses classes.
"""


class IPv4Address:
    """
    This class represents an IPv4 address with its 4 bytes and its mask.
    """

    def __init__(self, first_byte=10, second_byte=0, third_byte=0, fourth_byte=0, mask=24):
        """
        Initialize an IPv4 address by setting its values for each byte composing the address and the mask.
        """
        self.first_byte = first_byte
        self.second_byte = second_byte
        self.third_byte = third_byte
        self.fourth_byte = fourth_byte
        self.mask = mask

    def __str__(self):
        return f"{self.first_byte}.{self.second_byte}.{self.third_byte}.{self.fourth_byte}/{self.mask}"

    def get_fourth_byte(self):
        """
        :return: (int) The fourth byte of the IPv4 address.
        """
        return self.fourth_byte

    def set_host(self, host):
        """
        Set the host part of the IPv4 address.
        """
        host_list = str(host).split(".")
        if len(host_list) == 3:
            self.second_byte = host_list[0]
            self.third_byte = host_list[1]
            self.fourth_byte = host_list[2]
        elif len(host_list) == 2:
            self.third_byte = host_list[0]
            self.fourth_byte = host_list[1]
        else:
            self.fourth_byte = host_list[0]


class IPv6Address:
    """
    This class represents an IPv6 address with its 16 bytes and its mask.
    """

    def __init__(self, first_block="fc00", second_block="0", third_block="0", fourth_block="0", fifth_block="0",
                 sixth_block="0", seventh_block="0", eighth_block="0", mask=48):
        """
        Initialize an IPv6 address by setting its values (in hexadecimal, represented as str) for each block
        composing the address and the mask.
        """
        self.full_address = [first_block, second_block, third_block, fourth_block, fifth_block, sixth_block,
                             seventh_block, eighth_block]
        self.mask = mask

    def __str__(self):
        address_repr = self.full_address[:]
        zero_repr = "::"
        zero_blocks = self.get_zeros()
        if zero_blocks:
            if len(zero_blocks) > 1:
                diff = zero_blocks[1] - zero_blocks[0]
                for i in range(diff + 1):
                    address_repr[zero_blocks[0] + i] = ""  # we do not represent 0 value (but "::" instead)
            else:
                address_repr[zero_blocks] = zero_repr
        res = f"{address_repr[0]}:{address_repr[1]}:{address_repr[2]}:{address_repr[3]}:{address_repr[4]}:" \
              f"{address_repr[5]}:{address_repr[6]}:{address_repr[7]}/{self.mask}"
        for i in range(len(self.full_address) - 1, 2, -1):
            res = res.replace(":" * i, "::")
        return res

    def get_zeros(self):
        """
        Check if there are any empty consecutive blocks (0 value) in the IP address and return them. If not,
        return the first occurrence of a 0 value.

        :return: (int|tuple of int) Index of the first occurrence of a 0 value in the IP address or a range of 0.
        """
        zero_blocks = sorted([i for i, x in enumerate(self.full_address) if x == "0" or x == "0000"])
        res = None
        if zero_blocks:  # zero value(s) found
            if len(zero_blocks) > 1:
                gaps = [[current, next] for current, next in zip(zero_blocks, zero_blocks[1:]) if
                        current + 1 < next]
                edges = iter(zero_blocks[:1] + sum(gaps, []) + zero_blocks[-1:])
                ranges = list(zip(edges, edges))
                stop = False
                i = 0
                while not stop:
                    if ranges[i][0] != ranges[i][1]:  # start != end: there is a range of empty blocks
                        res = ranges[i][0], ranges[i][1]
                        stop = True
                    else:
                        i += 1
                if not res:  # consecutive blocks not found
                    res = zero_blocks[0]
            else:
                res = zero_blocks[0]
        return res

    def get_block(self, block_nbr):
        """
        :param block_nbr: (int) Index of the block number.
        :return: (str) A specified block of the IP address (if valid).
        """
        res = None
        if 0 <= block_nbr <= 7:
            res = self.full_address[block_nbr]
        return res

    def increment(self, block_nbr):
        """
        Increment a specified block of an IPv6 address.

        :param block_nbr: (int) A block of the IPv6 address we would like to increment.
        :return: (str) An incremented block.
        """
        block = self.get_block(block_nbr)
        res = block
        i = 1
        incremented_value = ""
        while (not incremented_value or "0" in incremented_value) and i <= len(block):
            incremented_value += self.get_next_hex_value(block[-i])
            i += 1
        return res[:-(i - 1)] + incremented_value[::-1]

    def get_next_hex_value(self, value):
        """
        :return: (str) The next value (as str) of a number in base 16.
        """
        res = ""
        try:
            if int(value) + 1 < 10:
                res = str(int(value) + 1)
            else:
                res = "a"
        except ValueError:
            if value in {"a", "b", "c", "d", "e", "f"}:
                res = chr(ord(value) + 1)
            else:
                res = str(0)
        return res

    def set_host(self, host):
        """
        Set the host part of the IPv6 address.
        """
        host_list = str(host).split(".")
        length_host = len(host_list)
        length_ip = len(self.full_address)
        for i in range(length_host):
            self.full_address[length_ip - length_host + i] = host_list[i]
