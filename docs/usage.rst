=====
Usage
=====

To use phonevalidator in a project::

    import phonevalidator
    from eve import Eve

    app = Eve(validator=phonevalidator.Validator)
    ...

Validation Examples::
    
    from phonevalidator import Validator

    schema = {
        'phone': {
            'type': 'phonenumber',
            'region': 'US', # default
            'formatPhoneNumber': True,
            'phoneNumberFormat': 'NATIONAL',  # default
        }
    }

    doc = {'phone': '5135555555'}
    validator = Validator(schema)

    print(validator.validate(doc))
    # True
    print(validator.document)
    # {'phone': '(513) 555-5555'}

.. note:: Default region is 'US', default phoneNumberFormat is 'NATIONAL'.
    These can also be set using environment variables.  To set the region
    using and environment variable use 'DEFAULT_PHONE_REGION' and use
    'PHONE_NUMBER_FORMAT' to set the phoneNumberFormat.
    
.. seealso:: :class:`phonenumbers.PhoneNumberFormat`: for valid formats

Similar to above, but using defaults::

    from phonevalidator import Validator


    schema = {
        'phone': {
            'type': 'phonenumber',
            'formatPhoneNumber': True,
        }
    }

    doc = {'phone': '5135555555;ext=1234'}
    validator = Validator(schema)

    print(validator.validate(doc))
    # True
    print(validator.document)
    # {'phone': '(513) 555-5555 ext. 1234'}


