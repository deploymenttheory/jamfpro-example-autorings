resource "jamfpro_static_computer_group" "auto_shard_1" {
  name                  = "auto-shard_1"
  assigned_computer_ids = [53, 58, 63, 68, 122, 127]
}
