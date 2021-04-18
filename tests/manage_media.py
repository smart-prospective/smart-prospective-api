from os import environ
from os.path import abspath, dirname, join
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
    medias = sp_api.get_medias()  # Get all the medias linked to you
    print(f"Current medias: {medias} (total: {len(medias)} media(s))")

    # ADD
    # File
    new_media = sp_api.add_media(category="file", name=random_string(8), file=join(dirname(abspath(__file__)), "image.png"), materials=[
                                 m["code"] for m in sp_api.get_materials()], tags=["TestAPI", "Local"])  # Create a new media (you will be the creator)
    # Audio
    new_media = sp_api.add_media(category="audio", name=random_string(8), file="/home/delbos-d/Music/Train - Hey, soul sister.mp3")  # Create a new media (you will be the creator)
    # Instagram
    new_media = sp_api.add_media(category="instagram", name=random_string(8), post_accounts=["@selenagomez", "@itsdougthepug"])  # Create a new media (you will be the creator)
    # Twitter
    new_media = sp_api.add_media(category="twitter", name=random_string(8), post_accounts=["@BarackObama", "@Youtube"])  # Create a new media (you will be the creator)
    # RSS
    new_media = sp_api.add_media(category="rss", name=random_string(8), post_accounts=[
                                 "https://www.asiaflash.com/horoscope/rss_horojour_poissons.xml", "https://www.ouest-france.fr/rss-en-continu.xml?tid=75258"])  # Create a new media (you will be the creator)
    # Youtube
    new_media = sp_api.add_media(category="youtube", name=random_string(8), url="https://www.youtube.com/watch?v=ReEgXh-wURs", keep_audio=True)  # Create a new media (you will be the creator)
    # Web
    new_media = sp_api.add_media(category="web", name=random_string(8), url="https://smartprospective.com")  # Create a new media (you will be the creator)
    # Template
    # Note: webview_details contains all the value (json) to fill the template
    new_media = sp_api.add_media(category="template", name=random_string(8), webview_details=json.dumps(
        {"text1": "Value1", "text2": "Value2"}), webviewtemplate=sp_api.get_webviewtemplates()[0]["code"])  # Create a new media (you will be the creator)
    # Note: If in webview_details you need to give a file, as value of a key use sp_api.upload_media_template_file(file="...absolute path...")["url"]
    print(f"A new media has been created: {new_media['name']}")

    # DOWNLOAD SOURCE FILE
    media_filepath = sp_api.download_src_media(new_media["code"])  # Download the media file, originaly uploaded (only the category with 'file' attibute during add)
    # Note: the filename can be given (no extension because will be auto set) (the filename can include the filepath which will be created if not yet)
    print(f"Download done for src media file: {new_media['name']} into: {media_filepath}")

    # DOWNLOAD CONVERTED FILE (.mp4 for most of the case) (If media has just been created, need to wait or an APIError will be raised)
    media_filepath = sp_api.download_converted_media(new_media["code"])  # Download the media file, converted into a supported format (.mp4) (all category except 'web')
    # Note: the filename can be given (no extension because will be auto set) (the filename can include the filepath which will be created if not yet)
    print(f"Download done for converted media file: {new_media['name']} into: {media_filepath}")

    # DOWNLOAD FINAL FILE (according to a specific material) (If media has just been created, need to wait or an APIError will be raised)
    # Download the media file that will be display on a material (all category except 'web')
    media_filepath = sp_api.download_final_media(new_media["code"], sp_api.get_materials()[0]["code"], filename="final-file")
    # Note: the filename can be given (no extension because will be auto set) (the filename can include the filepath which will be created if not yet)
    print(f"Download done for final media file: {new_media['name']} into: {media_filepath}")

    # DISABLE
    if sp_api.disable_media(new_media["code"]):  # Disable the just created Media
        print(f"The media: {new_media['name']} has been disable")

    # ENABLE
    if sp_api.enable_media(new_media["code"]):  # Enable the just created Media
        print(f"The media: {new_media['name']} has been enable")

    # DELETE
    print(f"Deleting media: {new_media['name']}")
    sp_api.delete_media(new_media["code"])  # Delete the just created Media

    sp_api.logout()  # Logout the account, more safe to use it, to avoid potential attacks
except APIError as e:
    print(f"Failure using the Smart Prospective API: {e}")
