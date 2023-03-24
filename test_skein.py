import unittest
from skein import Skein, Threefish512


class TestSkein(unittest.TestCase):
    @staticmethod
    def write_to_file(path, message_converted):
        file = open(path, "wb")
        file.write(message_converted)
        file.close()

    @staticmethod
    def add_0x(string_v):
        return list(map(lambda x: "0x" + x, string_v.split()))

    @staticmethod
    def string_to_byte(list_string_bytes):
        return list(map(lambda x: Skein.to_bytes(int(x, base=16), 1), list_string_bytes))

    def list_of_byte_to_bytes(self, string_v):
        list_string_bytes = self.add_0x(string_v)
        list_strings_of_byte = self.string_to_byte(list_string_bytes)
        return b''.join(list_strings_of_byte)

    """Data for test_skein_IV was taken from Skein documentation"""
    def test_skein_IV(self):
        skein = Skein()
        self.assertEqual(skein.skein_iv(), [0x4903ADFF749C51CE, 0x0D95DE399746DF03, 0x8FD1934127C79BCE,
                                            0x9A255629FF352CB1, 0x5DB62599DF6CA7B0, 0xEABE394CA9D5C3F4,
                                            0x991112C71A75B523, 0xAE18A40B660FCC33])

    """Data for tests named ...documentation_xx was taken from Skein documentation"""
    def test_skein_512_512_documentation_1(self):
        message = "FF"
        test_result = """71 B7 BC E6 FE 64 52 22 7B 9C ED 60 14 24 9E 5B
                         F9 A9 75 4C 3A D6 18 CC C4 E0 AA E1 6B 31 6C C8
                         CA 69 8D 86 43 07 ED 3E 80 B6 EF 15 70 81 2A C5
                         27 2D C4 09 B5 A0 12 DF 2A 57 91 02 F3 40 61 7A"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("doc1.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("doc1.txt")

        self.assertEqual(path_returned, "doc1.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

    def test_skein_512_512_documentation_2(self):
        message = """FF FE FD FC FB FA F9 F8 F7 F6 F5 F4 F3 F2 F1 F0
                     EF EE ED EC EB EA E9 E8 E7 E6 E5 E4 E3 E2 E1 E0
                     DF DE DD DC DB DA D9 D8 D7 D6 D5 D4 D3 D2 D1 D0
                     CF CE CD CC CB CA C9 C8 C7 C6 C5 C4 C3 C2 C1 C0"""

        test_result = """45 86 3B A3 BE 0C 4D FC 27 E7 5D 35 84 96 F4 AC
                         9A 73 6A 50 5D 93 13 B4 2B 2F 5E AD A7 9F C1 7F
                         63 86 1E 94 7A FB 1D 05 6A A1 99 57 5A D3 F8 C9
                         A3 CC 17 80 B5 E5 FA 4C AE 05 0E 98 98 76 62 5B"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("doc2.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("doc2.txt")

        self.assertEqual(path_returned, "doc2.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

    def test_skein_512_512_documentation_3(self):
        message = """FF FE FD FC FB FA F9 F8 F7 F6 F5 F4 F3 F2 F1 F0
                     EF EE ED EC EB EA E9 E8 E7 E6 E5 E4 E3 E2 E1 E0
                     DF DE DD DC DB DA D9 D8 D7 D6 D5 D4 D3 D2 D1 D0
                     CF CE CD CC CB CA C9 C8 C7 C6 C5 C4 C3 C2 C1 C0
                     BF BE BD BC BB BA B9 B8 B7 B6 B5 B4 B3 B2 B1 B0
                     AF AE AD AC AB AA A9 A8 A7 A6 A5 A4 A3 A2 A1 A0
                     9F 9E 9D 9C 9B 9A 99 98 97 96 95 94 93 92 91 90
                     8F 8E 8D 8C 8B 8A 89 88 87 86 85 84 83 82 81 80"""

        test_result = """91 CC A5 10 C2 63 C4 DD D0 10 53 0A 33 07 33 09
                         62 86 31 F3 08 74 7E 1B CB AA 90 E4 51 CA B9 2E
                         51 88 08 7A F4 18 87 73 A3 32 30 3E 66 67 A7 A2
                         10 85 6F 74 21 39 00 00 71 F4 8E 8B A2 A5 AD B7"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("doc3.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("doc3.txt")

        self.assertEqual(path_returned, "doc3.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

    """Data for tests named "...file_xx" and "test_threefish" was taken from 
    https://www.schneier.com/wp-content/uploads/2015/01/skein.zip, from file named "skein_golden_kat_internals.txt"""
    def test_skein_512_512_file_1(self):
        message = """00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00"""

        test_result = """33 F7 45 7D  E0 65 69 E7  CF 5F D1 ED  D5 0C CF E1
                         D5 F1 66 42  9E 75 DD BE  54 A5 B7 E2  47 03 0D D9
                         12 F0 DC 5A  B6 01 2F 59  CE 92 03 AB  D8 2B 31 6D
                         F6 7D 5C 6F  00 9A 18 BA  84 DB 03 01  46 DA 99 DB"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("file1.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("file1.txt")

        self.assertEqual(path_returned, "file1.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

    def test_skein_512_512_file_2(self):
        message = """00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00"""

        test_result = """FB E6 5B 75  D6 81 B2 FE  35 47 80 BD  DF 82 CC F1
                         64 C5 CB 28  27 F8 E4 E7  DE 96 23 59  07 44 34 28
                         95 78 81 C7  6C E4 65 55  E2 BB 9E E3  4F 42 F7 A9
                         B2 E0 90 B5  5D 73 C7 A0  25 06 E1 7B  BD FF A4 F2"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("file2.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("file2.txt")

        self.assertEqual(path_returned, "file2.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

    def test_skein_512_512_file_3(self):
        message = """00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00
                     00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00"""

        test_result = """24 35 9E 4D  A3 9D B5 B4  99 50 87 C3  17 3B D1 6D
                         C7 3E 65 AB  7E C1 99 1F  7F A8 A3 DB  23 93 97 DC
                         09 C9 46 11  57 D9 39 B2  8F B8 10 7A  13 B3 1A 15
                         15 8B D0 0F  85 43 3A D2  AA E4 A1 B0  1B 25 E8 4D"""

        message_bytes = self.list_of_byte_to_bytes(message)
        test_result_bytes = self.list_of_byte_to_bytes(test_result)
        self.write_to_file("file3.txt", message_bytes)
        skein = Skein()
        path_returned, n_bytes_hash, my_hash = skein.skein_512_512("file3.txt")

        self.assertEqual(path_returned, "file3.txt")
        self.assertEqual(n_bytes_hash, len(test_result_bytes))
        self.assertEqual(my_hash, test_result_bytes)

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
        message_bytes = self.list_of_byte_to_bytes(message)
        key_bytes = self.list_of_byte_to_bytes(key)
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
        message_bytes = self.list_of_byte_to_bytes(message)
        key_bytes = threefish.words_to_bytes(key_words)
        obtained_result = threefish.threehish_512(key_bytes, message_bytes, tweak)
        obtained_result_words = threefish.bytes_to_words(obtained_result)

        self.assertEqual(result, obtained_result_words)




if __name__ == '__main__':
    unittest.main()
