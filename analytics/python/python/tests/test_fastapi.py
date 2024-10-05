import pytest
import subprocess
import time
import requests


FASTAPI_APP_DIR = "./tests/integration/fastapi"
HOST = "127.0.0.1"
PORT = "8000"
BASE_URL = f"http://{HOST}:{PORT}"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Start FastAPI server as a subprocess
    process = subprocess.Popen(
        ["uvicorn", "app:app", "--host", HOST, "--port", PORT],
        cwd=FASTAPI_APP_DIR,
    )

    # Wait for the server to start
    time.sleep(2)

    yield  # Allow tests to run

    process.terminate()
    process.wait()


def test_response():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_speed():
    response_times = [timed_request() for _ in range(100)]
    average_response_time = sum(response_times) / len(response_times)
    print(f"Average response time: {average_response_time*1000:.4f} ms")
    assert average_response_time < 0.1


def timed_request():
    start = time.time()
    _ = requests.get(BASE_URL)
    end = time.time()
    return end - start
