"""
Tropical Downloader - Backend API Tests
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "running"


def test_get_config():
    resp = client.get("/api/config")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "download_path" in data["data"]


def test_update_config():
    resp = client.put("/api/config", json={"theme": "dark"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


def test_get_browsers():
    resp = client.get("/api/browsers")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


def test_get_history_empty():
    resp = client.get("/api/history")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_get_tasks_empty():
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


def test_disk_space():
    resp = client.get("/api/disk-space")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "free_gb" in data["data"]


def test_analyze_invalid_url():
    resp = client.post("/api/analyze", json={
        "url": "https://not-a-real-video.example.com/invalid"
    })
    # Should return 400 with an error detail
    assert resp.status_code in (400, 422)


def test_download_invalid_task():
    resp = client.get("/api/download/nonexistent-task")
    assert resp.status_code == 404


def test_channel_backup_invalid():
    resp = client.get("/api/channel-backup/nonexistent")
    assert resp.status_code == 404
