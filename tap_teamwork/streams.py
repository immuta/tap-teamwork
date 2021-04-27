"""Stream class for tap-teamwork."""

import requests

from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from singer_sdk.streams import RESTStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TeamworkStream(RESTStream):
    """Teamwork stream class."""

    response_result_key = None
    _page_size = 250

    @property
    def http_headers(self) -> dict:
        "Implement Basic Auth with API Key as username and dummy password"
        result = super().http_headers

        api_key = self.config.get("api_key")
        auth = b64encode(f"{api_key}:xxx".encode()).decode()

        result["Authorization"] = f"Basic {auth}"

        return result

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["hostname"] + "/projects/api/v3/"

    def get_url_params(
        self, partition: Optional[dict], next_page_token: Optional[Any] = 1
    ) -> Dict[str, Any]:
        params = {
            "updatedAfter": None,
            "page": next_page_token,
            "pageSize": self._page_size,
        }
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        if self.response_result_key:
            resp_json = resp_json.get(self.response_result_key, {})
        if isinstance(resp_json, dict):
            yield resp_json
        else:
            for row in resp_json:
                yield row

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Union[int, None],
    ) -> Union[int, None]:

        previous_token = previous_token or 0
        data = response.json()
        results = data.get(self.response_result_key, data)

        if len(results) >= self._page_size:
            return previous_token + 1

        return None


class CompaniesStream(TeamworkStream):
    name = "companies"
    path = "/companies.json"
    primary_keys = ["id"]
    response_result_key = "companies"
    schema_filepath = SCHEMAS_DIR / "companies.json"

    @property
    def url_base(self) -> str:
        """The 'companies' endpoint is only in API version 1, so requires a different base"""
        return self.config["hostname"] + "/"


class LatestActivityStream(TeamworkStream):
    name = "latest_activity"
    path = "latestactivity.json"
    primary_keys = ["id"]
    response_result_key = "activities"
    schema_filepath = SCHEMAS_DIR / "latest_activity.json"


class MilestonesStream(TeamworkStream):
    name = "milestones"
    path = "milestones.json"
    response_result_key = "milestones"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "milestones.json"


class PeopleStream(TeamworkStream):
    name = "people"
    path = "people.json"
    primary_keys = ["id"]
    response_result_key = "people"
    schema_filepath = SCHEMAS_DIR / "people.json"


class ProjectsStream(TeamworkStream):
    name = "projects"
    path = "projects.json"
    primary_keys = ["id"]
    response_result_key = "projects"
    schema_filepath = SCHEMAS_DIR / "projects.json"

    def get_url_params(self, partition, next_page_token=None):
        return {
            "includeArchivedProjects": True,
            "page": next_page_token,
            "pageSize": self._page_size,
        }


class ProjectCustomFieldsStream(TeamworkStream):
    name = "project_custom_fields"
    path = "projects.json"
    primary_keys = ["id"]
    response_result_key = "included"
    schema_filepath = SCHEMAS_DIR / "project_custom_fields.json"

    def get_url_params(self, partition, next_page_token=None):
        return {
            "includeArchivedProjects": True,
            "fields[customfields]": "[id,entity,name,description,type]",
            "includeCustomFields": True,
            "page": next_page_token,
            "pageSize": self._page_size,
        }

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()

        # Extract custom fields
        custom_fields = resp_json.get("included", {}).get("customfields", {})
        raw_records = resp_json.get("included", {}).get("customfieldProjects", {})

        for k, v in raw_records.items():
            merged = {**v, **custom_fields[str(v.get("customfieldId"))]}
            yield merged


class ProjectUpdatesStream(TeamworkStream):
    name = "project_updates"
    path = "projects/updates.json"
    primary_keys = ["id"]
    response_result_key = "projectUpdates"
    schema_filepath = SCHEMAS_DIR / "project_updates.json"


class RisksStream(TeamworkStream):
    name = "risks"
    path = "risks.json"
    primary_keys = ["id"]
    response_result_key = "risks"
    schema_filepath = SCHEMAS_DIR / "risks.json"


class TagsStream(TeamworkStream):
    name = "tags"
    path = "tags.json"
    primary_keys = ["id"]
    response_result_key = "tags"
    schema_filepath = SCHEMAS_DIR / "tags.json"


class TasksStream(TeamworkStream):
    name = "tasks"
    path = "tasks.json"
    primary_keys = ["id"]
    response_result_key = "todo-items"
    schema_filepath = SCHEMAS_DIR / "tasks.json"

    @property
    def url_base(self) -> str:
        """The 'tasks' endpoint is only in API version 1, so requires a different base"""
        return self.config["hostname"] + "/"

    def get_url_params(self, partition, next_page_token=None):
        return {
            "updatedAfter": None,
            "page": next_page_token,
            "pageSize": self._page_size,
            "includeCompletedTasks": True,
        }


class CategoriesStream(TeamworkStream):
    name = "categories"
    path = "projectCategories.json"
    primary_keys = ["id"]
    response_result_key = "categories"
    schema_filepath = SCHEMAS_DIR / "categories.json"

    @property
    def url_base(self) -> str:
        """The 'catgories' endpoint is only in API version 1, so requires a different base"""
        return self.config["hostname"] + "/"

    def get_url_params(self, partition, next_page_token=None):
        return {
            "updatedAfter": None,
            "page": next_page_token,
            "pageSize": self._page_size,
        }
