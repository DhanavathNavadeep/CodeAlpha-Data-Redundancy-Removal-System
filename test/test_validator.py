import unittest
from models.validator import validate


class TestValidator(unittest.TestCase):

    def test_valid_record(self):
        record = {
            "Name": "John",
            "Email": "john@gmail.com",
            "Phone": "9876543210"
        }
        self.assertTrue(validate(record))

    def test_empty_name(self):
        record = {
            "Name": "",
            "Email": "john@gmail.com",
            "Phone": "9876543210"
        }
        self.assertFalse(validate(record))

    def test_invalid_email(self):
        record = {
            "Name": "John",
            "Email": "johngmail.com",
            "Phone": "9876543210"
        }
        self.assertFalse(validate(record))

    def test_invalid_phone_length(self):
        record = {
            "Name": "John",
            "Email": "john@gmail.com",
            "Phone": "98765"
        }
        self.assertFalse(validate(record))

    def test_phone_contains_letters(self):
        record = {
            "Name": "John",
            "Email": "john@gmail.com",
            "Phone": "98765ABCD1"
        }
        self.assertFalse(validate(record))

    def test_missing_email(self):
        record = {
            "Name": "John",
            "Email": "",
            "Phone": "9876543210"
        }
        self.assertFalse(validate(record))


if __name__ == "__main__":
    unittest.main()