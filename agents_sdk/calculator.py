import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python calculator.py <expression>', file=sys.stderr)
        sys.exit(1)

    expression = sys.argv[1]
    for character in expression:
        if character not in '0123456789+-*/ ':
            print('Invalid characters in expression', file=sys.stderr)
            sys.exit(1)

    try:
        result = eval(expression)
    except Exception as e:
        print(f'Error evaluating expression: {e}', file=sys.stderr)
        sys.exit(1)

    print(result)
	