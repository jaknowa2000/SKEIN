import unittest
from src.implementation.skein import Threefish512
from src.tests.support_test import list_of_byte_to_bytes


class TestThreefish(unittest.TestCase):
    def test_threefish_512_none(self):
        message = """00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"""

        key = """00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"""

        tweak = [0x0000000000000000,  0x0000000000000000]

        result = [0xBC2560EFC6BBA2B1,  0xE3361F162238EB40,  0xFB8631EE0ABBD175,  0x7B9479D4C5479ED1,
                  0xCFF0356E58F8C27B,  0xB1B7B08430F0E7F7,  0xE9A380A56139ABF1,  0xBE7B6D4AA11EB47E]

        threefish = Threefish512()
        tweak = threefish.to_int(threefish.words_to_bytes(tweak))
        message_bytes = list_of_byte_to_bytes(message)
        key_bytes = list_of_byte_to_bytes(key)
        obtained_result = threefish.threehish_512(key_bytes, message_bytes, tweak)
        obtained_result_words = threefish.bytes_to_words(obtained_result)

        self.assertEqual(result, obtained_result_words)

    def test_threefish_512(self):
        message = """FF FE FD FC FB FA F9 F8 F7 F6 F5 F4 F3 F2 F1 F0
                     EF EE ED EC EB EA E9 E8 E7 E6 E5 E4 E3 E2 E1 E0
                     DF DE DD DC DB DA D9 D8 D7 D6 D5 D4 D3 D2 D1 D0
                     CF CE CD CC CB CA C9 C8 C7 C6 C5 C4 C3 C2 C1 C0"""

        key_words = [0x1716151413121110, 0x1F1E1D1C1B1A1918, 0x2726252423222120, 0x2F2E2D2C2B2A2928,
                     0x3736353433323130, 0x3F3E3D3C3B3A3938, 0x4746454443424140, 0x4F4E4D4C4B4A4948]

        tweak = [0x0706050403020100,  0x0F0E0D0C0B0A0908]

        result = [0x2C5AD426964304E3, 0x9A2436D6D8CA01B4, 0xDD456DB00E333863, 0x794725970EB9368B,
                  0x043546998D0A2A27, 0x25A7C918EA204478, 0x346201A1FEDF11AF, 0x3DAF1C5C3D672789]

        threefish = Threefish512()
        tweak = threefish.to_int(threefish.words_to_bytes(tweak))
        message_bytes = list_of_byte_to_bytes(message)
        key_bytes = threefish.words_to_bytes(key_words)
        obtained_result = threefish.threehish_512(key_bytes, message_bytes, tweak)
        obtained_result_words = threefish.bytes_to_words(obtained_result)

        self.assertEqual(result, obtained_result_words)


if __name__ == '__main__':
    unittest.main()
