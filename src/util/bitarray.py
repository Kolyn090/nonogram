# Original Java Version by fedimser: https://github.com/fedimser/nonolab
# Translated by Kolyn090


class BitArray:
    def __init__(self, length):
        self.length = length
        self.chunks = int((length - 1) / 64) + 1
        self.bits = [0] * self.chunks

    def get_bit(self, index):
        assert index < self.length
        return self.bits[index // 64] & (1 << (index % 64)) != 0

    def set_bit(self, index, value):
        assert index < self.length
        indicator = 1 << (index % 64)
        if value:
            self.bits[index // 64] |= indicator
        else:
            if self.bits[index // 64] & indicator != 0:
                self.bits[index // 64] -= indicator

    def and_with(self, other):
        assert other.length == self.length
        for i in range(self.chunks):
            self.bits[i] &= other.bits[i]

    def or_with(self, other):
        assert other.length == self.length
        for i in range(self.chunks):
            self.bits[i] |= other.bits[i]

    def get_length(self):
        return self.length

    def __str__(self):
        return ''.join('1' if self.get_bit(i) else '0' for i in range(self.length))


'''
if __name__ == "__main__":
    # Test case 1: Basic bit setting and getting
    bit_array = BitArray(10)
    bit_array.set_bit(0, True)
    assert bit_array.get_bit(0) == True, "Test 1.1 Failed: Bit at index 0 should be True"
    bit_array.set_bit(0, False)
    assert bit_array.get_bit(0) == False, "Test 1.2 Failed: Bit at index 0 should be False"

    # Test case 2: Set and get a bit at a higher index
    bit_array.set_bit(9, True)
    assert bit_array.get_bit(9) == True, "Test 2 Failed: Bit at index 9 should be True"

    # Test case 3: Length of the BitArray
    assert bit_array.get_length() == 10, "Test 3 Failed: Length should be 10"

    # Test case 4: AND operation
    bit_array1 = BitArray(5)
    bit_array2 = BitArray(5)
    bit_array1.set_bit(1, True)
    bit_array1.set_bit(3, True)
    bit_array2.set_bit(1, True)
    bit_array2.set_bit(2, True)
    bit_array1.and_with(bit_array2)
    assert bit_array1.get_bit(1) == True, "Test 4.1 Failed: Bit at index 1 should be True after AND"
    assert bit_array1.get_bit(2) == False, "Test 4.2 Failed: Bit at index 2 should be False after AND"
    assert bit_array1.get_bit(3) == False, "Test 4.3 Failed: Bit at index 3 should be False after AND"

    # Test case 5: OR operation
    bit_array1.set_bit(3, True)
    bit_array1.or_with(bit_array2)
    assert bit_array1.get_bit(1) == True, "Test 5.1 Failed: Bit at index 1 should be True after OR"
    assert bit_array1.get_bit(2) == True, "Test 5.2 Failed: Bit at index 2 should be True after OR"
    assert bit_array1.get_bit(3) == True, "Test 5.3 Failed: Bit at index 3 should be True after OR"

    # Test case 6: toString representation
    bit_array3 = BitArray(4)
    bit_array3.set_bit(0, True)
    bit_array3.set_bit(2, True)
    assert str(bit_array3) == "1010", "Test 6 Failed: String representation should be '1010'"

    # Test case 7: Larger bit index
    bit_array4 = BitArray(100)
    bit_array4.set_bit(63, True)
    assert bit_array4.get_bit(63) == True, "Test 7.1 Failed: Bit at index 63 should be True"
    bit_array4.set_bit(64, True)
    assert bit_array4.get_bit(64) == True, "Test 7.2 Failed: Bit at index 64 should be True"
    assert bit_array4.get_bit(62) == False, "Test 7.3 Failed: Bit at index 62 should be False"

    print("All tests passed!")
'''
