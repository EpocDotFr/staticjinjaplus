from subprocess import call

def main() -> None:
    exit(call(
        'pygmentize '
        '-S default '
        '-f html '
        '-a .codehilite '
        '> docs/extra/pygments.css',
        shell=True
    ))


if __name__ == '__main__':
    main()
