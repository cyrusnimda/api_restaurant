import unittest
from api.models import DateTimeValidation, PersonsNumberValidation, DateUnknownTypeValidation

class ModelTests(unittest.TestCase):
    mock_config = {
        "BOOKING_HOURS" : [
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', 
        '19:00', '19:30', '20:00', '20:30', '21:00', '21:30',
        '22:00'
        ],
        "DATE_FORMAT" : "%Y-%m-%d %H:%M"
    }

    def test_datetime_validation_no_parameter(self):
        self.assertRaises(TypeError, DateTimeValidation)
        self.assertRaises(TypeError, DateTimeValidation, "2219-12-31 13:00")
        
    def test_datetime_validation_ok(self):
        validation = DateTimeValidation("2019-12-31 13:00", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateTimeValidation("2019-1-1 13:00", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateTimeValidation("2018-12-31 13:00", self.mock_config)
        self.assertTrue(validation.validate())

    def test_datetime_validation_error_format(self):
        self.assertRaises(ValueError, DateTimeValidation, "2018-12-31", self.mock_config )
    
    def test_datetime_validation_error_past(self):
        validation = DateTimeValidation("2018-12-31 13:00", self.mock_config)
        self.assertRaises(ValueError, validation.validate, True)

    def test_datetime_validation_error_config_hours(self):
        validation = DateTimeValidation("2018-12-31 23:00", self.mock_config)
        self.assertRaises(ValueError, validation.validate)

    def test_persons_validation_ok(self):
        validation = PersonsNumberValidation("12")
        self.assertTrue(validation.validate())

    def test_persons_validation_no_parameter(self):
        self.assertRaises(TypeError, PersonsNumberValidation)

    def test_persons_validation_error(self):
        self.assertRaises(ValueError, PersonsNumberValidation, "a")

        validation = PersonsNumberValidation("50")
        self.assertRaises(ValueError, validation.validate)

        validation = PersonsNumberValidation("0")
        self.assertRaises(ValueError, validation.validate)

    def test_date_unknown_validation_ok(self):
        validation = DateUnknownTypeValidation("2019-12-31 13:00", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateUnknownTypeValidation("2019-1-1 13:00", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateUnknownTypeValidation("2018-12-31 13:00", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateUnknownTypeValidation("2019-12-31", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateUnknownTypeValidation("2019-1-1", self.mock_config)
        self.assertTrue(validation.validate())

        validation = DateUnknownTypeValidation("2018-12-31", self.mock_config)
        self.assertTrue(validation.validate())
