import os
import json

from jsonstore import JsonStore

from oxigraph_admin import settings


if not os.path.exists(settings.OXIGRAPH_STORE_FILE):
    with open(settings.OXIGRAPH_STORE_FILE, 'w') as f:
        data = {
            "users": [
                {
                    "username": "admin",
                    "permissions": [
                        "/api/v1/"
                    ],
                    "password_hash": "$2b$12$3mqiwa5WDBUtTRYzilZRceyaBJ89vOn2bm6JtNQp2MpEBHICRSRxW"
                }
            ],
            "security": {
                "enabled": True
            }
        }
        f.write(json.dumps(data, indent=4))

store = JsonStore(settings.OXIGRAPH_STORE_FILE, indent=4, auto_commit=True)
