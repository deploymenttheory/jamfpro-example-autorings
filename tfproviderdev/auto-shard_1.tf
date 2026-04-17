resource "jamfpro_static_computer_group" "auto_shard_1" {
  name                  = "auto-shard_1"
  assigned_computer_ids = [52, 55, 58, 61, 63, 66, 69]
}
