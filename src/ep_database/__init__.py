import logging

from config_loader import ConfigLoader
from database import Database

from ep_database_model import *

# Create a logger
logger = logging.getLogger('ep_database')

ConfigLoader.load_settings()

# Get the data for the database
database_location = ConfigLoader.config['data_folder']
database_file = f'{database_location}/energy_prices.db'

# Connect to the database
connection_string = f'sqlite:///{database_file}'
Database.connect(connection=connection_string, create_tables=True)
