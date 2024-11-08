"""irrigation_unlimited test for logging"""

# pylint: disable=unused-import
from unittest.mock import patch
import homeassistant.core as ha
from custom_components.irrigation_unlimited.irrigation_unlimited import (
    IULogger,
)
from tests.iu_test_support import IUExam

IUExam.quiet_mode()


async def test_link_ids(hass: ha.HomeAssistant, skip_dependencies, skip_history):
    """Test invalid, duplicate and orphaned ids."""
    # pylint: disable=unused-argument

    with patch.object(IULogger, "log_duplicate_id") as mock_duplicate:
        with patch.object(IULogger, "log_orphan_id") as mock_orphan:
            async with IUExam(hass, "test_ids.yaml"):
                assert mock_duplicate.call_count == 7
                assert mock_orphan.call_count == 1

    with patch.object(IULogger, "_format") as mock:
        async with IUExam(hass, "test_ids.yaml"):
            assert (
                sum(1 for call in mock.call_args_list if call.args[1] == "DUPLICATE_ID")
                == 7
            )
            assert (
                sum(1 for call in mock.call_args_list if call.args[1] == "ORPHAN_ID")
                == 1
            )
