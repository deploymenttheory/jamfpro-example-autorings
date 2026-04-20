resource "jamfpro_static_computer_group" "auto_shard_1" {
  name                  = "auto-shard_1"
  assigned_computer_ids = [53, 57, 61, 63, 67, 71, 124, 128]
}
