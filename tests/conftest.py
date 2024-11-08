"""Global fixtures for irrigation_unlimited integration."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch
import pytest

# pylint: disable=invalid-name
# pylint: disable=unused-argument

pytest_plugins = "pytest_homeassistant_custom_component"

# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(hass, enable_custom_integrations):
    """Allow custom integrations to load"""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture(autouse=True)
def auto_enable_unix_sockets(socket_enabled):
    """Allow the use of sockets. Required for http integration"""
    yield


# Prevent HomeAssistant from loading the Irrigation Unlimited dependencies which
# are currently "history" which requires "recorder" which requires "http".
@pytest.fixture(name="skip_dependencies", autouse=True)
def skip_dep():
    """Skip loading dependencies"""
    with patch("homeassistant.loader.Integration.dependencies", return_value=[]):
        yield


@pytest.fixture(name="skip_setup")
def skip_setup():
    """Fake the coordinator is setup"""
    with patch(
        "custom_components.irrigation_unlimited.IUCoordinator._is_setup",
        return_value=True,
    ):
        yield


@pytest.fixture(name="skip_history")
def skip_history():
    """Skip history calls"""
    with patch(
        "homeassistant.components.recorder.history.get_significant_states",
        return_value=[],
    ):
        yield


@pytest.fixture(name="skip_start")
def skip_start():
    """Skip coordinator start calls"""
    with patch(
        "custom_components.irrigation_unlimited.IUClock.start",
        return_value=None,
    ):
        yield

@pytest.fixture(name="allow_memory_db")
def allow_memory_db():
    """Allow in memory DB"""
    with patch(
        "homeassistant.components.recorder.ALLOW_IN_MEMORY_DB",
        return_value=True,
    ):
        yield
