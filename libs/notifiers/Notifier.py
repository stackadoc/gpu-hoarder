import abc
import logging
from typing import *

from libs.clouds.Cloud import Instance
from libs.config import NOTIFY_NEW_INSTANCES, NOTIFY_LOST_INSTANCES


class Notifier(abc.ABC):

    @property
    @abc.abstractmethod
    def enabled_env_name(self) -> str:
        """Name of the environment variable that enable this notifier"""
        ...

    def lost_instances_message(self, lost_instances: List[Instance]):
        return (
            "❌ The following instances are no longer available:\n" +
            "\n".join([
                f"• {instance.zone}: {instance.type}"
                for instance in sorted(lost_instances, key=lambda x: x.zone)
            ])
        )

    def new_instances_message(self, new_instances: List[Instance]):
        return (
            "✅ The following instances are available:\n" +
            "\n".join([
                f"• {instance.zone}: {instance.type}"
                for instance in sorted(new_instances, key=lambda x: x.zone)
            ])
        )

    @abc.abstractmethod
    def send_message(self, message: str):
        """Send a message"""
        ...

    def notify(self, lost_instances: List[Instance], new_instances: List[Instance]):
        if NOTIFY_NEW_INSTANCES and new_instances:
            logging.debug("[%s] Send message for new instances." % type(self).__name__)
            self.send_message(self.new_instances_message(new_instances))
        if NOTIFY_LOST_INSTANCES and lost_instances:
            logging.debug("[%s] Send message for lost instances." % type(self).__name__)
            self.send_message(self.lost_instances_message(lost_instances))
