from abc import ABC, abstractmethod
import re


class ContactInfo(ABC):
    @abstractmethod
    def __init__(self, value: str):
        pass

    def __str__(self):
        return self.value


class EmailAddress(ContactInfo):
    """
    Small component for checking and storing an email address.
    """

    EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Email must be a string, got {type(value)}")

        value = value.strip()

        if len(value) == 0:
            raise ValueError("Email cannot be empty")

        if " " in value:
            raise ValueError("Email cannot contain spaces")

        if len(value) > 254:
            raise ValueError("Email is too long")

        if not re.match(self.EMAIL_PATTERN, value):
            raise ValueError(f"Invalid email address: {value}")

        self.value = value.lower()