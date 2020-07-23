from test.troydblack.camera import FlaskAppBaseTester


class FlaskAppTester(FlaskAppBaseTester):
    def test_StatusUrl(self):
        result = self.app.get('/status')

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.json, {'status': 'Running'})
