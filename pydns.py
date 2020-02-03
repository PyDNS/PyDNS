from pydns.server import Server
from pydns.utils.log import logger
from pydns import config
from pydns.utils import resources

# initialize logger
logger.info("Logger Initialized")

# Create default config
logger.info("Loading config...")
config = config.load()
port = config.getInt("general", "port")

logger.info(resources.getConfigPath())

server = Server(port=port)

