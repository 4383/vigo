from sys import exit

from pbr.version import VersionInfo

from vigo import bootstrap
from vigo import cli
from vigo.config import GeneralConfig
from vigo.exceptions import OpenstackerException
from vigo.governance import Governance
from vigo.models import Analyze


def sync():
    bootstrap.sync()


def reset():
    bootstrap.reset()


def main():
    bootstrap.execute()
    governance = Governance()
    args = cli.argparser(governance.groups()).parse_args()
    GeneralConfig(args.debug, args.verbose)
    version = VersionInfo("vigo")
    if args.version:
        print("vigo v{version}".format(version=version))
        return 0

    try:
        Analyze(args.groups, governance, args.query)
    except OpenstackerException as err:
        print(str(err))
        return 1
    footer = "Generated by vigo v{version}".format(version=version)
    print("-" * len(footer))
    print(footer)
    print("-" * len(footer))
    return 0


if __name__ == "__main__":
    exit(main())
