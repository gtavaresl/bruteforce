import string
from zipfile import BadZipFile, ZipFile
from itertools import product
import threading
from time import sleep
import argparse


def open_zip(zipfile, password):
    #print('Trying: ', password)
    try:
        zipfile.extractall(pwd=bytes(password, 'utf-8'))
        print('Worked with: ', password)
        return True
    except:
        return False


def open_easy():
    for i in range(10000):
        if open_zip('easy.zip', str(i)):
            break


def open_medium():
    chars = string.digits + string.ascii_letters

    for pwd in product(chars, repeat=8):
        pwd = ''.join(pwd)
        if open_zip('medium.zip', pwd):
            break


def open_hard(filename):
    zipfile = ZipFile(filename)

    # alphabet = string.digits + string.ascii_letters + '!@#$%^&*?,()-=+[]/;'
    alphabet = string.ascii_lowercase

    num_parts = 16
    part_size = len(alphabet) // num_parts

    for i in range(num_parts):
        if i == num_parts - 1:
            first_bit = alphabet[part_size * i:]
        else:
            first_bit = alphabet[part_size * i: part_size * (i+1)]

        thr = threading.Thread(target=do_job, args=(i,
                                                    zipfile, first_bit, alphabet, ))
        thr.start()


def do_job(name, zipfile, first_bits, alphabet):
    print('Starting thread ', str(name))
    i = 0
    for password in product(first_bits, alphabet, alphabet, alphabet, alphabet, alphabet, alphabet, alphabet):
        i += 1
        if i % 1000000 == 0:
            print(print('Thread ' + str(name) + ' made :' + str(i)))
        password = ''.join(password)
        if open_zip(zipfile, password):
            break
    print('Thread ' + str(name) + 'finished!')


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default='texto.zip',
                    help="input zip filename")
    args = vars(ap.parse_args())
    filename = args["input"]

    open_hard(filename)
