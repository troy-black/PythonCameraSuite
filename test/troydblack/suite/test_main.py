from test.troydblack.suite import FastApiBaseTester


class FastApiMainTester(FastApiBaseTester):
    def test_ApiStatusUrl(self):
        response = self.client.get('/api/status')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'status': 'Running'})
