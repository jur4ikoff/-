import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('integers', type=int,
                        nargs='*')
    args = parser.parse_args()
    integr = args.integers
    if len(integr) == 0:
        print('NO PARAMS')
    elif len(integr) == 1:
        print('TOO FEW PARAMS')
    elif len(integr) > 2:
        print('TOO MANY PARAMS')
    else:
        print(integr[0] + integr[1])
except SystemExit:
    pass
