import timeit
from skein import Skein


def main():
    start = timeit.default_timer()
    a = Skein()
    path_returned, n_bytes_hash, my_hash = a.skein_512_512("try.txt")
    stop = timeit.default_timer()
    print("\nThe hashing took: ", (stop-start), "[s]")
    print("\nPath of hashed file: ", path_returned)
    print("Length of hash in bytes (should be 64): ", n_bytes_hash)
    print("Hash: ")
    print("-------------------------------------------------------------------------------")
    for index, byte in enumerate(my_hash, start=1):
        if index % 16 == 0:
            print(hex(byte), end="\n")
        else:
            print(hex(byte), end=" ")

    print("-------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()