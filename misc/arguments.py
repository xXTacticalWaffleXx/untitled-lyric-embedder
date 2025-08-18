import sys

class args:
    recursive = False
    debug = False
    dryRun = False
    help = False
    noApiCall = False

    target = ""

def handler():
    if len(sys.argv) -1 != 0: # testing if arguments exist
        for x in sys.argv:
            match x:
                case "-r":
                    args.recursive = True
                case "-d":
                    args.debug = True
                case "-D":
                    args.dryRun = True
                case "-h":
                    args.help = True
                case "-N":
                    args.noApiCall = True
                case _:
                    if x == sys.argv[-1]:
                        args.target = x
                    
    return args

args = handler()