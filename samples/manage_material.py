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
    materials = sp_api.get_materials()  # Get all the materials linked to you
    print(f"Current materials: {materials} (total: {len(materials)} material(s))")

    # ADD
    new_material = sp_api.add_material(name=random_string(8), building=sp_api.get_buildings()[0]["code"])  # Create a new material (you will be the creator)
    print(f"A new material has been created: {new_material['name']}")

    # REBOOT the material (return the status: True or False)
    if sp_api.reboot_material(new_material["code"]):
        print(f"The material {new_material['name']} has been command to reboot")

    # REFRESH the medias in material (return the status: True or False)
    if sp_api.refresh_material(new_material["code"]):
        print(f"The material {new_material['name']} has been command to refresh")

    # # DELETE is not allowed yet

    sp_api.logout()  # Logout the account, more safe to use it, to avoid potential attacks
except APIError as e:
    print(f"Failure using the Smart Prospective API: {e}")
