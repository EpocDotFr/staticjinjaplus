import argparse


def cli() -> None:
    arg_parser = argparse.ArgumentParser(description='The staticjinjaplus CLI which should be your main and only entry point to staticjinjaplus.')

    command_arg_parser = arg_parser.add_subparsers(dest='command', required=True)

    build_arg_parser = command_arg_parser.add_parser('build', help='Build the site')
    build_arg_parser.add_argument(
        '-w', '--watch',
        help='Automatically rebuild the site when templates are modified',
        action='store_true'
    )

    command_arg_parser.add_parser('clean', help='Delete and recreate the output directory')

    command_arg_parser.add_parser('publish', help='Publish the site (using `rsync` through SSH)')

    command_arg_parser.add_parser('serve', help='Serve the rendered site directory through HTTP')

    args = arg_parser.parse_args()

    if args.command == 'build':
        pass
    elif args.command == 'clean':
        pass
    elif args.command == 'publish':
        pass
    elif args.command == 'serve':
        pass
