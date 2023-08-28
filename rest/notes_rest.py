from rest.rest_client import RestClient


class NotesRest(RestClient):
    """
    Notes API service
    """

    BASE_URL = "https://practice.expandtesting.com/notes/api/"
    _token: str | None = None

    @property
    def _headers(self):
        return {"x-auth-token": self._token}

    def get_health_check(self):
        """
        Send a GET request to /health-check
        :return: response in JSON format
        """
        self._log.info("Checking health")
        response = self._get("health-check")
        return response

    def post_users_register(
        self, name=None, email=None, password=None, expected_status_code=201
    ):
        """
        Send a POST request to /users/register
        :param expected_status_code: expected response code
        :param name: user's name
        :param email: user's email
        :param password: user's password
        :return: response in JSON format
        """
        self._log.info(f"register as {name}")
        response = self._post(
            "users/register",
            data={"name": name, "email": email, "password": password},
            expected_status_code=expected_status_code,
        )
        return response

    def post_users_login(self, email=None, password=None, expected_status_code=200):
        """
        Send a POST request to /users/login
        :param email: registered user's email
        :param password: registered user's password
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Logging in as {email}")
        response = self._post(
            "users/login",
            json={"email": email, "password": password},
            expected_status_code=expected_status_code,
        )
        if response["status"] == 200:
            self._token = response["data"]["token"]
        return response

    def get_users_profile(self, expected_status_code=200):
        """
        Send a GET request to /users/profile
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Retrieving user's profile")
        response = self._get("users/profile", expected_status_code=expected_status_code)
        return response

    def patch_users_profile(
        self, name=None, phone=None, company=None, expected_status_code=200
    ):
        """
        Send a PATCH request to /users/profile
        :param name: user's new name
        :param phone: user's phone
        :param company: user's company
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Updating user's profile")
        response = self._patch(
            "users/profile",
            data={"name": name, "phone": phone, "company": company},
            expected_status_code=expected_status_code,
        )
        return response

    def post_users_forgot_password(self, email=None, expected_status_code=200):
        """
        Send a POST request to /users/forgot-password
        :param email: user's email
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Sending password reset link to user's email {email}")
        response = self._post(
            "users/forgot-password",
            json={"email": email},
            expected_status_code=expected_status_code,
        )
        return response

    def post_users_verify_reset_password_token(self, token, expected_status_code=200):
        """
        Send a POST request to /users/verify-reset-password-token
        :param token: password reset token received via email
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Verifying password reset token")
        response = self._post(
            "users/verify-reset-password-token",
            json={"token": token},
            expected_status_code=expected_status_code,
        )
        return response

    def post_users_reset_password(self, token, new_password, expected_status_code=200):
        """
        Send a POST request to /users/reset-password
        :param expected_status_code: expected response code
        :param token: password reset token received via email
        :param new_password: user's new password
        :return: response in JSON format
        """
        self._log.info(f"Resetting user's password")
        response = self._post(
            "users/reset-password",
            json={"token": token, "newPassword": new_password},
            expected_status_code=expected_status_code,
        )
        return response

    def post_users_change_password(
        self, current_password, new_password, expected_status_code=200
    ):
        """
        Send POST request to /users/change-password
        :param current_password: user's current password
        :param new_password: user's new password
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Changing user's password")
        response = self._post(
            "users/change-password",
            data={"currentPassword": current_password, "newPassword": new_password},
            expected_status_code=expected_status_code,
        )
        return response

    def delete_users_logout(self, expected_status_code=200):
        """
        Send a DELETE request to /users/logout
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Logging out")
        response = self._delete(
            "users/logout", expected_status_code=expected_status_code
        )
        if response["status"] == 200:
            self._token = None
        return response

    def delete_users_delete_account(self, expected_status_code=200):
        """
        Send a DELETE request to /users/delete-account
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Deleting account")
        response = self._delete(
            "users/delete-account", expected_status_code=expected_status_code
        )
        if response["status"] == 200:
            self._token = None
        return response

    def post_notes(
        self, title=None, description=None, category=None, expected_status_code=200
    ):
        """
        Send a POST request to /notes
        :param title: title of the note
        :param description: description of the note
        :param category: category of the note (Home, Work, Personal)
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Creating note with title: {title}")
        response = self._post(
            "notes",
            data={"title": title, "description": description, "category": category},
            expected_status_code=expected_status_code,
        )
        return response

    def get_notes(self, expected_status_code=200):
        """
        Send a GET request to /notes
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info("Retrieving a list of notes")
        response = self._get("notes", expected_status_code=expected_status_code)
        return response

    def get_note_by_id(self, note_id=None, expected_status_code=200):
        """
        Send a GET request to /notes/{id}
        :param note_id: note's id
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Retrieving a note with id: {note_id}")
        response = self._get(
            f"notes/{note_id}", expected_status_code=expected_status_code
        )
        return response

    def put_note_by_id(
        self,
        note_id=None,
        title=None,
        description=None,
        completed=None,
        category=None,
        expected_status_code=200,
    ):
        """
        Send a PUT request to /notes/{id}
        :param note_id: note's id
        :param title: note's title
        :param description: note's description
        :param completed: note's status: completed or not completed (True, False)
        :param category: note's category (Home, Work, Personal)
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Updating a note with id: {note_id}")
        response = self._put(
            f"notes/{note_id}",
            json={
                "title": title,
                "description": description,
                "completed": completed,
                "category": category,
            },
            expected_status_code=expected_status_code,
        )
        return response

    def patch_note_by_id(self, note_id=None, completed=None, expected_status_code=200):
        """
        Send a PATCH request to /notes/{id}
        :param note_id: note's id
        :param completed: note's status: completed or not completed (True, False)
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Updating status of note with id: {note_id}")
        response = self._patch(
            f"notes/{note_id}",
            json={"completed": completed},
            expected_status_code=expected_status_code,
        )
        return response

    def delete_note_by_id(self, note_id=None, expected_status_code=200):
        """
        Send a DELETE request to /notes/{note_id}
        :param note_id: id of the note
        :param expected_status_code: expected response code
        :return: response in JSON format
        """
        self._log.info(f"Deleting note with id: {note_id}")
        response = self._delete(
            f"notes/{note_id}", expected_status_code=expected_status_code
        )
        return response
