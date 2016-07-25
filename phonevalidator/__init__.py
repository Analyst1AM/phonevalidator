# -*- coding: utf-8 -*-

from .phonevalidator import ValidatorMixin
from cerberus import Validator as SuperValidator


class Validator(SuperValidator, ValidatorMixin):
    """ Extends `cerberus.Validator` and adds the `phonenumber` constraint
    to Cerburus validation's.

    :Example:

    .. code-block:: python

        >>> from phonevalidator import Validator
        >>> schema = {
        ...     'phone': {
        ...         'type': 'phonenumber',
        ...         'formatPhoneNumber': True,
        ...         'phoneNumberFormat': 'NATIONAL',
        ...         'region': 'US'
        ...     }
        ... }
        >>> doc = {'phone': '5135555555'}
        >>> v = Validator(schema)
        >>> v.validate(doc)
        True
        >>> v.document
        {'phone': '(513) 555-5555'}
        >>> doc = {'phone': 'gibberish'}
        >>> v.validate(doc)
        False


    """
    pass

__author__ = 'Michael Housh'
__email__ = 'mhoush@houshhomeenergy.com'
__version__ = '1.1.0'
__all__ = ['Validator', 'ValidatorMixin']
