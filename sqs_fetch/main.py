from ETLJob import ETLJob
from config.config import load_config
from readers_writers.client_registery import client_registry
from models.message_model import Message
from utils.schema_validator import SchemaValidator
from utils.transform import PiiTransformer
from readers_writers import sqs_client, db_client


def get_config():
    config = load_config('config/config.yaml')
    # Create clients based on the configuration
    read_client_config = config['etl']['read_client']
    write_client_config = config['etl']['write_client']
    schema_keys = config['etl']['validator']['message_schema']
    schema_validator = SchemaValidator(schema_keys)
    read_client = client_registry.create(read_client_config['type'], **read_client_config)
    write_client = client_registry.create(write_client_config['type'], **write_client_config)
    return read_client, write_client, schema_validator


def main():

    read_client, write_client, schema_validator = get_config()
    etl = ETLJob(read_client, write_client, schema_validator)
    pii_transformer = PiiTransformer()
    etl.start(transformer=pii_transformer, model=Message)


if __name__ == "__main__":
    main()
