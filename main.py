import hashlib
from argparse import ArgumentParser
from md5 import MD5

def main():
    argParser = ArgumentParser()

    argParser.add_argument(
        "s",
        metavar='string input',
        type=str,
    )

    md5 = MD5()
    arguments = argParser.parse_args()
    md5Hash = md5._generate_hash(arguments.s)

    print("Hash created by algorithm: ", md5Hash)
    print("Hash created by hashlib lib: ", hashlib.md5(arguments.s.encode("utf_8")).hexdigest())

if __name__ == "__main__":
    main()
