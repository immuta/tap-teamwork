"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests
from tap_teamwork.tap import TapTeamwork


SAMPLE_CONFIG = {
    "api_key": "my_api_key",
    "hostname": "https://company.teamwork.com",
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapTeamwork, config=SAMPLE_CONFIG)
    for test in tests:
        test()
