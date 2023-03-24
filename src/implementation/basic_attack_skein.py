from skein import Skein
import time
import multiprocessing
from multiprocessing.sharedctypes import Array, Value
from math import ceil, log2

"""Set time of attack in seconds and nuber of attacked bytes below"""
ATTACK_TIME = 30
NB = 4


def attack_skein(start_val, number_messages):
    start_message = bytes(start_val)
    print("\nStart message: ", str(start_message))
    skein = Skein()
    attacked_hash = skein.skein_512_512("", start_message)
    modified_message = int.from_bytes(start_message, "big") + 1
    start = time.time()
    while True:
        modified_message = modified_message.to_bytes(length=ceil((log2(modified_message+1))/8), byteorder="big")
        current_hash = skein.skein_512_512("", modified_message)
        if attacked_hash[:NB] == current_hash[:NB]:
            break
        modified_message = int.from_bytes(modified_message, "big")
        modified_message += 1
        number_messages.value += 1
    stop = time.time()
    attacked_time = stop - start
    show_stats(attacked_time, attacked_hash, current_hash, modified_message, number_messages)


def show_stats(attacked_time, attacked_hash, current_hash, modified_message, number_messages):
    print("Time of attack: ", attacked_time/(60*60), "[h]\n")
    print(f"Attacked skein hash on first {NB} bytes: ", end=" ")
    for i in attacked_hash[:NB]:
        print(hex(i), end=" ")
    print(f"\n\nObtained hash on first {NB} bytes: ", end=" ")
    for i in current_hash[:NB]:
        print(hex(i), end=" ")
    print("\nMessage that gave this hash: ")
    for i in range(0, len(modified_message), 20):
        print(list(map(hex, modified_message[i:20 + i])))
    print("\nNumber of hashed messages: ", int(number_messages.value))


def main():
    message = b'Sean Connery'
    message = Array('b', message)
    number_messages = Value("d", 0)
    proces_attack = multiprocessing.Process(target=attack_skein, name="Attack_skein", args=(message, number_messages))
    proces_attack.start()
    proces_attack.join(ATTACK_TIME)
    if proces_attack.is_alive():
        print("\nAllowable attack time: ", ATTACK_TIME/(60*60), "[h] has elapsed")
        print("Number of hashed messages: ", int(number_messages.value))
        proces_attack.terminate()
        proces_attack.join()


if __name__ == "__main__":
    main()
