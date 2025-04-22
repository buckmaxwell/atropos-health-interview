def test_get_task_types(client):
    response = client.get("/task-types")
    assert response.status_code == 200

    task_types = response.json()
    assert isinstance(task_types, list)
    assert len(task_types) >= 1

    first = task_types[0]
    assert "type" in first
    assert "description" in first
    assert "payload_schema" in first

    schema = first["payload_schema"]
    assert "$schema" in schema
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "properties" in schema
    assert "file_url" in schema["properties"]
