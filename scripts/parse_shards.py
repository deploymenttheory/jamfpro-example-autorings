
import os
import sys
import json

FILE_NAME = "shards.json"
SHARDS_DIR = "shards/"

if not os.path.exists(FILE_NAME):
    print(f"error: {FILE_NAME} not found")
    sys.exit(1)

with open(FILE_NAME, "r", encoding="utf-8") as f:
    data: dict
    data = json.load(f)

shards: dict
shards = data.get("shards", [])

if not shards:
    print("no shards available")
    sys.exit(1)

for k, v in shards.items():
    # HCL identifiers can't have hyphens
    resource_name = f"auto_{k}".replace("-", "_")
    group_name    = f"auto-{k}"
    ids           = ", ".join(str(i) for i in v)

    tf  = f'resource "jamfpro_static_computer_group" "{resource_name}" {{\n'
    tf += f'  name                  = "{group_name}"\n'
    tf += f'  assigned_computer_ids = [{ids}]\n'
    tf += '}\n'

    
    filename = f"{SHARDS_DIR}/{group_name}.tf"
    with open(filename, "w", encoding="utf-8") as out:
        out.write(tf)
    print(f"wrote {filename}")
