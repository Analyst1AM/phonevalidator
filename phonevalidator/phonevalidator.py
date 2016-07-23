# -*- coding: utf-8 -*-

from eve.io.mongo import Validator
from os import environ
from phonenumbers import (
    format_number,
    is_valid_number,
    parse,
    NumberParseException,
    PhoneNumberFormat
)


_formats = {
    'NATIONAL': PhoneNumberFormat.NATIONAL,
    'INTERNATIONAL': PhoneNumberFormat.INTERNATIONAL,
    'E164': PhoneNumberFormat.E164,
    'RFC3966': PhoneNumberFormat.RFC3966,
    'DEFAULT': PhoneNumberFormat.NATIONAL,
}

def _default_formatter():
    return environ.get('PHONE_NUMBER_FORMAT', 'DEFAULT')

def _default_region():
    return environ.get('DEFAULT_PHONE_REGION', 'US')

def _formatter(formatter=None):
    # returns a phonenumber.PhoneNumberFormat used to format
    # a phone number.
    if not formatter or not isinstance(formatter, str):
        formatter = _default_formatter()
    return _formats.get(formatter.upper())
    
class Validator(Validator):

    def _validate_formatPhoneNumber(self, formatPhoneNumber, field, value):
        """ Fake validate function to let cerberus accept "formatPhoneNumber"
            as a keyword in the schema.

        """
        pass

    def _validate_phoneNumberFormat(self, phoneNumberFormat, field, value):
        """ Fake validate function to let cerberus accept "phoneNumberFormat"
            as a keyword in the schema.

            :param phoneNumberFormat:  a string for accepted format.
                :accepted formats: ['NATIONAL', 'INTERNATIONAL', 'RFC3966', 'E164']

        """
        print('phoneNumberFormat', phoneNumberFormat)
        if phoneNumberFormat.upper() not in _formats.keys():
            self._error(field,
                        'Not a valid phone number format: {}'.format(value))

    def _validate_region(self, region, field, value):
        """ Fake validate function to let cerberus accept "region"
            as a keyword in the schema.

        """
        pass

    def _validate_type_phonenumber(self, field, value):
        """ Validates a phone number is valid. Optionally formatting the number.
            
            :param field:  field name.
            :param value:  field value.
        """
        # get the region from schema for this field or use default
        region = self.schema[field].get('region', _default_region())
        try:
            phone_number = parse(value, region)

            # check that it's valid number
            if not is_valid_number(phone_number):
                self._error(field, 'Phone Number not valid: {}'.format(value))
            elif self.schema[field].get('formatPhoneNumber'):
                # if the schema's 'formatPhoneNumber' is set to True,
                # format the phone number using a formatter derived from
                # the schema's 'phoneNumberFormat' value, next checks the environment
                # variable 'PHONE_NUMBER_FORMAT', or defaults to 'NATIONAL'.
                #
                formatter = _formatter(
                    self.schema[field].get('phoneNumberFormat') 
                )
                self.document[field] = format_number(phone_number, formatter)
        except NumberParseException:
            self._error(field, 'Phone Number not valid: {}'.format(value))
