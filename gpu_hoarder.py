import os
import time

from dotenv import load_dotenv

from libs.config import CLOUDS, SLEEP, NOTIFIERS

clouds = [cloud_class() for cloud_class in CLOUDS if os.environ.get(cloud_class.enabled_env_name) == "true"]
notifiers = [notifier_class() for notifier_class in NOTIFIERS if os.environ.get(notifier_class.enabled_env_name) == "true"]

while True:
    for cloud in clouds:
        load_dotenv(override=True)
        new_instances, lost_instances = cloud.update()
        for notifier in notifiers:
            notifier.notify(lost_instances=lost_instances, new_instances=new_instances)

    time.sleep(SLEEP)

