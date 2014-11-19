
if __name__ == '__main__':

    if __package__ is None:  # If running 'python __main__.py'
        from streamhammer.cli import main

    else:  # Else if running 'python -m streamhammer'
        from .cli import main

    main()
