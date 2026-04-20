resource "jamfpro_static_computer_group" "auto_shard_3" {
  name                  = "auto-shard_3"
  assigned_computer_ids = [55, 60, 65, 70, 124, 129]
}
