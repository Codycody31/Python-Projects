import timeit
import hashlib
import random
import string
import sys
import os
import argparse
import csv
import json
import datetime
import platform
def main():
    parser = argparse.ArgumentParser(
        description='Benchmark hashing algorithms.')
    parser.add_argument('-a', '--algorithms', nargs='+',
                        help='Hashing algorithms to benchmark.')
    parser.add_argument('-b', '--bytes', type=int,
                        default=1000000, help='Number of bytes to hash.')
    parser.add_argument('-c', '--csv', help='CSV file to write results to.')
    parser.add_argument('-j', '--json', help='JSON file to write results to.')
    parser.add_argument('-r', '--repetitions', type=int,
                        default=100, help='Number of times to repeat each test.')
    parser.add_argument('-s', '--seed', type=int,
                        default=0, help='Random seed to use.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress output to stdout.')
    parser.add_argument('-e', '--error', action='store_true', help='File to write errors to.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    if args.quiet:
        algorithms = args.algorithms
        if algorithms is None:
            algorithms = hashlib.algorithms_available
            algorithms = sorted(algorithms)
            algorithms = [
                a for a in algorithms if a in hashlib.algorithms_guaranteed]
        bytes = args.bytes
        repetitions = args.repetitions
        seed = args.seed
        csv_filename = args.csv
        json_filename = args.json
        now = datetime.datetime.now()
        output = {
            'date': now.isoformat(),
            'platform': platform.platform(),
            'python': platform.python_version(),
            'algorithms': algorithms,
            'bytes': bytes,
            'repetitions': repetitions,
            'seed': seed,
            'results': {}
        }
        random.seed(seed)
        data = ''.join(random.choice(string.ascii_letters + string.digits)
                    for _ in range(bytes))
        data = data.encode('utf-8')
        for algorithm in algorithms:
            hash_function = getattr(hashlib, algorithm)
            try:
                timer = timeit.Timer(lambda: hash_function(data).hexdigest())
                results = timer.repeat(repetitions, 1)
            except Exception as e:
                if args.error:
                    with open('hash_error_log.txt', 'a') as f:
                        f.write(str(e))
                        f.write(' ')
                        f.write(str(algorithm))
                        f.write(' ')
                        f.write(str(bytes))
                        f.write(' ')
                        f.write(str(repetitions))
                        f.write(' ')
                        f.write(str(seed))
                        f.write(' ')
                        f.write(str(now))
                        f.write(' ')
                        f.write(str(platform.platform()))
                        f.write(' ')
                        f.write(str(platform.python_version()))
                        f.write(' ')
                        f.write(str(csv_filename))
                        f.write(' ')
                        f.write(str(json_filename))
                        f.write(' ')
                        f.write('\r\n')
                results = [0]
            average = sum(results) / len(results)
            minimum = min(results)
            maximum = max(results)
            output['results'][algorithm] = {
                'average': average,
                'minimum': minimum,
                'maximum': maximum
            }
            if csv_filename is not None:
                with open(csv_filename, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['algorithm', 'average', 'minimum', 'maximum'])
                    for algorithm, results in output['results'].items():
                        writer.writerow(
                            [algorithm, results['average'], results['minimum'], results['maximum']])
            if json_filename is not None:
                with open(json_filename, 'w') as json_file:
                    json.dump(output, json_file, indent=4, sort_keys=True)
    if args.quiet == False:
        algorithms = args.algorithms
        if algorithms is None:
            algorithms = hashlib.algorithms_available
            algorithms = sorted(algorithms)
            algorithms = [
                a for a in algorithms if a in hashlib.algorithms_guaranteed]
        bytes = args.bytes
        repetitions = args.repetitions
        seed = args.seed
        csv_filename = args.csv
        json_filename = args.json
        now = datetime.datetime.now()
        output = {
            'date': now.isoformat(),
            'platform': platform.platform(),
            'python': platform.python_version(),
            'algorithms': algorithms,
            'bytes': bytes,
            'repetitions': repetitions,
            'seed': seed,
            'results': {}
        }
        print('Benchmarking hashing algorithms...')
        print('Date: {}'.format(now.isoformat()))
        if csv_filename is not None:
            print('Writing results to CSV file: {}'.format(csv_filename))
        if json_filename is not None:
            print('Writing results to JSON file: {}'.format(json_filename))
        print('Creating random data...')
        random.seed(seed)
        data = ''.join(random.choice(string.ascii_letters + string.digits)
                    for _ in range(bytes))
        data = data.encode('utf-8')
        for algorithm in algorithms:
            print('Benchmarking {}...'.format(algorithm))
            hash_function = getattr(hashlib, algorithm)
            try:
                timer = timeit.Timer(lambda: hash_function(data).hexdigest())
                results = timer.repeat(repetitions, 1)
            except Exception as e:
                if args.error:
                    with open('hash_error_log.txt', 'a') as f:
                        f.write(str(e))
                        f.write(' ')
                        f.write(str(algorithm))
                        f.write(' ')
                        f.write(str(bytes))
                        f.write(' ')
                        f.write(str(repetitions))
                        f.write(' ')
                        f.write(str(seed))
                        f.write(' ')
                        f.write(str(now))
                        f.write(' ')
                        f.write(str(platform.platform()))
                        f.write(' ')
                        f.write(str(platform.python_version()))
                        f.write(' ')
                        f.write(str(csv_filename))
                        f.write(' ')
                        f.write(str(json_filename))
                        f.write(' ')
                        f.write('\r\n')
                results = [0]
            average = sum(results) / len(results)
            minimum = min(results)
            maximum = max(results)
            output['results'][algorithm] = {
                'average': average,
                'minimum': minimum,
                'maximum': maximum
            }
            print('Average: {:.6f}s'.format(average))
            print('Minimum: {:.6f}s'.format(minimum))
            print('Maximum: {:.6f}s'.format(maximum))
            if csv_filename is not None:
                with open(csv_filename, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['algorithm', 'average', 'minimum', 'maximum'])
                    for algorithm, results in output['results'].items():
                        writer.writerow(
                            [algorithm, results['average'], results['minimum'], results['maximum']])
            if json_filename is not None:
                with open(json_filename, 'w') as json_file:
                    json.dump(output, json_file, indent=4, sort_keys=True)
main()
