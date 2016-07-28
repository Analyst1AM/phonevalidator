===============================
phonevalidator
===============================

.. image:: https://img.shields.io/travis/m-housh/phonevalidator.svg
        :target: https://travis-ci.org/m-housh/phonevalidator

.. image:: https://coveralls.io/repos/github/m-housh/phonevalidator/badge.svg?branch=master
        :target: https://coveralls.io/github/m-housh/phonevalidator?branch=master


Custom `cerberus.Validator` for phone numbers


* Free software: MIT license


Features
--------

* Custom validation mixin for `Cerberus`_ or an `Eve`_ API.  
  Uses the `phonenumbers`_ package for validation's and formatting.
  Tested under Python 2.7, Python 3.3, Python 3.4, and Python 3.5.

Basic Usage
-----------
-------

Cerberus Usage:
===============
.. code-block:: python

    from phonevalidator import Validator

    schema = {
        'phone': {
            'type': 'phonenumber',
            'formatPhoneNumber': True,
            'phoneNumberFormat': 'NATIONAL',
            'region': 'US',
        },
    }

    doc = {'phone': '5135555555'}

    v = Validator(schema)
    v.validate(doc)
    # True
    v.document
    # {'phone': '(513) 555-5555'}

    doc = {'phone': 'gibberish'}
    v.validate(doc)
    # False

Eve Usage:
==========
.. code-block:: python

    from phonevalidator import ValidatorMixin
    from eve.io.mongo import Validator
    from eve import Eve


    class MyValidator(Validator, ValidatorMixin):
        """ My custom validator that includes phone number 
        validations.
        """
        pass


    app = Eve(validator=MyValidtor)
    ...


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

This package also use the `phonenumbers`_ package which is licensed under
the `Apache2`_ license. The `Cerberus`_ package which is an open-source project.
`Eve`_ is licensed under the `BSD`_ license.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Cerberus`:  http://docs.python-cerberus.org
.. _`Eve`: http://python-eve.org
.. _`phonenumbers`:  https://github.com/daviddrysdale/python-phonenumbers
.. _`Apache2`: http://www.apache.org/licenses/LICENSE-2.0
.. _`BSD`: http://python-eve.org/license.html
