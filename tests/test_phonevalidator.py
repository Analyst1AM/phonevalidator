#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_phonevalidator
----------------------------------

Tests for `phonevalidator` module.
"""

import pytest
import os

from phonevalidator.phonevalidator import (
    Validator,
    _formatter,
    _default_formatter,
    _default_region,
)

from phonenumbers import PhoneNumberFormat

@pytest.fixture
def base_schema():
    return {'phone': {'type': 'phonenumber', 'region': 'US'}}


def test_formatter_method():
    # default
    assert _formatter() == PhoneNumberFormat.NATIONAL
    # returns the correct format even if not capitalized 
    assert _formatter('InTeRNATIONAL') == PhoneNumberFormat.INTERNATIONAL

def test_default_formatter_method():
    assert _default_formatter() == 'DEFAULT'
    os.environ['PHONE_NUMBER_FORMAT'] = 'INTERNATIONAL'
    assert _default_formatter() == 'INTERNATIONAL'
    os.environ['PHONE_NUMBER_FORMAT'] = ''

def test_default_region_method():
    assert _default_region() == 'US'
    os.environ['DEFAULT_PHONE_REGION'] = 'EN'
    assert _default_region() == 'EN'
    os.environ['DEFAULT_PHONE_REGION'] = ''


def test_phonenumber_fail(base_schema):
    doc = {'phone': 'gibberish'}
    v = Validator(base_schema)
    assert v.validate(doc) is False

    doc['phone'] = '+41513555'
    assert v.validate(doc) is False


def test_phone_number_valid(base_schema):
    base_schema['phone']['region'] = 'US'
    doc = {'phone': '5135555555'}
    v = Validator(base_schema)
    assert v.validate(doc)
    assert v.document['phone'] == '5135555555'

def test_phoneNumberFormat_fail(base_schema):
    base_schema['phone'].update({
        'phoneNumberFormat': 'InvalidFormat',
        'formatPhoneNumber': True,
        'region': 'US',
    })
    doc = {'phone': '5135555555'}
    v = Validator(base_schema)
    assert v.validate(doc) is False


def test_phone_gets_formatted(base_schema):
    base_schema['phone'].update({
        'formatPhoneNumber': True,
        'phoneNumberFormat': 'NATIONAL',
        'region': 'US'})
    doc = {'phone': '5135555555'}
    v = Validator(base_schema)
    assert v.validate(doc)
    assert v.document['phone'] == '(513) 555-5555'
