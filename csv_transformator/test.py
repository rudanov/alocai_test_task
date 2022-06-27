from fastapi.testclient import TestClient

from csv_transformator.main import app

client = TestClient(app)

fixtures_path = f'csv_transformator/fixtures'


def test_transform_file():
    with open(f'{fixtures_path}/upload_in.csv', 'rb') as upload_in:
        with open(f'{fixtures_path}/upload_out.csv', 'rb') as upload_out:
            response = client.post("/upload", files={'file': upload_in})

            assert response.status_code == 200
            assert response.content == upload_out.read()
