import os
from typing import *

import requests

from libs.clouds.Cloud import Cloud


class Scaleway(Cloud):
    zones = [
        "fr-par-1",
        "fr-par-2",
        "fr-par-3",
        "nl-ams-1",
        "nl-ams-2",
        "nl-ams-3",
        "pl-waw-1",
        "pl-waw-2",
        "pl-waw-3",
    ]
    enabled_env_name = "SCALEWAY_ENABLED"
    zones_env_name = "SCALEWAY_ZONES"
    instances_types_env_name = "SCALEWAY_INSTANCES_TYPES"

    def __init__(self):
        super().__init__()
        self.headers = {"X-Auth-Token": os.environ["SCALEWAY_SECRET_KEY"]}

    def _zone_instances(self, zone: str) -> Any:
        response = requests.get(
            url=(
                f"https://api.scaleway.com/instance/v1/zones/{zone}/products/servers/"
                f"availability"
            ),
            headers=self.headers,
        )
        response.raise_for_status()
        data = response.json()["servers"]
        instances_types = [
            instance_type
            for instance_type, availability in data.items()
            if availability["availability"] == "available"
        ]
        return instances_types
