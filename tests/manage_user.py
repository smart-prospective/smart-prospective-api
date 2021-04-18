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


# Optionnal / Utils method (only for the test)
def random_numbers(length):
    from random import choices
    from string import digits
    return ''.join(choices(digits, k=length))


try:
    # Setup the API credencial (do not perform any request at this moment)
    # Note: The public key starts by "pub_" & The secret key starts by "sec_"
    sp_api = SPApi(PUBLIC_KEY, PRIVATE_KEY)

    # GET
    users = sp_api.get_users()  # Get all the users linked to the user (does not inclue the current user)
    print(f"Current users: {users} (total: {len(users)} user(s))")

    # ADD
    new_user = sp_api.add_user(
        first_name=random_string(8),
        last_name=random_string(8),
        email=f"{random_string(8)}.{random_string(8)}@smartprospective.com", phone=f"+{random_numbers(10)}")  # Create a new user (will be in the same company as you)
    print(f"A new user has been created: {new_user['name']}")

    # DELETE
    print(f"Deleting user: {new_user['name']}")
    sp_api.delete_user(new_user["code"])  # Delete the just created User (actually the user is not delete, just disabled, it will be automatically deleted after a timeout)

    sp_api.logout()  # Logout the account, more safe to use it, to avoid potential attacks
except APIError as e:
    print(f"Failure using the Smart Prospective API: {e}")
