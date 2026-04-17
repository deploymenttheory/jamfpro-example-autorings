import os
import json
import jamfpy
from dotenv import load_dotenv
load_dotenv()

logger = jamfpy.new_logger(name="delete_dummy_computers", level=20)

TENTANT_FQDN = os.environ.get("JAMFPRO_INSTANCE_FQDN")
CLIENT_ID = os.environ.get("JAMFPRO_CLIENT_ID")
CLIENT_SEC = os.environ.get("JAMFPRO_CLIENT_SECRET")

instance = jamfpy.Tenant(
    fqdn=TENTANT_FQDN,
    auth_method="oauth2",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SEC,
    token_exp_threshold_mins=1
)


def delete_computers(computer_ids):
    for computer_id in computer_ids:
        resp = instance.classic.computers.delete_by_id(int(computer_id))
        if resp.ok:
            logger.info(f"Successfully DELETED computer id:{computer_id}")
        else:
            logger.warning(f"FAILED to DELETE computer id:{computer_id}")


def load_ids(path="computer_ids.json") -> list:
    with open(path) as f:
        return json.load(f)


computer_ids = load_ids()
delete_computers(computer_ids)
