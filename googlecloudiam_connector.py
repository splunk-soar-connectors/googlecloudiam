# File: googlecloudiam_connector.py
#
# Copyright (c) 2021-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Python 3 Compatibility imports

import base64
import json
import os
import tempfile

import googleapiclient.discovery

# Phantom App imports
import phantom.app as phantom
from google.oauth2 import service_account
from googleapiclient import errors
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault

# Usage of the consts file is recommended
from googlecloudiam_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class GoogleCloudIamConnector(BaseConnector):
    def __init__(self):
        super().__init__()
        self._state = None

    def _get_error_message_from_exception(self, e):
        """This method is used to get appropriate error messages from the exception.
        :param e: Exception object
        :return: error message
        """

        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_message = e.args[1]
                elif len(e.args) == 1:
                    error_code = ERROR_CODE_MESSAGE
                    error_message = e.args[0]
            else:
                error_code = ERROR_CODE_MESSAGE
                error_message = ERROR_MESSAGE_UNAVAILABLE
        except:
            error_code = ERROR_CODE_MESSAGE
            error_message = ERROR_MESSAGE_UNAVAILABLE

        try:
            if error_code in ERROR_CODE_MESSAGE:
                error_text = f"Error Message: {error_message}"
            else:
                error_text = f"Error Code: {error_code}. Error Message: {error_message}"
        except:
            self.debug_print("Error occurred while parsing the error message")
            error_text = PARSE_ERROR_MESSAGE

        return error_text

    def _create_client(self, action_result):
        try:
            service_account_json = json.loads(self.key_json)
        except:
            return action_result.set_status(phantom.APP_ERROR, INVALID_SERVICE_ACCOUNT_JSON)

        try:
            credentials = service_account.Credentials.from_service_account_info(
                service_account_json, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )

            self._client = googleapiclient.discovery.build(IAM_SERVICE_NAME, IAM_SERVICE_VERSION, credentials=credentials)

        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Could not create google api client: {err}")

        return phantom.APP_SUCCESS

    def _send_request(self, request, action_result):
        try:
            response = request.execute()
        except errors.HttpError as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Google API HTTP Error: {err}"), None)
        except errors.Error as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Google API Request Error: {err}"), None)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Error Processing Request: {err}"), None)

        return phantom.APP_SUCCESS, response

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Connecting to endpoint")

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_serviceaccountkey(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]

        name = f"projects/{self.project}/serviceAccounts/{account}"
        try:
            request = self._client.projects().serviceAccounts().keys().list(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, LIST_SERVICE_ACCOUNT_KEY_SUCCESS_MESSAGE)

    def _handle_get_serviceaccountkey(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]
        key = param["key"]

        name = f"projects/{self.project}/serviceAccounts/{account}/keys/{key}"
        try:
            request = self._client.projects().serviceAccounts().keys().get(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, GET_SERVICE_ACCOUNT_KEY_SUCCESS_MESSAGE)

    def _handle_delete_serviceaccountkey(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]
        key = param["key"]

        name = f"projects/{self.project}/serviceAccounts/{account}/keys/{key}"
        try:
            request = self._client.projects().serviceAccounts().keys().delete(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, DELETE_SERVICE_ACCOUNT_KEY_SUCCESS_MESSAGE)

    def _handle_create_serviceaccountkey(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]
        save_key = param.get("save_key_to_vault")

        name = f"projects/{self.project}/serviceAccounts/{account}"
        try:
            request = self._client.projects().serviceAccounts().keys().create(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)
        if phantom.is_fail(ret_val):
            return ret_val

        if save_key:
            try:
                key_encoded = response["privateKeyData"]
                key_name = os.path.basename(response["name"])
                key_filename = f"{key_name}.json"
                key = base64.b64decode(key_encoded)
                vault_path = Vault.get_vault_tmp_dir()
                file_desc, file_path = tempfile.mkstemp(dir=vault_path)

                with open(file_path, "wb") as f:
                    f.write(key)
                vault_ret = Vault.add_attachment(file_path, self.get_container_id(), key_filename)
                response["vault_id"] = vault_ret[phantom.APP_JSON_HASH]
                response["filename"] = key_filename
                action_result.set_summary({"created_vault_id": vault_ret[phantom.APP_JSON_HASH]})
            except Exception as e:
                err = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, err)

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, CREATE_SERVICE_ACCOUNT_KEY_SUCCESS_MESSAGE)

    def _handle_get_serviceaccount(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]

        name = f"projects/{self.project}/serviceAccounts/{account}"
        try:
            request = self._client.projects().serviceAccounts().get(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, GET_SERVICE_ACCOUNT_SUCCESS_MESSAGE)

    def _handle_disable_serviceaccount(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]

        name = f"projects/{self.project}/serviceAccounts/{account}"
        try:
            request = self._client.projects().serviceAccounts().disable(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, DISABLE_SERVICE_ACCOUNT_SUCCESS_MESSAGE)

    def _handle_enable_serviceaccount(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            self.save_progress(API_CLIENT_ERROR_MESSAGE)
            return action_result.get_status()

        # Required values can be accessed directly
        account = param["account"]

        name = f"projects/{self.project}/serviceAccounts/{account}"
        try:
            request = self._client.projects().serviceAccounts().enable(name=name)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, err)
        ret_val, response = self._send_request(request, action_result)

        if phantom.is_fail(ret_val):
            return ret_val

        action_result.add_data(response)
        return action_result.set_status(phantom.APP_SUCCESS, ENABLE_SERVICE_ACCOUNT_SUCCESS_MESSAGE)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "list_serviceaccountkey":
            ret_val = self._handle_list_serviceaccountkey(param)

        elif action_id == "get_serviceaccountkey":
            ret_val = self._handle_get_serviceaccountkey(param)

        elif action_id == "delete_serviceaccountkey":
            ret_val = self._handle_delete_serviceaccountkey(param)

        elif action_id == "create_serviceaccountkey":
            ret_val = self._handle_create_serviceaccountkey(param)

        elif action_id == "get_serviceaccount":
            ret_val = self._handle_get_serviceaccount(param)

        elif action_id == "disable_serviceaccount":
            ret_val = self._handle_disable_serviceaccount(param)

        elif action_id == "enable_serviceaccount":
            ret_val = self._handle_enable_serviceaccount(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        self.key_json = config["key_json"]
        self.project = config["project"]

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse
    import sys

    import pudb
    import requests

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = GoogleCloudIamConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=60)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=60)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GoogleCloudIamConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == "__main__":
    main()
