import skein
import random


def check_mix():
    round_n = 1
    block = random.randint(2 ** 511, 2 ** 512 - 1)
    print(block)
    block = 9706794053534508365091581628265777444983715381840147170897838015681424956743155799705111460122597395863239062648592300087943258556167194258455758776082231
    block = skein.to_bytes(block, 64)
    words = skein.bytes_to_words(block)
    for i in words:
        print(hex(i), end="")
    print("\n")
    words_new = []
    for i in range(4):
        x, y = skein.mix_fun(words[2*i], words[2*i + 1], round_n, i)
        words_new.append(x)
        words_new.append(y)
    sumi = ""
    for i in words_new:
        a = str(hex(i))[2:]
        while len(a) < 16:
            a = "0" + a
        sumi += a
    print(sumi)


def check_key():
    round_n = 17
    block = random.randint(2 ** 511, 2 ** 512 - 1)
    tweak = random.randint(2 ** 127, 2 ** 128 - 1)
    print(block)
    print(tweak)
    block = 12154318075531385683948857958357150528243345123141261426455496670127150293128573963258499991383805411532041286752049962260327254234103947468773041407201017
    tweak = 333205804626991183346845319332073990565
    tweak = skein.to_bytes(tweak, 16)
    block = skein.to_bytes(block, 64)
    words = skein.bytes_to_words(block)
    words_tweak = skein.bytes_to_words(tweak)
    print("Key:")
    for i in words:
        print(hex(i), end="")
    print("\nTweak:")
    for i in words_tweak:
        print(hex(i), end="")
    print("\n")
    subkeys = []
    for i in range(20):
        subkey = skein.key_schedule(words, words_tweak, i)
        subkeys.append(subkey)
    for index, subkey in enumerate(subkeys):
        print(f"index: {index}")
        for i in subkey:
            print(hex(i), end="  ")
        print("\n")


def to_int_2(string_of_bytes):
    to_int_val = int.from_bytes(string_of_bytes, 'little')
    return to_int_val


def words_to_bytes(words):
    bytes_1 = b''
    for word in words:
        bytes_1 = to_bytes(word, 8) + bytes_1
    return bytes_1


def to_bytes(int_val, n_bytes):
    string_of_bytes = int_val.to_bytes(n_bytes, 'little')
    return string_of_bytes


def check_threefish():
    tweak = skein.words_to_bytes([0x0706050403020100, 0x0F0E0D0C0B0A0908])
    key = skein.words_to_bytes([0x1716151413121110, 0x1F1E1D1C1B1A1918, 0x2726252423222120, 0x2F2E2D2C2B2A2928,
                                0x3736353433323130, 0x3F3E3D3C3B3A3938, 0x4746454443424140, 0x4F4E4D4C4B4A4948])
    plain = skein.words_to_bytes([0xF8F9FAFBFCFDFEFF, 0xF0F1F2F3F4F5F6F7, 0xE8E9EAEBECEDEEEF, 0xE0E1E2E3E4E5E6E7,
                                  0xD8D9DADBDCDDDEDF, 0xD0D1D2D3D4D5D6D7, 0xC8C9CACBCCCDCECF, 0xC0C1C2C3C4C5C6C7])
    ##tweak = words_to_bytes([0x0000000000000000, 0x0000000000000000])
    ##key = words_to_bytes([0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
                               ## 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000])
    ##plain = words_to_bytes([0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
                                 ## 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000])
    print(to_int_2(tweak))
    print(to_int_2(key))
    print(to_int_2(plain), "\n")
    my_threefish = skein.threefish(key, tweak, plain)
    my_threefish_words = skein.bytes_to_words(my_threefish)
    for i in my_threefish_words:
        print(str(hex(i))[2:], end="  ")

def main():
    # check_mix()
    # check_key()
    check_threefish()


if __name__ == "__main__":
    main()
