def test_register_same_email(notes_service, email, password):
    name = "test_rest_api"
    response = notes_service.post_users_register(
        name, email, password, expected_status_code=409
    )
    assert (
        response["message"] == "An account already exists with the same email address"
    )


def test_login(notes_service, email, password):
    response = notes_service.post_users_login(email, password)
    assert response["data"]["token"] is not None


def test_login_invalid_email(notes_service, password):
    invalid_email = "invalid@email.com"
    response = notes_service.post_users_login(
        invalid_email, password, expected_status_code=401
    )
    assert response["message"] == "Incorrect email address or password"


def test_profile_unauthorized(notes_service):
    response = notes_service.get_users_profile(expected_status_code=401)
    assert (
        response["message"]
        == "No authentication token specified in x-auth-token header"
    )


def test_get_profile(authenticated_notes_service, email):
    response = authenticated_notes_service.get_users_profile()

    assert response["message"] == "Profile successful"
    assert response["data"]["email"] == email
    assert response["data"]["name"] == "test_rest_api"
    assert response["data"]["id"] is not None


def test_update_profile(authenticated_notes_service):
    name = "test_rest_api"
    phone = "0800208020"
    company = "hillel IT school"
    response = authenticated_notes_service.patch_users_profile(name, phone, company)
    assert response["message"] == "Profile updated successful"
    assert response["data"]["name"] == name
    assert response["data"]["phone"] == phone
    assert response["data"]["company"] == company


def test_reset_forgot_password(notes_service, email):
    response = notes_service.post_users_forgot_password(email)
    assert (
        response["message"] == f"Password reset link successfully sent to {email}. "
        f"Please verify by clicking on the given link"
    )


def test_reset_forgot_password_invalid_email(notes_service):
    invalid_email = "invalid@email.com"
    response = notes_service.post_users_forgot_password(
        invalid_email, expected_status_code=401
    )
    assert response["message"] == "No account found with the given email address"


def test_verify_reset_password_token_invalid(notes_service, prepared_token):
    response = notes_service.post_users_verify_reset_password_token(
        prepared_token, expected_status_code=401
    )
    assert (
        response["message"]
        == "The provided password reset token is invalid or has expired"
    )


def test_reset_password_cut_token(notes_service, new_password):
    cut_token = "8bb383368052433799da088796d5d0aba0312d2ebb3446bca983d39"
    response = notes_service.post_users_reset_password(
        cut_token, new_password, expected_status_code=400
    )
    assert response["message"] == "Token must be between 64 characters"


def test_change_password_identical(authenticated_notes_service, password):
    response = authenticated_notes_service.post_users_change_password(
        password, password, expected_status_code=400
    )
    assert (
        response["message"]
        == "The new password should be different from the current password"
    )


def test_change_password_cut_new(authenticated_notes_service, password):
    cut_new_password = "pwd"
    response = authenticated_notes_service.post_users_change_password(
        password, cut_new_password, expected_status_code=400
    )
    assert response["message"] == "New password must be between 6 and 30 characters"


def test_change_password_invalid_current(authenticated_notes_service, password):
    invalid_current_password = "12345678"
    response = authenticated_notes_service.post_users_change_password(
        invalid_current_password, password, expected_status_code=400
    )
    assert response["message"] == "The current password is incorrect"


def test_change_password_cut_current(authenticated_notes_service, new_password):
    cut_password = "pwd"
    response = authenticated_notes_service.post_users_change_password(
        cut_password, new_password, expected_status_code=400
    )
    assert response["message"] == "Current password must be between 6 and 30 characters"


def test_change_password_unauthorized(notes_service, password, new_password):
    response = notes_service.post_users_change_password(
        password, new_password, expected_status_code=401
    )
    assert (
        response["message"]
        == "No authentication token specified in x-auth-token header"
    )


def test_logout(authenticated_notes_service):
    response = authenticated_notes_service.delete_users_logout()
    assert response["message"] == "User has been successfully logged out"


def test_logout_unauthorized(notes_service):
    response = notes_service.delete_users_logout(expected_status_code=401)
    assert (
        response["message"]
        == "No authentication token specified in x-auth-token header"
    )


def test_delete_account(prepared_user):
    response = prepared_user.delete_users_delete_account()
    assert response["message"] == "Account successfully deleted"


def test_delete_account_unauthorized(notes_service):
    response = notes_service.delete_users_delete_account(expected_status_code=401)
    assert (
        response["message"]
        == "No authentication token specified in x-auth-token header"
    )
