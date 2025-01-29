import logging
import time

from confluent_kafka import Producer


class KafkaConnector:
    def __init__(self, server: str, command_callbacks: dict) -> None:
        prod_config = {"bootstrap.servers": server}

        self.producer = Producer(prod_config)
        self.command_callbacks = command_callbacks

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.error(f"Message delivery failed: {err}")
        else:
            logging.debug(
                f"Message delivered to {msg.topic()} [{msg.partition()}] at time {time.time()}"
            )

    def send_one(self, data):
        # Trigger any available delivery report callbacks from previous produce() calls
        self.producer.poll(0)

        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        self.producer.produce(
            "plants-info",
            data,
            callback=self.delivery_report,
            key=str(11),  # mock device id
        )

    def flush(self):
        self.producer.flush()

    def close_consumer(self):
        self.consumer.close()
