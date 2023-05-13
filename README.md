# rpi-kafka-elastic
## 1. Install
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

## 2. Kafka Client
`cd kafka-client && source kafka/bin/activate`

## Reference:
[https://developer.confluent.io/get-started/python](Python - Get Started)
[https://github.com/confluentinc/librdkafka#build-from-source](librdkafka - Build From Source)

## Issues:
[https://github.com/confluentinc/confluent-kafka-python/issues/875](confluent-kafka-python requires librdkafka v1.4.0 or later.)
[https://github.com/confluentinc/confluent-kafka-python/issues/928](undefined symbol: rd_kafka_event_AlterConsumerGroupOffsets_result)