from src.implementation.threefish import Threefish512


def write_to_file(path, message_converted):
    file = open(path, "wb")
    file.write(message_converted)
    file.close()


def add_0x(string_v):
    return list(map(lambda x: "0x" + x, string_v.split()))


def string_to_byte(list_string_bytes):
    return list(map(lambda x: Threefish512.to_bytes(int(x, base=16), 1), list_string_bytes))


def list_of_byte_to_bytes(string_v):
    list_string_bytes = add_0x(string_v)
    list_strings_of_byte = string_to_byte(list_string_bytes)
    return b''.join(list_strings_of_byte)

