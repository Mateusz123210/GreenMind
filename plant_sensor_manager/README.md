This module is used to control sensor data on an embedded device closest to the plants

# Development
run_format_and_lint.sh script should be used to maintain consistent code style

# Instruction to run on linux
sudo /opt/kafka_2.13-3.6.0/bin/zookeeper-server-start.sh /opt/kafka_2.13-3.6.0/config/zookeeper.properties

sudo /opt/kafka_2.13-3.6.0/bin/kafka-server-start.sh /opt/kafka_2.13-3.6.0/config/server.properties

### For debug
/opt/kafka_2.13-3.6.0/bin/kafka-console-consumer.sh --topic plants-info --from-beginning --bootstrap-server localhost:9092

/opt/kafka_2.13-3.6.0/bin/kafka-console-producer.sh --topic plants-info --bootstrap-server localhost:9092
