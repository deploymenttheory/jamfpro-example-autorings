import os
import random
import uuid
import json
from optparse import OptionParser
from pathlib import Path
import jamfpy
from dotenv import load_dotenv
load_dotenv()

logger = jamfpy.new_logger(name="site_computer_setup", level=20)

COMPUTER_COUNT = 10

TENTANT_FQDN = os.environ.get("JAMFPRO_INSTANCE_FQDN")
CLIENT_ID = os.environ.get("JAMFPRO_CLIENT_ID")
CLIENT_SEC = os.environ.get("JAMFPRO_CLIENT_SECRET")
RANDOM_NUMBER = random.randint(0,9999)


instance = jamfpy.Tenant(
    fqdn=TENTANT_FQDN,
    auth_method="oauth2",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SEC,
    token_exp_threshold_mins=1
)


def create_computer_config(computer_name):
    return f"""
<computer>
    <general>
        <name>{computer_name}</name>
        <serial_number>{uuid.uuid4()}</serial_number>
        <udid>{uuid.uuid4()}</udid>
        <barcode_1/>
        <barcode_2/>
        <asset_tag/>
        <remote_management>
            <managed>true</managed>
            <management_username>jamfadmin</management_username>
            <management_password>string</management_password>
        </remote_management>
    </general>
    <location>
        <username/>
        <realname/>
        <real_name/>
        <email_address/>
        <position/>
        <phone/>
        <phone_number/>
        <department/>
        <building/>
        <room/>
    </location>
    <purchasing>
        <is_purchased>true</is_purchased>
        <is_leased>false</is_leased>
        <po_number/>
        <vendor/>
        <applecare_id>test</applecare_id>
        <purchase_price/>
        <purchasing_account/>
        <po_date/>
        <po_date_epoch>0</po_date_epoch>
        <po_date_utc/>
        <warranty_expires/>
        <warranty_expires_epoch>0</warranty_expires_epoch>
        <warranty_expires_utc/>
        <lease_expires/>
        <lease_expires_epoch>0</lease_expires_epoch>
        <lease_expires_utc/>
        <life_expectancy>0</life_expectancy>
        <purchasing_contact/>
        <os_applecare_id/>
        <os_maintenance_expires/>
        <attachments/>
    </purchasing>
    <extension_attributes>
        <extension_attribute>
            <id>2</id>
            <value/>
        </extension_attribute>
    </extension_attributes>
</computer>
    """



def parse_id_from_response(resp_text) -> str:
    start = "<id>"
    end = "</id>"
    return parse_tag_contents(start, end, resp_text)


def parse_tag_contents(start_tag, end_tag, resp_text):
    start_tag_length = len(start_tag)
    start_tag_index = resp_text.index(start_tag)
    end_tag_index = resp_text.index(end_tag)
    offset_start_tag_index = start_tag_index + start_tag_length

    return resp_text[offset_start_tag_index : end_tag_index]



def create_computers(amount):
    computer_ids = []
    for i in range (0, amount):
        computer_name = f"dummy-computer-{RANDOM_NUMBER}-{i}"
        computer_config = create_computer_config(computer_name)
        computer_id = send_create(instance.classic.computers, computer_config, "computers")
        computer_ids.append(computer_id)
    return computer_ids


def send_create(instance_object, payload, type_string):
    resp = instance_object.create(payload)
    if resp.ok:
        resp_text = resp.text
        object_id = parse_id_from_response(resp_text)
        logger.info(f"Successfully CREATED {type_string} id:{object_id}")
    else:
        logger.warning(f"FAILED to CREATE {type_string}")
    return object_id


def write_ids_to_data_source(computer_ids):
    full_path = "computer_ids.json"
    file = Path(full_path)
    # If the file path doesnt exist, the next line facilitates its creation
    file.parent.mkdir(parents=True, exist_ok=True)
    data_json = json.dumps(computer_ids)
    file.write_text(data_json)


computer_ids = create_computers(COMPUTER_COUNT)
write_ids_to_data_source(computer_ids=computer_ids)
