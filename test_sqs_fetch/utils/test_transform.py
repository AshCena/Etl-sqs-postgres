import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
from sqs_fetch.utils.transform import PiiTransformer


class TestPiiTransformer(unittest.TestCase):

    def setUp(self):
        self.data = {
            "Body": json.dumps({
                "user_id": "123",
                "device_type": "ios",
                "ip": "127.0.0.1",
                "device_id": "xabcd",
                "locale": "en-US",
                "app_version": "1.2.3"
            })
        }
        self.transformer = PiiTransformer()

    def test_transform(self):
        with patch('sqs_fetch.utils.transform.mask') as mask, \
                patch('sqs_fetch.utils.transform.datetime') as datetime:

            datetime.now.return_value = "2024, 6, 20"
            mask.side_effect = lambda x: f"x_{x}"

            expected_data = {
                "user_id": "123",
                "device_type": "ios",
                "masked_ip": "x_127.0.0.1",
                "masked_device_id": "x_xabcd",
                "locale": "en-US",
                "app_version": 1,
                "create_date": "2024, 6, 20"
            }

            transformed_data = self.transformer.transform(self.data)
            self.assertEqual(transformed_data, expected_data)
            mask.assert_any_call("127.0.0.1")
            mask.assert_any_call("xabcd")


if __name__ == '__main__':
    unittest.main()
