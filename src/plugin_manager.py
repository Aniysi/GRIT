import sys
import query
from colorama import Fore, Style
from git import Repo

def main():
    # Get command line arguments (excluding script name)
    args = sys.argv[1:]
        
    # Check if we are in a Git repository first
    try:
        Repo('.', search_parent_directories=True)
    except:
        print(Fore.RED + "Error: not a Git repository" + Style.RESET_ALL, file=sys.stderr)
        sys.exit(1)
    
    # Check arguments
    if len(args) == 1 and args[0] == 'cmd':
        query.main()
    else:
        print(Fore.RED + "Error: not a Gini command" + Style.RESET_ALL, file=sys.stderr)
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    main()
