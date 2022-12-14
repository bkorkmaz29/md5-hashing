import hashlib
from argparse import ArgumentParser
from md5 import MD5


def main():
    argParser = ArgumentParser()

    argParser.add_argument(
        "input_string",
        metavar='string input',
        type=str,
    )

    md5 = MD5()
    arguments = argParser.parse_args()
    md5_hash = md5.generate_hash(arguments.input_string)

    print("Hash generated by algorithm: ", md5_hash)
    print("Hash generated by hashlib:   ", hashlib.md5(arguments.input_string.encode("utf_8")).hexdigest())

if __name__ == "__main__":
    main()
