from .network import *
from .log import getLogger
from .decorators import is_login, supported_parameters


class SPApi():
    token = None
    api_public_key = None
    api_secret_key = None

    def __init__(self, api_public_key, api_secret_key):
        self.api_public_key = api_public_key
        self.api_secret_key = api_secret_key

    def login(self):
        """
            Login the user, in order to get a token using the api_public_key & api_secret_key.
            If the token is already present, no login is performed.

            :raise APIError: On any error
            :rtype: str
            :return: The API token, valid until logout or timeout
        """
        if not self.token:
            self.token = default_post({
                "api_public_key": self.api_public_key,
                "api_secret_key": self.api_secret_key
            }, "login")["token"]
        else:
            getLogger().debug("SPApi: Already connected")
        return self.token

    @is_login
    def logout(self):
        """
            Logout the user, in order to get release the token.
            The token must be set already present, no login is performed.

            :raise APIError: On any error
        """
        default_post({"token": self.token}, "logout")
        self.token = None

    # Users
    @is_login
    def get_users(self):
        """
            Get all the users link to this user.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of users
        """
        return default_get(self.token, "users")["users"]

    @is_login
    @supported_parameters(["first_name", "last_name", "email", "phone", "position", "password", "right_groups", "rights", "picture", "picture_link",
                           "buildings", "materialgroups", "materials"])
    def add_user(self, **kwargs):
        kwargs["token"] = self.token
        user = default_post(kwargs, "users/add")["user"]
        getLogger().info("User {user['name']} created!")
        return user

    @is_login
    def delete_user(self, code):
        default_post({
            "token": self.token,
            "user_code": code
        }, "users/remove")
        getLogger().info("User {code} deleted!")

    # Materials
    @is_login
    def get_materials(self):
        """
            Get all the materials.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of materials
        """
        return default_get(self.token, "materials")["materials"]

    @is_login
    @supported_parameters(["name", "building", "link_code", "picture", "picture_link", "default_media", "time_to_invalid",
                           "users", "division", "rotation", "bg_color", "width", "height", "player_config"])
    def add_material(self, **kwargs):
        kwargs["token"] = self.token
        material = default_post(kwargs, "materials/add")["material"]
        getLogger().info("Material {material['name']} created!")
        return material

    @is_login
    def reboot_material(self, code):
        status = default_post({
            "token": self.token,
            "material_code": code
        }, "materials/reboot")["status"]
        if status:
            getLogger().info("Material {code} will reboot!")
        else:
            getLogger().warning("Material {code} has already been asked to reboot, need to wait!")
        return status

    @is_login
    def refresh_material(self, code):
        status = default_post({
            "token": self.token,
            "material_code": code
        }, "materials/refresh")["status"]
        if status:
            getLogger().info("Material {code} will be refreshed!")
        else:
            getLogger().warning("Material {code} has already been asked to refresh, need to wait!")
        return status

    # Material Groups
    @is_login
    def get_materialgroups(self):
        """
            Get all the materialgroups.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of materialgroups
        """
        return default_get(self.token, "material-groups")["materialgroups"]

    @is_login
    @supported_parameters(["name", "comment", "materials", "buildings", "picture", "picture_link"])
    def add_materialgroup(self, **kwargs):
        kwargs["token"] = self.token
        materialgroup = default_post(kwargs, "material-groups/add")["materialgroup"]
        getLogger().info("Material Group {materialgroup['name']} created!")
        return materialgroup

    @is_login
    def delete_materialgroup(self, code):
        default_post({
            "token": self.token,
            "materialgroup_code": code
        }, "material-groups/remove")
        getLogger().info("User {code} deleted!")

    # Buildings
    @is_login
    def get_buildings(self):
        """
            Get all the buildings.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of buildings
        """
        return default_get(self.token, "buildings")["buildings"]

    # Media

    @is_login
    def get_medias(self):
        """
            Get all the medias.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of medias
        """
        return default_get(self.token, "medias")["medias"]

    @is_login
    @supported_parameters(["category", "name", "comment", "tags", "force_fullscreen", "lock", "buildings", "material_groups", "materials",
                           "format_details", "condition_start", "condition_end", "condition_weather", "condition_time", "frequency",
                           "print_min", "print_max", "animation_start", "animation_end", "male", "female", "both", "age_zero_fifteen",
                           "age_sixteen_twenty_eight", "age_twenty_nine_thirty_six", "age_thirty_seven_fifty", "age_fifty_one_ninty_nine",
                           "interests", "pcs_farmer", "pcs_worker", "pcs_retirees", "pcs_intermediate_professions", "pcs_employee",
                           "pcs_student", "pcs_unemployed", "pcs_craftsmen", "pcs_managment_nd_profession", "vistor_type_new",
                           "vistor_type_frequent", "vistor_type_occasional", "vistor_type_everybody", "specific_duration", "keep_audio",
                           "url", "file", "post_accounts", "webview_details", "webviewtemplate"])
    def add_media(self, category, **kwargs):
        # If file is given -> Double request: 1st Media File Upload -> 2nd add media
        if "file" in kwargs:
            file_input = None
            with open(kwargs["file"], "rb") as f:
                file_input = default_post({
                    "token": self.token
                }, "medias/upload", files={"file": f})["file"]["code"]
            if not file_input:
                getLogger().error(f"SPApi.add_media: Error from file upload\nFile after upload:{file_input}")
                raise APIError(f"Failure on file upload")
            # Field convertion "file" -> "file_input"
            kwargs["file_input"] = file_input
            del kwargs["file"]
        # Field convertion "post_accounts" -> "post_accounts_text"
        if "post_accounts" in kwargs:
            kwargs["post_accounts_text"] = ",".join(kwargs["post_accounts"])
            del kwargs["post_accounts"]
        # Field convertion "tags" -> "tags_text"
        if "tags" in kwargs:
            kwargs["tags_text"] = ",".join(kwargs["tags"])
            del kwargs["tags"]
        # Field convertion "interests" -> "interests_text"
        if "interests" in kwargs:
            kwargs["interests_text"] = ",".join(kwargs["interests"])
            del kwargs["interests"]
        kwargs["token"] = self.token
        media = default_post(kwargs, f"medias/add/{category}")["media"]
        getLogger().info("Media {media['name']} created!")
        return media

    @is_login
    def upload_media_template_file(self, file):
        with open(file, "rb") as f:
            return default_post({
                "token": self.token
            }, "medias/upload/template", files={"file": f})["file"]
        raise APIError(f"Failure on template file upload, maybe the file is not found or not readable")

    @is_login
    def download_final_media(self, media_code, material_code, filename=None):
        return post_to_download({
            "token": self.token,
            "media_code": media_code,
            "material_code": material_code,
        }, "medias/download/final", filename=filename)

    def download_converted_media(self, media_code, filename=None):
        return post_to_download({
            "token": self.token,
            "media_code": media_code
        }, "medias/download/convert", filename=filename)

    def download_src_media(self, media_code, filename=None):
        return post_to_download({
            "token": self.token,
            "media_code": media_code
        }, "medias/download/src", filename=filename)

    @is_login
    def disable_media(self, media_code):
        status = default_post({
            "token": self.token,
            "media_code": media_code
        }, "medias/disable")["status"]
        if status:
            getLogger().info("Media {code} has been disable!")
        else:
            getLogger().warning("Media {code} cannot be disable!")
        return status

    @is_login
    def enable_media(self, media_code):
        status = default_post({
            "token": self.token,
            "media_code": media_code
        }, "medias/enable")["status"]
        if status:
            getLogger().info("Media {code} has been enable!")
        else:
            getLogger().warning("Media {code} cannot be enable!")
        return status

    @is_login
    def delete_media(self, code):
        default_post({
            "token": self.token,
            "media_code": code
        }, "medias/remove")
        getLogger().info("Media {code} deleted!")

    # WebviewTemplate

    @is_login
    def get_webviewtemplates(self):
        """
            Get all the webviewtemplates.

            :raise APIError: On any error
            :rtype: [{...}]
            :return: The list of webviewtemplates
        """
        return default_get(self.token, "webviewtemplates")["webviewtemplates"]
