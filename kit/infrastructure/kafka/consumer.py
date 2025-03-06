from dataclasses import dataclass, field
from traceback import TracebackException
from typing import Optional

from confluent_kafka import Consumer


@dataclass
class KafkaConsumer:
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = 'smallest'

    consumer: Consumer = field(init=False)

    def __post_init__(self) -> None:
        self.consumer = Consumer(
            {
                'bootstrap.servers': self.bootstrap_servers,
                'group.id': self.group_id,
                'auto.offset.reset': self.auto_offset_reset,
            }
        )

    def __enter__(self) -> Consumer:
        return self.consumer

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        self.consumer.close()
