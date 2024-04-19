import abc
import dataclasses
import logging
import os
from typing import *


@dataclasses.dataclass(frozen=True)
class Instance:
    zone: str
    type: str


class Cloud(abc.ABC):
    def __init__(self):
        self.last_available_instances = None

    @property
    def zones_filter(self) -> List[str]:
        if os.environ.get(self.zones_env_name):
            return os.environ[self.zones_env_name].split(",")
        else:
            return self.zones

    @property
    def instances_types_filter(self) -> Union[List[str], None]:
        if os.environ.get(self.instances_types_env_name):
            return os.environ[self.instances_types_env_name].split(",")
        else:
            return None

    @property
    @abc.abstractmethod
    def zones(self) -> List[str]:
        """List all available zones"""
        ...

    @property
    @abc.abstractmethod
    def enabled_env_name(self) -> str:
        """Name of the environment variable that enable this cloud"""
        ...

    @property
    @abc.abstractmethod
    def zones_env_name(self) -> str:
        """Name of the environment variable that filter the zones"""
        ...

    @property
    @abc.abstractmethod
    def instances_types_env_name(self) -> str:
        """Name of the environment variable that filter the instances types"""
        ...

    @abc.abstractmethod
    def _zone_instances(self, zone: str) -> List[str]:
        """
        Function to list all the available instances in a zone
        :param zone: The name of the zone
        :return: The list of available instances types
        """
        ...

    def instances(self) -> List[Instance]:
        """
        List all available instances types per region
        :return: List of tuples that contains the zone and the available instance
        """
        availabilities = []
        for zone in self.zones_filter:
            logging.debug("[%s] Get instances in zone %s..." % (type(self).__name__, zone))
            available_instances_types = self._zone_instances(zone)
            zone_availabilities = [
                Instance(zone=zone, type=instance_type)
                for instance_type in available_instances_types
                if (
                    self.instances_types_filter is None
                    or instance_type in self.instances_types_filter
                )
            ]
            availabilities += zone_availabilities

        return availabilities

    def update(self) -> Tuple[List[Instance], List[Instance]]:
        """
        List the new instances and the lost instances from the previous update() call
        :return: Tuple with the new instances and the lost instances
        """
        new_instances = []
        lost_instances = []
        available_instances = self.instances()
        if self.last_available_instances is not None:
            new_instances = list(
                set(available_instances) - set(self.last_available_instances)
            )
            if new_instances:
                logging.info(
                    "[%s] New instances: %s" % (type(self).__name__, new_instances)
                )
            lost_instances = list(
                set(self.last_available_instances) - set(available_instances)
            )
            if lost_instances:
                logging.info(
                    "[%s] Lost instances: %s" % (type(self).__name__, lost_instances)
                )
        self.last_available_instances = available_instances.copy()
        return new_instances, lost_instances
