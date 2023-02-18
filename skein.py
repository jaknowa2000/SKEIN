import timeit


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

    @staticmethod
    def pi_permutation(words):
        pi = [2, 1, 4, 7, 6, 5, 0, 3]
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


class Skein(Threefish512):
    def __init__(self):
        super().__init__()

    def ubi(self, g_config, message, tweak_s):
        nm = len(message)
        message = self.padding(message)
        message = self.split_message(message)
        h_i = g_config
        for i in range(len(message)):
            if i == 0:
                a_i = 1
            else:
                a_i = 0
            if i == len(message) - 1:
                b_k_1 = 1
            else:
                b_k_1 = 0
            tweak = tweak_s + min(nm, (i+1) * self.nb) + a_i * 2**126 + b_k_1 * 2**127
            h_i = self.threefish_block(h_i, self.to_bytes(tweak, 16), message[i])
            h_i_1 = b''
            for index, byte in enumerate(message[i]):
                h_i_1 += self.to_bytes(h_i[index] ^ message[i][index], 1)
            h_i = h_i_1[:]
        return h_i

    def skein_iv(self):
        k_prim = b''
        for i in range(self.nb):
            k_prim += b'\x00'
        config = b'\x53\x48\x41\x33'
        config += self.to_bytes(1, 2)
        config += b'\x00\x00'
        config += self.to_bytes(512, 8)
        config += b'\x00\x00\x00'
        for i in range(13):
            config += b'\x00'
        tweak = 4*(2**120)
        ubi_result = self.ubi(k_prim, config, tweak)
        ubi = self.bytes_to_words(ubi_result)
        return ubi

    def output(self, g):
        t_out = 63
        out = self.ubi(g, self.to_bytes(0, 8), t_out * 2**120)
        return out

    def skein_512_512(self, path, *args):
        if args:
            message = args[0]
        else:
            file = open(path, "rb")
            message = b"".join(file.readlines())
            file.close()
        # g_0 == IV
        iv = [0x4903ADFF749C51CE, 0x0D95DE399746DF03, 0x8FD1934127C79BCE, 0x9A255629FF352CB1, 0x5DB62599DF6CA7B0,
              0xEABE394CA9D5C3F4, 0x991112C71A75B523, 0xAE18A40B660FCC33]
        g0 = self.words_to_bytes(iv)
        t_msg = 48
        g1 = self.ubi(g0, message, t_msg * 2**120)
        h = self.output(g1)
        if args:
            return h
        else:
            return path, len(h), h

