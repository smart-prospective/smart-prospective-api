from os import environ
from smart_prospective_api import SPApi, APIError
import json

PUBLIC_KEY = environ["SP_PUBLIC_KEY"]
PRIVATE_KEY = environ["SP_PRIVATE_KEY"]


# Optionnal / Utils method (only for the test)
def random_string(length):
    from random import choices
    from string import ascii_lowercase
    return ''.join(choices(ascii_lowercase, k=length))


try:
    # Setup the API credencial (do not perform any request at this moment)
    # Note: The public key starts by "pub_" & The secret key starts by "sec_"
    sp_api = SPApi(PUBLIC_KEY, PRIVATE_KEY)

    # GET
    materialgroups = sp_api.get_materialgroups()  # Get all the materialgroups linked to you
    print(f"Current materialgroups: {materialgroups} (total: {len(materialgroups)} materialgroup(s))")

    # ADD
    materials = sp_api.get_materials()[:2]  # Get all the Material Groups linked to you
    # Create a new materialgroup (you will be the creator)
    new_materialgroup = sp_api.add_materialgroup(name=random_string(8),
                                                 comment=random_string(35),
                                                 materials=[m["code"] for m in materials])
    print(f"A new materialgroup has been created: {new_materialgroup['name']}")

    # DELETE
    print(f"Deleting materialgroup: {new_materialgroup['name']}")
    sp_api.delete_materialgroup(new_materialgroup["code"])  # Delete the just created Material Group

    sp_api.logout()  # Logout the account, more safe to use it, to avoid potential attacks
except APIError as e:
    print(f"Failure using the Smart Prospective API: {e}")
