resource "jamfpro_static_computer_group" "auto_shard_2" {
  name                  = "auto-shard_2"
  assigned_computer_ids = [64]
}
