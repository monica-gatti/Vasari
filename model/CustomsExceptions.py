# !/usr/bin/python
# coding=utf-8
class ObjectNotFoundException(Exception):
    """Exception raised for errors in retrieving objects.

    Attributes:
        id -- input id which caused the error
        message -- explanation of the error
    """

    def __init__(self, id, message="instance not present for id: "):
        self.id = id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} -> {self.id}'
class ArgumentOutOfRangeException(Exception):
    """Exception raised for errors in parameters.

    Attributes:
        field -- input which caused the error
        message -- explanation of the error
    """

    def __init__(self, field, message="wrong parameter: "):
        self.field = field
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} -> {self.field}'
class GenericErrorException(Exception):
    """Exception raised for generic errors like service unavailability of misconfiguration.

    Attributes:
        technical_details -- cause of the error
        message -- explanation of the error
    """

    def __init__(self, technical_details, message="not present"):
        self.technical_details = technical_details
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} -> {self.technical_details}'