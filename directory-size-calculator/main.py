import os
directory = os.path.dirname(__file__) + "\\"


def get_dir_size(path):
    """
    It recursively iterates over all files and directories in the given path, and returns the total size
    of all files in bytes
    
    :param path: The path to the directory you want to get the size of
    :return: The total size of the directory in bytes.
    """
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def print_sizes(path, output=False, verbose=True):
    """
    It prints the size of each directory in the path, and the total size of the path
    
    :param path: the path to the directory you want to check the size of
    :param output: If True, the output will be written to a file, defaults to False (optional)
    :param verbose: If True, prints the size of each directory. If False, only prints the total size,
    defaults to True (optional)
    """
    total_size = convert_bytes(get_dir_size(path))
    if output:
        with open(directory + 'output.txt', 'w') as f:
            for root, dirs, files in os.walk(path):
                text = f'{root}: {get_dir_size(root)} bytes'
                f.write(text + ' ' + '\n')
                if verbose:
                    print(text)
    else:
        for root, dirs, files in os.walk(path):
            text = f'{root}: {get_dir_size(root)} bytes'
            if verbose:
                print(text)
    print(f'Total size: {total_size}')


def convert_bytes(num):
    """
    It takes a number of bytes and returns a string with the number of bytes, kilobytes, megabytes,
    gigabytes, or terabytes, depending on the size of the number
    
    :param num: The number of bytes to convert
    :return: the size of the file in bytes, KB, MB, GB, or TB.
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return num


if __name__ == '__main__':
    path = input('Enter the path of the directory: ')
    output = input('Output to file? (y/n): ')
    verbose = input('Verbose? (y/n): ')
    output = output.lower()
    verbose = verbose.lower()
    output = True if output == 'y' else False
    verbose = True if verbose == 'y' else False
    print('Calculating...')
    print_sizes(path, output, verbose)
