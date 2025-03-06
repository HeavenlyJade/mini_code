import socket
from dataclasses import dataclass, field
from traceback import TracebackException
from typing import Optional

from confluent_kafka import Producer


@dataclass
class KafkaProducer:
    bootstrap_servers: str
    client_id: str = socket.gethostname()
    retries: int = 3

    producer: Producer = field(init=False)

    def __post_init__(self) -> None:
        self.producer = Producer(
            {
                'bootstrap.servers': self.bootstrap_servers,
                'client.id': self.client_id,
                'retries': self.retries,
            }
        )

    def __enter__(self) -> Producer:
        return self.producer

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        self.producer.flush()
