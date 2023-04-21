""" Main module of the script """

import logging
import threading

from flask import Flask
from rich.logging import RichHandler

from config_loader import ConfigLoader

from .exceptions import ConfigLoadError
from .retriever import data_retriever

from .bus import bus

# Load the settings
if not ConfigLoader.load_settings():
    raise ConfigLoadError('Configuration was not loaded.')

# Configure logging
logging.basicConfig(
    level=ConfigLoader.config['logging']['level'],
    format='%(name)s: %(message)s',
    datefmt="[%X]",
    handlers=[RichHandler()]
)

# Create a logger for the My REST API package
logger = logging.getLogger('MAIN')

# Done with the initialization phase
logger.info('Application initialized')
bus.emit('iniitialized')

# Start the retriever function
retriever_thread = threading.Thread(target=data_retriever, daemon=True)
retriever_thread.start()
bus.emit('updater_thread_started')

# Create the Flask App
flask_app = Flask(__name__)
