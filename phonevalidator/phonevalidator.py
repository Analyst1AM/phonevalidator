# -*- coding: utf-8 -*-

from eve.io.mongo import Validator
from os import environ
from phonenumbers import (
    format_number,
    is_valid_number,
    parse,
    NumberParseException,
    PhoneNumberFormat,
    SUPPORTED_REGIONS,
)


class Validator(Validator):
    """ A custom cerberus.Validator subclass adding the `phonenumber` constraint
    to Cerberus validation's.

    """
    def __init__(self, *args, formatter=None, region=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = None
        self.region = None

        if formatter is not None:
            self._set_formatter(
                formatter=formatter
            )

        if region is not None:
            self._set_region(
                region=region
            )

    def _default_region(self):
        region = environ.get('DEFAULT_PHONE_REGION')
        if region and region.upper() in SUPPORTED_REGIONS:
            return region.upper()
        return 'US'

    def _is_valid_region(self, region):
        if isinstance(region, str) and region.upper() in SUPPORTED_REGIONS:
            return True
        return False

    def _set_region(self, region=None):
        if self._is_valid_region(region):
            self.region = region.upper()
        else:
            self.region = self._default_region()

    def _set_default_formatter(self):
        env_format = environ.get('DEFAULT_PHONE_FORMAT')
        if env_format is not None:
            self._set_formatter(
                formatter=env_format
            )
        else:
            self.formatter = PhoneNumberFormat.NATIONAL

    def _set_formatter(self, formatter=None):
        if formatter is None or not isinstance(formatter, str):
            self._set_default_formatter()
        else:
            self.formatter = getattr(
                PhoneNumberFormat,
                formatter.upper(),
                PhoneNumberFormat.NATIONAL
            )

    def _validate_formatPhoneNumber(self, formatPhoneNumber, field, value):
        """ Fake validate function to let cerberus accept "formatPhoneNumber"
            as a keyword in the schema.

        """
        pass

    def _validate_phoneNumberFormat(self, phoneNumberFormat, field, value):
        """ Fake validate function to let cerberus accept "phoneNumberFormat"
            as a keyword in the schema.

            :param phoneNumberFormat:  a string for accepted format.
            :accepted formats: ['NATIONAL',
                                'INTERNATIONAL',
                                'RFC3966',
                                'E164'
                                ]

        """
        keys = PhoneNumberFormat.__dict__.keys()
        valids = [key for key in keys if not key.startswith('_')]

        if phoneNumberFormat.upper() not in valids:
            self._error(field,
                        'Not a valid phone number format: {}'.format(value))

    def _validate_region(self, region, field, value):
        """ Fake validate function to let cerberus accept "region"
            as a keyword in the schema.

        """
        if self._is_valid_region(region) is False:
            self._error(field,
                        'Region not valid: {}'.format(region))

    def _validate_type_phonenumber(self, field, value):
        """ Validates a phone number is valid. Optionally formatting the number.

            :param field:  field name.
            :param value:  field value.
        """
        # get the region from schema for this field or use default
        self._set_region(self.schema[field].get('region'))
        try:
            phone_number = parse(value, self.region)

            # check that it's valid number
            if not is_valid_number(phone_number):
                self._error(field, 'Phone Number not valid: {}'.format(value))
            elif self.schema[field].get('formatPhoneNumber'):
                # if the schema's 'formatPhoneNumber' is set to True,
                # format the phone number using a formatter derived from
                # the schema's 'phoneNumberFormat' value, next checks the
                # environmen variable 'PHONE_NUMBER_FORMAT',
                # or defaults to 'NATIONAL'.
                formatter = self.schema[field].get('phoneNumberFormat')
                self._set_formatter(
                    formatter=formatter
                )
                self.document[field] = format_number(phone_number,
                                                     self.formatter)
        except NumberParseException:
            self._error(field, 'Phone Number not valid: {}'.format(value))
