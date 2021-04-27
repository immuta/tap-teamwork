"""Teamwork tap class."""

from pathlib import Path
from typing import List

from singer_sdk import Tap, Stream
from singer_sdk.typing import (
    DateTimeType,
    PropertiesList,
    Property,
    StringType,
)

from tap_teamwork.streams import (
    CategoriesStream,
    CompaniesStream,
    LatestActivityStream,
    ProjectsStream,
    ProjectCustomFieldsStream,
    ProjectUpdatesStream,
    PeopleStream,
    MilestonesStream,
    RisksStream,
    TagsStream,
    TasksStream,
)


STREAM_TYPES = [
    CategoriesStream,
    CompaniesStream,
    LatestActivityStream,
    ProjectsStream,
    ProjectCustomFieldsStream,
    ProjectUpdatesStream,
    PeopleStream,
    MilestonesStream,
    RisksStream,
    TagsStream,
    TasksStream,
]


class TapTeamwork(Tap):
    """Teamwork tap class."""

    name = "tap-teamwork"

    config_jsonschema = PropertiesList(
        Property("api_key", StringType, required=True),
        Property("hostname", StringType, required=True),
        Property("start_date", DateTimeType),
        Property("user_agent", StringType, default="tap-teamwork@teamwork.com"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


# CLI Execution:

cli = TapTeamwork.cli
