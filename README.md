# jamfpro-autoring

Distributes Jamf Pro computer inventory across N shards and generates Terraform `jamfpro_static_computer_group` resources via a GitHub Actions workflow.

---

## How it works

```
workflow_dispatch
       ↓
go-jamf-guid-sharder   ← fetches live computer inventory from Jamf Pro
       ↓
shards.json            ← computer IDs mapped to shard groups
       ↓
scripts/parse_shards.py
       ↓
{environment}/*.tf     ← one .tf file per shard
       ↓
Pull Request           ← review & merge to apply
```

---

## Distribution strategies

| Strategy | Description | Relevant inputs |
|---|---|---|
| `round-robin` | Evenly distributes computers across N shards | `shard_count`, `seed` |
| `rendezvous` | Consistent hash-based distribution — stable across inventory changes | `shard_count`, `seed` |
| `percentage` | Splits inventory by percentages summing to 100 | `shard_percentages` |
| `size` | Fixed shard sizes; use `-1` for remainder | `shard_sizes` |

---

## Workflow inputs (`auto-ring`)

| Input | Description | Default |
|---|---|---|
| `environment` | GitHub Actions environment to target | `tfproviderdev` |
| `strategy` | Distribution algorithm | `round-robin` |
| `shard_count` | Number of shards (round-robin / rendezvous) | `3` |
| `shard_percentages` | Percentages summing to 100, e.g. `10,30,60` | — |
| `shard_sizes` | Absolute sizes, `-1` = remainder, e.g. `50,200,-1` | — |
| `seed` | Seed string for deterministic shuffling | — |
| `exclude_ids` | Computer IDs to exclude from all shards, e.g. `1001,1002` | — |

---

## Secrets & variables

Configure per GitHub Actions environment:

| Name | Type | Description |
|---|---|---|
| `JAMFPRO_INSTANCE_FQDN` | Variable | Jamf Pro instance domain, e.g. `example.jamfcloud.com` |
| `JAMFPRO_CLIENT_ID` | Secret | OAuth2 client ID |
| `JAMFPRO_CLIENT_SECRET` | Secret | OAuth2 client secret |

---

## Docker image

The workflow runs inside a Docker container (`ghcr.io/{repo}/main:latest`) that packages the `go-jamf-guid-sharder` binary, Terraform, and Python dependencies. Rebuild it by triggering the `build-push-docker-image` workflow dispatch — it pulls the latest sharder release from GitHub and pushes a new image tagged with both `latest` and the commit SHA.

---

## Test data

`scripts/mocking/computers/` contains helpers to populate and clean up dummy computers in a Jamf Pro instance:

```bash
# create N dummy computers
python scripts/mocking/computers/create_dummy_computers.py <count>

# delete them
python scripts/mocking/computers/delete_dummy_computers.py
```

Requires `JAMFPRO_INSTANCE_FQDN`, `JAMFPRO_CLIENT_ID`, and `JAMFPRO_CLIENT_SECRET` — either via a `.env` file alongside the scripts or as environment variables.
