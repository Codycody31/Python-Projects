import argparse
import sys
from cryptography.fernet import Fernet


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt a file using cryptography.')
    parser.add_argument('-f', '--file', help='File to encrypt/decrypt.')
    parser.add_argument('-k', '--key', type=int, help='Key to use.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress output to stdout.')
    parser.add_argument('-e', '--error', action='store_true',
                        help='File to write errors to.')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-d', '--decrypt', action='store_true',
                        help='Decrypt file.')
    parser.add_argument('-s', '--save', action='store_true',
                        help='Save key to file.')
    args = parser.parse_args()
    file = args.file
    if args.decrypt == False:
        if args.key is None:
            key = Fernet.generate_key()
        else:
            key = args.key
        try:
            with open(file, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            print('File not found.')
            sys.exit(1)
        f = Fernet(key)
        encrypted = f.encrypt(data)
        try:
            with open(file, 'wb') as f:
                f.write(encrypted)
        except FileNotFoundError:
            print('File not found.')
            sys.exit(1)
        if args.save:
            try:
                with open('key.key', 'wb') as key_file:
                    key_file.write(key)
            except FileNotFoundError:
                print('File not found.')
                sys.exit(1)
        if args.quiet == False:
            print('File encrypted.'), print(key)


main()
