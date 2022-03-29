from . import main

# having a __main__.py allows you to run the script like this:
'''
    python -m path.to.the.script.directory
'''
# NOTE: treating our code as a Python package allows us to do relative imports
if __name__ == '__main__':
    main()
