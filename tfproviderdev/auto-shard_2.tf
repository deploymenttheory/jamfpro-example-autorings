resource "jamfpro_static_computer_group" "auto_shard_2" {
  name                  = "auto-shard_2"
  assigned_computer_ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61]
}
