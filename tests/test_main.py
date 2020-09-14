import unittest

from fastapi.testclient import TestClient

from tdb.camerasuite.app import app


class FastApiBaseTester(unittest.TestCase):
    def setUp(self):
        # mount(url='/static', directory='../src/troydblack/suite/static', name='static')
        self.client = TestClient(app)


class FastApiMainTester(FastApiBaseTester):
    def test_ApiStatusUrl(self):
        response = self.client.get('/api/status')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'status': 'Running'})
