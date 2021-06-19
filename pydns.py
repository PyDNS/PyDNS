import sys
import argparse
from pydns.server import Server
from pydns.utils.log import logger
from pydns import config
from pydns.utils import resources


def main():
    # Create the parser and add the arguments
    parser = argparse.ArgumentParser(prog='pydns', description="PyDNS argument parser")
    parser.version = resources.getVersion()
    parser.add_argument('-c', '--config', type=str, help='Specify the path to the config file', required=False)
    parser.add_argument('-v', '--version', action='version', help='Shows the version of PyDNS you are running')
    parser.add_argument('-d', '--daemon', type=bool, help='Start server in background as a daemon', required=False,
                        default=False)

    # Parse the arguments
    args = parser.parse_args()

    # initialize logger
    logger.info("Logger Initialized")

    # Create default config
    logger.info("Loading config...")
    if args.config:
        conf = config.load(args.config)
    else:
        conf = config.load()

    port = conf.getInt("general", "port")
    backend = conf.getString("database", "backend")

    logger.info(resources.getConfigPath())

    # make sure we have a valid backend
    if backend not in resources.BACKENDS:
        logger.error("Invalid backend %s, stopping server." % backend)
        sys.exit()

    server = Server(port=port)

    if args.daemon:
        server.start()
    else:
        server.foreground()


if __name__ == "__main__":
    main()
