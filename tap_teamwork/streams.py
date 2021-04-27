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
        self, partition: Optional[dict], next_page_token: Optional[Any] = 0
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.
        If paging is supported, developers may override this method with specific paging
        logic.
        """
        params = {
            "updatedAfter": None,
            "page": next_page_token,
            "pageSize": self._page_size
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
        return {"includeArchivedProjects": True}


class ProjectCustomFieldsStream(TeamworkStream):
    name = "project_custom_fields"
    path = "projects.json"
    primary_keys = ["id"]
    response_result_key = "included"
    schema_filepath = SCHEMAS_DIR / "project_custom_fields.json"

    def get_url_params(self, partition, next_page_token=None):
        return {
            "includeArchivedProjects": True,
            "page": next_page_token,
            "pageSize": self._page_size,
            "includeCustomFields": True,
            "fields[customfields]": "[id,entity,name,description,type]",
        }

    # def sync_paginated(self, url, params):
    #     table = self.TABLE
    #     _next = True
    #     page = 1

    #     all_resources = []
    #     while _next is not None:
    #         result = self.client.make_request(url, self.API_METHOD, params=params)
    #         custom_fields = result.get("included", {}).get("customfields", {})
    #         raw_records = result.get("included", {}).get("customfieldProjects", {})
    #         proc_records = []
    #         for k, v in raw_records.items():
    #             combined = {**v, **custom_fields[str(v.get("customfieldId"))]}
    #             proc_records.append(combined)

    #         data = self.get_stream_data(proc_records)

    #         with singer.metrics.record_counter(endpoint=table) as counter:
    #             singer.write_records(table, data)
    #             counter.increment(len(data))
    #             all_resources.extend(data)

    #         LOGGER.info("Synced page %s for %s", page, self.TABLE)
    #         params["page"] = params["page"] + 1
    #         if len(data) < params.get("pageSize", 250):
    #             _next = None
    #     return all_resources



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
            "pageSize": 250,
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
            "pageSize": 250,
        }
