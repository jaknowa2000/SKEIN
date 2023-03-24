from src.implementation.threefish import Threefish512


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

