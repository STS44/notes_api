def test_health_check(notes_service):
    response = notes_service.get_health_check()
    assert response["success"] is True
