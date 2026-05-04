import pytest

from backend.app.utils.email_address import ContactInfo, EmailAddress


TEST_EMAIL = "test@example.com"


def test_contact_info_base_class():
    with pytest.raises(TypeError):
        ContactInfo(TEST_EMAIL)


def test_construct_email():
    email = EmailAddress(TEST_EMAIL)
    assert isinstance(email, EmailAddress)


def test_construct_email_bad_type():
    with pytest.raises(TypeError):
        EmailAddress(42)


def test_construct_email_empty_string():
    with pytest.raises(ValueError):
        EmailAddress("")


def test_construct_email_only_spaces():
    with pytest.raises(ValueError):
        EmailAddress("   ")


def test_construct_email_no_at_symbol():
    with pytest.raises(ValueError):
        EmailAddress("testexample.com")


def test_construct_email_no_domain():
    with pytest.raises(ValueError):
        EmailAddress("test@")


def test_construct_email_no_username():
    with pytest.raises(ValueError):
        EmailAddress("@example.com")


def test_construct_email_no_dot():
    with pytest.raises(ValueError):
        EmailAddress("test@example")


def test_construct_email_has_space():
    with pytest.raises(ValueError):
        EmailAddress("test user@example.com")


def test_email_is_lowercase():
    email = EmailAddress("Test@Example.COM")
    assert str(email) == "test@example.com"


def test_email_str():
    email = EmailAddress(TEST_EMAIL)
    assert str(email) == TEST_EMAIL