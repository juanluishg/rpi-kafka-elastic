# rpi-kafka-elastic
## Instructions
### 1. Install
On host:

`docker-compose up -d`

On raspberry-pi:

`cd kafka-client && python3 -m venv ./kafka`

`sudo apt update && sudo apt upgrade librdkafka-dev`

`cd ~/Downloads && git clone https://github.com/confluentinc/librdkafka.git && cd librdkafka`

`./configure --install-deps`

`make`

`sudo make install`

`pip3 install confluent-kafka`

### 2. Kafka Client
`cd kafka-client && source kafka/bin/activate`

### 3. Kafka Link Elastic
To active the connection:

`sh start_kafka_connect.sh`

## Ports:
1. Zookeeper -> 2181
2. Kafka Broker -> 9092 & 9101
3. Schema Registry -> 8081
4. Control Center -> 9021
5. Kafka Connect -> 8083
6. Elastic -> 19200 & 9300
7. Kibana -> 5601

## Reference:
[Python - Get Started](https://developer.confluent.io/get-started/python)

[librdkafka - Build From Source](https://github.com/confluentinc/librdkafka#build-from-source)

[How Kafka Networking works](https://www.confluent.io/blog/kafka-listeners-explained/)

[Kafka Connect to Elastic](https://medium.com/@jan_5421/how-to-add-an-elasticsearch-kafka-connector-to-a-local-docker-container-f495fe25ef72)

[JSON Producer](https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/json_producer.py)

## Issues:
[confluent-kafka-python requires librdkafka v1.4.0 or later.](https://github.com/confluentinc/confluent-kafka-python/issues/875)

[undefined symbol: rd_kafka_event_AlterConsumerGroupOffsets_result](https://github.com/confluentinc/confluent-kafka-python/issues/928)