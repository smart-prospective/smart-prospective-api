Smart Prospective API
======================

This python library is made to connect to Smart Prospective API, in order to manage your account, users, medias, publish content, bills...

Installation
------------
```python3 pip install smart-prospective-api```

Compatibility
-------------
Python >=3.6


Custom Config
-------------
__SMART_PROSPECTIVE_SERVER__: If you set this environment variable you can specify the target server ([More info](https://en.wikipedia.org/wiki/Environment_variable)):
```
import os
os.environ["SMART_PROSPECTIVE_SERVER"] = "https://custom-server.com"
```

Usage
-----
```
from smart-prospective-api import SPApi, APIError

try:
    # Setup the API credencial (do not perform any request at this moment)
    # Note: The public key starts by "pub_" & The secret key starts by "sec_"
    sp_api = SPApi("your_api_public_key", "your_api_secret_key")

    sp_api.get_medias()  # Get all the medias linked to this account

    sp_api.logout()  # Logout the account, more safe to use it, to avoid potential attacks
except APIError as e:
    print(f"Failure using the Smart Prospective API: {e}")

# Other Method (less common)
token = sp_api.login()  # This call is optionnal, because it's automatic on every call if needed if the token is not set
sp_api.token = token  # Manually set the token (so it won't perform any login() once you call any method)
```


Contact
-------
* Phone: +33 (0) 1 86 66 01 70
* Email: dev@smartprospective.com