"""Constants for BEP Collectes."""

from datetime import timedelta

DOMAIN = "bep_collectes"

BASE_URL = "https://bep.harkor.be/api/locality"
LOCALITIES_URL = "https://bep.harkor.be/api/localities"

SCAN_INTERVAL = timedelta(hours=12)

PLATFORMS = ["sensor"]
