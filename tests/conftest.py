import os
from logging import getLogger

import pytest

from rest.notes_rest import NotesRest

logger = getLogger(__name__)


@pytest.fixture(scope="session")
def email():
    return os.getenv("EMAIL")


@pytest.fixture()
def new_email():
    return os.getenv("NEW_EMAIL")


@pytest.fixture(scope="session")
def password():
    return os.getenv("PASSWORD")


@pytest.fixture()
def new_password():
    return os.getenv("NEW_PASSWORD")


@pytest.fixture
def notes_service():
    return NotesRest()


@pytest.fixture
def authenticated_notes_service(notes_service, email, password):
    notes_service.post_users_login(email, password)
    return notes_service


@pytest.fixture
def prepared_token(notes_service, email, password):
    logger.info("Prepare token for tests")
    response = notes_service.post_users_login(email, password)
    logger.info("Token prepared")
    return response["data"]["token"]


@pytest.fixture
def prepared_user(notes_service, new_email, password):
    logger.info("Prepare user for tests")
    name = "test_rest_api"
    notes_service.post_users_register(name, new_email, password)
    notes_service.post_users_login(new_email, password)
    logger.info("User prepared")
    return notes_service


@pytest.fixture
def prepared_note(authenticated_notes_service) -> dict:
    logger.info("Preparing note for tests")
    response = authenticated_notes_service.post_notes(
        title="Test Title",
        description="Test Description",
        category="Home",
        expected_status_code=200,
    )
    logger.info(f"Note prepared: {response['data']}")
    return response["data"]
