resource "jamfpro_static_computer_group" "auto_shard_4" {
  name                  = "auto-shard_4"
  assigned_computer_ids = [56, 61, 66, 71, 125, 130]
}
