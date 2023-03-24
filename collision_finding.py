import time
import multiprocessing
import random
from multiprocessing.sharedctypes import Value
from math import ceil, log2
from skein import Skein


def collision_skein(number_messages):
    nb = 4
    modified_message = random.randint(2 ** 800, 2 ** 801)
    hash_list = []
    message_list = []
    start = time.time()
    while True:
        modified_message = modified_message.to_bytes(length=ceil((log2(modified_message+1))/8), byteorder="big")
        message_list.append(modified_message)
        skein = Skein()
        current_hash = skein.skein_512_512("", modified_message)
        if current_hash[:nb] in hash_list:
            index = hash_list.index(current_hash[:nb])
            break
        hash_list.append(current_hash[:nb])
        modified_message = int.from_bytes(modified_message, "big")
        modified_message += 1
        number_messages.value += 1
    stop = time.time()
    print("Time of attack: ", (stop-start)/(60*60), "[h]\n")
    print("First message of collision: ")
    for index1, i in enumerate(modified_message):
        if (index1 + 1) % 32 == 0:
            print(hex(i), end="\n")
        else:
            print(hex(i), end=" ")
    print(f"\n\nHash of this message on first {nb} bytes: ", end=" ")
    for i in current_hash[:nb]:
        print(hex(i), end=" ")
    print("\n\nSecond message of collision: ")
    for index1, i in enumerate(message_list[index]):
        if (index1 + 1) % 32 == 0:
            print(hex(i), end="\n")
        else:
            print(hex(i), end=" ")
    print(f"\n\nHash of this message on first {nb} bytes: ", end=" ")
    for i in hash_list[index]:
        print(hex(i), end=" ")
    print("\n\nNumber of hashed messages: ", int(number_messages.value))


def main():
    number_messages = Value("d", 0)
    proces_attack = multiprocessing.Process(target=collision_skein, name="Attack_skein", args=(number_messages,))
    proces_attack.start()
    attack_time = 30
    proces_attack.join(attack_time)
    if proces_attack.is_alive():
        print("\nAllowable attack time: ", attack_time/(60*60), "[h] has elapsed")
        print("Number of hashed messages: ", int(number_messages.value))
        proces_attack.terminate()
        proces_attack.join()


if __name__ == "__main__":
    main()
