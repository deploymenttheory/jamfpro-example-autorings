# jamfpro-autoring

Distributes Jamf Pro computer inventory across N shards and generates Terraform `jamfpro_static_computer_group` resources via GitHub Actions.

---

## Setup

### GitHub Actions environment

Create one environment per target (e.g. `tfproviderdev`) and configure:

| Name | Type | Description |
|---|---|---|
| `JAMFPRO_INSTANCE_FQDN` | Variable | Jamf Pro instance domain, e.g. `example.jamfcloud.com` |
| `JAMFPRO_CLIENT_ID` | Secret | OAuth2 client ID |
| `JAMFPRO_CLIENT_SECRET` | Secret | OAuth2 client secret |

### Docker image

The `auto-ring` workflow runs inside a container that packages the `go-jamf-guid-sharder` binary, Terraform, and Python. Build it once (and after any sharder release) by triggering **`build-push-docker-image`**.

---

## Workflows

| Workflow | Trigger | Description |
|---|---|---|
| `auto-ring` | `workflow_dispatch` | Shards inventory and opens a PR with updated `.tf` files |
| `build-push-docker-image` | `workflow_dispatch` | Builds and pushes the runner Docker image to GHCR |
| `create-dummy-computers` | `workflow_dispatch` | Creates N dummy computers in Jamf Pro for testing |
| `delete-dummy-computers` | `workflow_dispatch` | Deletes dummy computers created by the above |

---

## auto-ring inputs

| Input | Description | Default |
|---|---|---|
| `environment` | GitHub Actions environment to target | `tfproviderdev` |
| `strategy` | Distribution algorithm | `round-robin` |
| `shard_count` | Number of shards (round-robin / rendezvous) | — |
| `shard_percentages` | Percentages summing to 100, e.g. `10,30,60` | — |
| `shard_sizes` | Absolute sizes, `-1` = remainder, e.g. `50,200,-1` | — |
| `seed` | Seed for deterministic shuffling | — |
| `exclude_ids` | Comma-separated computer IDs to exclude, e.g. `1001,1002` | — |

### Distribution strategies

| Strategy | Description |
|---|---|
| `round-robin` | Even distribution across N shards |
| `rendezvous` | Consistent hash — stable across inventory changes |
| `percentage` | Split by percentages summing to 100 |
| `size` | Fixed shard sizes; use `-1` for remainder |
