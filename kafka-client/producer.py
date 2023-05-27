import sys
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
import psutil
from uuid import uuid4
from gpiozero import CPUTemperature
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from time import sleep, time
import json

class Monitor(object):
    """
    Monitor record

    Args:
        cpu_usage (double): CPU Usage in percentage

        cpu_temperature (double): CPU temperature in celsius

        ram_usage (double): RAM usage in percentage

        ram_usage_mb(double): RAM usage in MB
    """

    def __init__(self, cpu_usage, cpu_temperature, ram_usage, ram_usage_mb):
        self.cpu_usage = cpu_usage
        self.cpu_temperature = cpu_temperature
        self.ram_usage = ram_usage
        self.ram_usage_mb = ram_usage_mb

def monitor_to_dict(monitor):
    """
    Returns a dict representation of a monitor instance for serialization.

    Args:
        monitor (Monitor): Monitor instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with monitor attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return dict(timestamp=time(),
                cpu_usage=monitor.cpu_usage,
                cpu_temperature=monitor.cpu_temperature,
                ram_usage=monitor.ram_usage,
                ram_usage_mb=monitor.ram_usage)

def main(args):
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    print("Going to connect to: " + config_parser['default']['bootstrap.servers'])

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    # Produce data by selecting random values from these lists.
    topic = "internal-monitoring"

    schema_str = """
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "InternalMonitoring",
      "description": "A Real Time Raspberry Monitoring",
      "type": "object",
      "properties": {
        "timestamp": {
          "description": "Timestamp",
          "type": "number"
        },
        "cpu_usage": {
          "description": "CPU Usage in percentage",
          "type": "number"
        },
        "cpu_temperature": {
          "description": "CPU temperature in celsius",
          "type": "number"
        },
        "ram_usage": {
          "description": "RAM usage in percentage",
          "type": "number"
        },
        "ram_usage_mb": {
          "description": "RAM usage in MB",
          "type": "number"
        }
      },
      "required": [ "timestamp", "cpu_usage", "cpu_temperature", "ram_usage", "ram_usage_mb" ]
    }
    """
    schema_registry_conf = {'url': args.schema_server}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    json_serializer = JSONSerializer(schema_str, schema_registry_client, monitor_to_dict)

    while(True):
        cpu = CPUTemperature()
        monitor = Monitor(psutil.cpu_percent(4), cpu.temperature, psutil.virtual_memory()[2], psutil.virtual_memory()[3]/1000000000 )

        print("Publishing: " + str(monitor))

        producer.produce(topic=topic,
                        key=str(uuid4()),
                        value=json.dumps(monitor_to_dict(monitor)),
                        on_delivery=delivery_callback)

        # Block until the messages are sent.
        producer.poll(10000)
        producer.flush()

        sleep(5)


if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('-c', dest='config_file', type=FileType('r'))
    parser.add_argument('-s', dest='schema_server', type=str)
    args = parser.parse_args()
    main(args)