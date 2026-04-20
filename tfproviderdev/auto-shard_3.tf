resource "jamfpro_static_computer_group" "auto_shard_3" {
  name                  = "auto-shard_3"
  assigned_computer_ids = [55, 59, 65, 69, 122, 126, 130]
}
