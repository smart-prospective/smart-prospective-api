from requests import get, post
import json
import os
import re

from .exceptions import APIError
from .decorators import network_try_except
from .log import getLogger


def get_server(subpath):
    """
        Return the complete api server url with subpath, by checking environnement variable 'SMART_PROSPECTIVE_SERVER' or use a default one

        :param subpath str: The subpath of the url to use (no need to include '/api' e.g: 'users/add')
        :rtype: str
        :return: The complete url
    """
    if "SMART_PROSPECTIVE_SERVER" in os.environ:
        server_url = os.environ["SMART_PROSPECTIVE_SERVER"]
    else:
        server_url = "https://app.smartprospective.com"
    # Add the /api to url (to save code)
    return f"{server_url}/api{subpath}"


def treat_response(response):
    """
        Treat a request.Response from a get() or a post() by parsing in json the response and checking the status code of the request.

        :param response request.Response: The response to treat
        :rtype: {...}/None
        :raise APIError: If status code is 4XX or 5XX
        :return: The JSON response. None otherwise (invalid JSON)
    """
    try:
        json_response = json.loads(response.text)
    except Exception as err:
        getLogger().error(f"SPApi.network: Invalid json response: {response.text}")
        json_response = None
    if int(response.status_code / 100) in [4, 5]:
        # Error
        getLogger().error(f"SPApi.network: Error from request:\nUrl:{response.url}\nResponse:{json_response}")
        raise APIError(f"Invalid status code response: {response.status_code}")
    return json_response


def treat_file_response(response, filename=None):
    """
        Treat a request.Response with a file given from a get() or a post() by using response.content

        :param response request.Response: The response to treat
        :param filename str/None: The filename (no extension) to create, can include the path (absolute or relative) (will be created if doesn't exist)
        :rtype: str/None
        :raise APIError: If status code is 4XX or 5XX / Folder cannot be created
        :return: The filepath created. None otherwise (invalid response)
    """
    if int(response.status_code / 100) in [4, 5]:
        # Error
        getLogger().error(f"SPApi.network: Error from request:\nUrl:{response.url}\nResponse Status:{response.text}")
        raise APIError(f"Invalid status code response: {response.status_code}")
    try:
        # Complete or Set filename
        try:
            request_filename = re.findall("filename=(.+)", response.headers['content-disposition'])[0]
            if not filename:
                # If filename not given, use the one from the request
                filename = request_filename
            else:
                # If filename given, only contact file extension
                filename += "." + request_filename.split(".")[-1]
        except Exception as e:
            getLogger().warning(f"SPApi.network: Cannot find the filename in the request: {response.headers}, use default filename 'unknown'")
            filename = "unknown"
        # Check folder from filename (create if if needed)
        folder = os.path.dirname(filename)
        if folder and not os.path.isdir(folder):
            os.makedirs(folder)
        with open(filename, "wb") as f:
            # Write the file from the request content
            f.write(response.content)
    except Exception as err:
        getLogger().error(f"SPApi.network: Invalid file response: {err}")
        filename = None
    return filename


@network_try_except
def default_get(token, resource):
    """
        Perform a GET request, insert the token as GET parameter and finally treat the response (JSON)

        :param token str: The token (set in GET parameters)
        :param resource str: The resource to build the url (https://server_url/api/{resource})
        :rtype: {...}/None
        :raise APIError: See treat_response()
        :return: See treat_response()
    """
    url = get_server(f"/{resource}") + f"?token={token}"
    return treat_response(get(url))


@network_try_except
def default_post(parameters, resource, files=None):
    """
        Perform a POST request and finally treat the response (JSON)

        :param parameters {...}: The data to use in the POST request
        :param resource str: The resource to build the url (https://server_url/api/{resource})
        :param files {...}: The files to insert
        :rtype: {...}/None
        :raise APIError: See treat_response()
        :return: See treat_response()
    """
    return treat_response(post(get_server(f"/{resource}"), data=parameters, files=files))


@network_try_except
def post_to_download(parameters, resource, files=None, filename=None):
    """
        Perform a POST request and finally treat the file response (filepath)

        :param parameters {...}: The data to use in the POST request
        :param resource str: The resource to build the url (https://server_url/api/{resource})
        :param files {...}: The files to insert
        :param filename str/None: The filename to create (See treat_file_response())
        :rtype: str/None
        :raise APIError: See treat_file_response()
        :return: See treat_file_response()
    """
    return treat_file_response(post(get_server(f"/{resource}"), data=parameters, files=files), filename=filename)
