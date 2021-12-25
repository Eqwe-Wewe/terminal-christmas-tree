import argparse
import os
import random
import time


BALL = '@'
COLOR = {
    'blue': '\033[94m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}
STAR = '*'
density_dict = {
    1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1
}


def random_change_char(string, value):
    indexes = random.sample(range(0, len(string)), value)
    string = list(string)
    for idx in indexes:
        if string[idx] != ' ' and string[idx] == '_':
            string[idx] = BALL
    return ''.join(string)


def tree(height=13, screen_width=80):
    star = (STAR, 3*STAR)
    if height % 2 != 0:
        height += 1
    body = ['/_\\', '/_\_\\']
    trunk = '[___]'
    begin = '/'
    end = '\\'
    pattern = '_/'
    j = 5
    for i in range(7, height + 1, 2):
        middle = pattern + (i - j) * pattern
        line = ''.join([begin, middle[:-1], end])
        body.append(line)
        middle = middle.replace('/', '\\')
        line = ''.join([begin, middle[:-1], end])
        body.append(line)
        j += 1

    return [line.center(screen_width) for line in (*star, *body, trunk)]


def balls(tree, density):
    for idx, _ in enumerate(tree[:-3], 2):
        tree[idx] = random_change_char(
            tree[idx],
            len(tree[idx])//density_dict[density])
    return tree


def colored_stars_balls(tree):
    for idx, _ in enumerate(tree):
        string = list(tree[idx])
        for pos, _ in enumerate(string):
            if string[pos] == STAR:
                string[pos] = ''.join([COLOR['yellow'], STAR, '\033[0m'])
            elif string[pos] == BALL:
                string[pos] = ''.join(
                    [random.choice(list(COLOR.values())), BALL, '\033[0m']
                )
        tree[idx] = ''.join(string)
    return tree


def cli():
    parser = argparse.ArgumentParser(
        prog="Python Christmas Tree by Chico Lucio from Ciencia Programada",
        epilog="Ctrl-C interrupts the Christmas :-("
    )
    parser.add_argument(
        '-s', '--size', default=13, type=int,
        help=(
            "Tree height. If even it will be subtracted 1. If less than 7,"
            " considered 5. Default: 13"
        )
    )
    parser.add_argument(
        '-w', '--width', default=80, type=int,
        help="Screen width. Used to center the tree. Default: 80"
    )
    parser.add_argument(
        '-t', '--terminal', action='store_true',
        help=(
            "Uses the terminal size to center the tree. -s and -w will"
            " be ignored"
        )
    )
    parser.add_argument(
        '-d', '--density', default=4, type=int,
        help=(
            'The density of Christmas tree balls in a row display at a time. '
	    'Max: 10. Min: 1. Default: 4'
        )
    )
    args = parser.parse_args()

    if args.terminal:
        screen_width, height = os.get_terminal_size()
        height -= 2
        density = args.density
    else:
        height = args.size
        screen_width = args.width
        density = args.density
    while True:
        try:
            time.sleep(random.uniform(.1, 1))
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n'.join(
                colored_stars_balls(
                    balls(tree(height, screen_width), density)
                    )
                )
            )
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{'Merry Christmas!!':^{screen_width}}", end='\n\n')
            break


if __name__ == '__main__':
    cli()
