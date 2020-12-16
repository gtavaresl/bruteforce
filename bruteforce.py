import string
from zipfile import ZipFile
from itertools import product
import threading
from time import sleep
import argparse
import sys


class BruteThread:

    def __init__(self):
        self._running = True

    def terminate(self):
        print('Stop running threads!')
        self._running = False

    def run(self, name, zipfile, first_bits, alphabet):
        print('Starting thread ', str(name))
        i = 0
        # , alphabet, alphabet, alphabet, alphabet):
        for password in product(first_bits, alphabet, alphabet, alphabet):
            if self._running == False:
                print('Thread ' + str(name) + ' finished by another thread!')
                break
            i += 1
            if i % 1000000 == 0:
                print('Thread ' + str(name) + ' made :' + str(i))
            password = ''.join(password)
            if open_zip(zipfile, password):
                print('Thread ' + str(name) + ' finished!')
                self.terminate()
                break


def open_zip(zipfile, password):
    # print('Trying: ', password)
    try:
        zipfile.extractall(pwd=bytes(password, 'utf-8'))
        print('Worked with: ', password)
        return True
    except:
        return False


def open_easy():
    zipfile = ZipFile('easy.zip')
    for i in range(10000):
        if open_zip(zipfile, str(i)):
            break


def open_medium():
    chars = string.digits + string.ascii_letters

    for pwd in product(chars, repeat=8):
        pwd = ''.join(pwd)
        if open_zip('medium.zip', pwd):
            break


def open_hard(filename):
    threads = BruteThread()
    zipfile = ZipFile(filename)

    #alphabet = string.digits
    # alphabet = string.digits + string.ascii_letters + '!@#$%^&*?,()-=+[]/;'
    alphabet = string.ascii_lowercase

    num_threads = 8
    part_size = len(alphabet) // num_threads

    for i in range(num_threads):
        if i == num_threads - 1:
            first_bit = alphabet[part_size * i:]
        else:
            first_bit = alphabet[part_size * i: part_size * (i+1)]

        thread = threading.Thread(target=threads.run, args=(i,
                                                            zipfile, first_bit, alphabet, ))
        thread.start()


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default='texto.zip',
                    help="input zip filename")
    args = vars(ap.parse_args())
    filename = args["input"]

    # open_easy()
    open_hard(filename)
