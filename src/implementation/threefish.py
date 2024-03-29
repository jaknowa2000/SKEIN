class KeyTypeError(Exception):
    pass


class InvalidKeyLength(Exception):
    pass


class Threefish512:
    def __init__(self):
        self.C_240 = 0x1BD11BDAA9FC1A22
        self.word_len = 64
        self.nb = 64
        self.n_rounds = 72

    @staticmethod
    def to_int(string_of_bytes):
        to_int_val = int.from_bytes(string_of_bytes, 'little')
        return to_int_val

    @staticmethod
    def to_bytes(int_val, n_bytes):
        string_of_bytes = int_val.to_bytes(n_bytes, 'little')
        return string_of_bytes

    @classmethod
    def bytes_to_words(cls, bytes_1):
        words = []
        for i in range(len(bytes_1)//8):
            words.append(cls.to_int(bytes_1[i*8:i*8+8]))
        return words

    @classmethod
    def words_to_bytes(cls, words):
        bytes_1 = b''
        for word in words:
            bytes_1 += cls.to_bytes(word, 8)
        return bytes_1

    def left_rotate(self, word, rotation_val):
        return ((word << rotation_val) | (word >> (self.word_len - rotation_val))) & 2**64 - 1

    def mix_fun(self, x0, x1, d, j):
        mix_table = [[46, 36, 19, 37],
                     [33, 27, 14, 42],
                     [17, 49, 36, 39],
                     [44, 9, 54, 56],
                     [39, 30, 34, 24],
                     [13, 50, 10, 17],
                     [25, 29, 39, 43],
                     [8, 35, 56, 22]]
        y0 = (x0 + x1) % 2**64
        y1 = self.left_rotate(x1, mix_table[d % 8][j]) ^ y0
        return y0, y1

    def mix_fun_inverse(self, y0, y1, d, j):
        mix_table = [[46, 36, 19, 37],
                     [33, 27, 14, 42],
                     [17, 49, 36, 39],
                     [44, 9, 54, 56],
                     [39, 30, 34, 24],
                     [13, 50, 10, 17],
                     [25, 29, 39, 43],
                     [8, 35, 56, 22]]
        mix_table = list(map(lambda x: list((64 - y for y in x)), mix_table))
        x1_temp = y1 ^ y0
        x1 = self.left_rotate(x1_temp, mix_table[d % 8][j])
        x0 = (y0 - x1) % 2 ** 64
        return x0, x1

    @staticmethod
    def pi_permutation(words):
        pi = [2, 1, 4, 7, 6, 5, 0, 3]
        new_words_order = []
        for i in pi:
            new_words_order.append(words[i])
        return new_words_order

    @staticmethod
    def pi_permutation_inverse(words):
        pi = [6, 1, 0, 7, 2, 5, 4, 3]
        new_words_order = []
        for i in pi:
            new_words_order.append(words[i])
        return new_words_order

    def split_message(self, message):
        blocks_message = []
        assert len(message) % self.nb == 0, "Error - incorrect message length"
        for i in range(len(message)//self.nb):
            blocks_message.append(message[i * self.nb : i * self.nb + self.nb])
        return blocks_message

    def padding(self, message):
        if len(message) == 0:
            p = self.nb
        else:
            p = -len(message) % self.nb
        for i in range(p):
            message += b'\x00'
        return message

    def key_schedule(self, key, tweak, s):
        nw = len(key)
        subkey = []
        tweak_ext = tweak[:]
        t_2 = tweak_ext[0] ^ tweak_ext[1]
        tweak_ext.append(t_2)
        k_nw = 0
        for k_i in key:
            k_nw = k_nw ^ k_i
        k_nw = k_nw ^ self.C_240
        key_ext = key[:]
        key_ext.append(k_nw)
        for i in range(nw):
            if i <= nw-4:
                subkey_i = key_ext[(s+i) % (nw+1)]
                subkey.append(subkey_i)
            if i == nw-3:
                subkey_i = (key_ext[(s+i) % (nw+1)] + tweak_ext[s % 3]) % 2**64
                subkey.append(subkey_i)
            if i == nw-2:
                subkey_i = (key_ext[(s+i) % (nw+1)] + tweak_ext[(s+1) % 3]) % 2**64
                subkey.append(subkey_i)
            if i == nw-1:
                subkey_i = (key_ext[(s+i) % (nw+1)] + s) % 2**64
                subkey.append(subkey_i)
        return subkey

    def threefish_block(self, key, tweak, plaintext):
        key = self.bytes_to_words(key)
        tweak = self.bytes_to_words(tweak)
        plaintext = self.bytes_to_words(plaintext)
        nw = len(key)
        v_vector = plaintext[:]
        f_vector = [0 for i in range(len(plaintext))]
        for d in range(self.n_rounds):
            if d % 4 == 0:
                e_vector = [sum(i) % 2**64 for i in zip(v_vector, self.key_schedule(key, tweak, d//4))]
            else:
                e_vector = v_vector[:]
            for j in range(nw // 2):
                f_vector[2*j : 2*j + 2] = self.mix_fun(e_vector[2*j], e_vector[2*j + 1], d, j)
            v_vector = self.pi_permutation(f_vector)
        c_vector = [sum(i) % 2**64 for i in zip(v_vector, self.key_schedule(key, tweak, self.n_rounds//4))]
        c_value = self.words_to_bytes(c_vector)
        return c_value

    def decryption_threefish_block(self, key, tweak, ciphertext):
        key = self.bytes_to_words(key)
        tweak = self.bytes_to_words(tweak)
        ciphertext = self.bytes_to_words(ciphertext)
        nw = len(key)
        n_rounds = 72
        c_vector = ciphertext[:]
        e_vector = [0] * len(ciphertext)
        v_vector = [(i[0] - i[1]) % 2 ** 64 for i in zip(c_vector, self.key_schedule(key, tweak, n_rounds // 4))]
        for d in range(n_rounds - 1, -1, -1):
            f_vector = self.pi_permutation_inverse(v_vector)
            for j in range(nw // 2):
                e_vector[2 * j: 2 * j + 2] = self.mix_fun_inverse(f_vector[2 * j], f_vector[2 * j + 1], d, j)
            if d % 4 == 0:
                v_vector = [(i[0] - i[1]) % 2 ** 64 for i in zip(e_vector, self.key_schedule(key, tweak, d // 4))]
            else:
                v_vector = e_vector[:]
        p_value = self.words_to_bytes(v_vector)
        return p_value

    @staticmethod
    def check_key(key):
        if not isinstance(key, bytes):
            try:
                key = bytes(key, encoding='utf-8')
            except TypeError:
                print("The type of key data is invalid!!!!!!!!!!")
                raise
        if len(key) != 64:
            raise InvalidKeyLength("Length of key is different than 64 bytes")
        return key

    def threehish_512(self, key, message, *args):
        key = self.check_key(key)
        tweak_s = 48 * 2 ** 120
        nb = 64
        message = self.padding(message)
        nm = len(message)
        message = self.split_message(message)
        cryptogram = b""
        for i in range(len(message)):
            if i == 0:
                a_i = 1
            else:
                a_i = 0
            if i == len(message) - 1:
                b_k_1 = 1
            else:
                b_k_1 = 0
            tweak = tweak_s + min(nm, (i + 1) * nb) + a_i * 2 ** 126 + b_k_1 * 2 ** 127
            if args:
                tweak = args[0]
            encrypted_block = self.threefish_block(key, self.to_bytes(tweak, 16), message[i])
            cryptogram += encrypted_block
        return cryptogram

    def decryption_threehish_512(self, key, ciphertext, *args):
        key = self.check_key(key)
        tweak_s = 48 * 2 ** 120
        nb = 64
        ciphertext = self.padding(ciphertext)
        nm = len(ciphertext)
        ciphertext = self.split_message(ciphertext)
        plaintext = b""
        for i in range(len(ciphertext)):
            if i == 0:
                a_i = 1
            else:
                a_i = 0
            if i == len(ciphertext) - 1:
                b_k_1 = 1
            else:
                b_k_1 = 0
            tweak = tweak_s + min(nm, (i + 1) * nb) + a_i * 2 ** 126 + b_k_1 * 2 ** 127
            if args:
                tweak = args[0]
            decrypted_block = self.decryption_threefish_block(key, self.to_bytes(tweak, 16), ciphertext[i])
            plaintext += decrypted_block
        return plaintext
