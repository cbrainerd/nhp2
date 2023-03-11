import logging
import sys

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


if "-d" in sys.argv:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.WARNING)
