from skein import Skein
import time


def generate_random():
    k = 1
    # r = int((2**30 * 8)/512)
    r = int((2**20 * 8)/512)
    # r = 1
    file = open("skein_random.bin", "w+b")
    skein = Skein()
    a, b, before_hash = skein.skein_512_512("skein_random.bin")
    start = time.time()
    for i in range(r):
        hash_1 = skein.skein_512_512("", before_hash)
        before_hash = (before_hash[0] ^ k).to_bytes(1, "big") + before_hash[1:]
        hash_2 = skein.skein_512_512("", before_hash)
        difference = b""
        for byte_i in zip(hash_1, hash_2):
            difference += (byte_i[0] ^ byte_i[1]).to_bytes(1, "big")
        file.write(difference)
        before_hash = hash_1
    stop = time.time()
    print("Time: ", stop-start)
    file.close()


def main():
    generate_random()


if __name__ == "__main__":
    main()
