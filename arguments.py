import sys

class args:
    recursive = False

def handler():
    if len(sys.argv) -2 != 0: # testing if arguments exist
        for x in sys.argv:
            match x:
                case "-r":
                    args.recursive = True
    return args