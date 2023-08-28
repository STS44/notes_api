import pytest


@pytest.mark.parametrize("category", ["Home", "Work", "Personal"])
def test_create_note(authenticated_notes_service, category):
    title = "Test Note"
    description = "Test Description"

    response = authenticated_notes_service.post_notes(title, description, category)

    assert response["message"] == "Note successfully created"
    assert response["data"]["title"] == title
    assert response["data"]["description"] == description
    assert response["data"]["category"] == category
    assert response["data"]["id"] is not None


def test_create_note_invalid_category(authenticated_notes_service):
    title = "Test note"
    description = "Test Description"
    category = "Invalid"

    response = authenticated_notes_service.post_notes(
        title, description, category, expected_status_code=400
    )

    assert (
        response["message"]
        == "Category must be one of the categories: Home, Work, Personal"
    )


def test_get_notes(authenticated_notes_service):
    response = authenticated_notes_service.get_notes()
    assert response["message"] == "Notes successfully retrieved"
    assert len(response["data"]) > 0
    for list_item in response["data"]:
        assert list_item["id"] is not None


def test_get_note_by_id(authenticated_notes_service, prepared_note):
    response = authenticated_notes_service.get_note_by_id(prepared_note["id"])
    assert response["message"] == "Note successfully retrieved"
    assert response["data"]["title"] == prepared_note["title"]
    assert response["data"]["description"] == prepared_note["description"]
    assert response["data"]["category"] == prepared_note["category"]


def test_get_note_by_id_cut_id(authenticated_notes_service):
    cut_id = "65e764e9d1562c00f72545"
    response = authenticated_notes_service.get_note_by_id(
        cut_id, expected_status_code=400
    )
    assert response["message"] == "Note ID must be a valid ID"


def test_get_note_by_id_deleted_note(authenticated_notes_service, prepared_note):
    authenticated_notes_service.delete_note_by_id(prepared_note["id"])
    response = authenticated_notes_service.get_note_by_id(
        prepared_note["id"], expected_status_code=404
    )
    assert (
        response["message"]
        == "No note was found with the provided ID, Maybe it was deleted"
    )


def test_put_note_by_id_cut_title(authenticated_notes_service, prepared_note):
    updated_title = "Cut"
    updated_description = "Updated Description"
    completed = True
    category = "Work"
    response = authenticated_notes_service.put_note_by_id(
        prepared_note["id"],
        updated_title,
        updated_description,
        completed,
        category,
        expected_status_code=400,
    )
    assert response["message"] == "Title must be between 4 and 100 characters"


def test_put_note_by_id_cut_description(authenticated_notes_service, prepared_note):
    updated_title = "Updated Title"
    updated_description = "Cut"
    completed = True
    category = "Work"
    response = authenticated_notes_service.put_note_by_id(
        prepared_note["id"],
        updated_title,
        updated_description,
        completed,
        category,
        expected_status_code=400,
    )
    assert response["message"] == "Description must be between 4 and 1000 characters"


def test_put_note_by_id(authenticated_notes_service, prepared_note):
    updated_title = "Updated Title"
    updated_description = "Updated Description"
    completed = True
    category = "Work"
    response = authenticated_notes_service.put_note_by_id(
        prepared_note["id"], updated_title, updated_description, completed, category
    )
    assert response["message"] == "Note successfully Updated"
    assert response["data"]["id"] == prepared_note["id"]
    assert response["data"]["title"] == updated_title
    assert response["data"]["description"] == updated_description
    assert response["data"]["completed"] == completed
    assert response["data"]["category"] == category


def test_put_note_by_id_deleted_note(authenticated_notes_service, prepared_note):
    updated_title = "Updated Title"
    updated_description = "Updated Description"
    completed = True
    category = "Work"
    authenticated_notes_service.delete_note_by_id(prepared_note["id"])
    response = authenticated_notes_service.put_note_by_id(
        prepared_note["id"],
        updated_title,
        updated_description,
        completed,
        category,
        expected_status_code=404,
    )
    assert (
        response["message"]
        == "No note was found with the provided ID, Maybe it was deleted"
    )


def test_patch_note_by_id_invalid_id(authenticated_notes_service, prepared_note):
    invalid_id = "64e7ce87d1562c00f72546c91"
    completed = True
    response = authenticated_notes_service.patch_note_by_id(
        invalid_id, completed, expected_status_code=400
    )
    assert response["message"] == "Note ID must be a valid ID"


def test_patch_note_by_id(authenticated_notes_service, prepared_note):
    completed = True
    response = authenticated_notes_service.patch_note_by_id(
        prepared_note["id"], completed
    )
    assert response["message"] == "Note successfully Updated"
    assert response["data"]["completed"] == completed
    assert response["data"]["id"] == prepared_note["id"]


def test_patch_note_by_id_deleted_note(authenticated_notes_service, prepared_note):
    completed = True
    authenticated_notes_service.delete_note_by_id(prepared_note["id"])
    response = authenticated_notes_service.patch_note_by_id(
        prepared_note["id"], completed, expected_status_code=404
    )
    assert (
        response["message"]
        == "No note was found with the provided ID, Maybe it was deleted"
    )


def test_delete_note_by_id(authenticated_notes_service, prepared_note):
    response = authenticated_notes_service.delete_note_by_id(prepared_note["id"])
    assert response["message"] == "Note successfully deleted"
