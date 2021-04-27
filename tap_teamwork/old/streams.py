import singer

from tap_teamwork.base import BaseStream, TimeRangeByObjectStream


LOGGER = singer.get_logger()


class CompaniesStream(BaseStream):
    TABLE = "companies"
    RESPONSE_KEY = "companies"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"companies.json"

    # The 'companies' endpoint is only in API version 1, so requires a different base
    def get_url_base(self):
        return self.config["hostname"] + "/"


class LatestActivityStream(BaseStream):
    TABLE = "latest_activity"
    RESPONSE_KEY = "activities"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"latestactivity.json"


class MilestonesStream(BaseStream):
    TABLE = "milestones"
    RESPONSE_KEY = "milestones"

    CACHE_RESULTS = True

    @property
    def path(self):
        return "milestones.json"


class ProjectsStream(BaseStream):
    TABLE = "projects"
    RESPONSE_KEY = "projects"

    params = {"includeArchivedProjects": True}

    @property
    def path(self):
        return f"projects.json"


class ProjectCustomFieldsStream(BaseStream):
    TABLE = "project_custom_fields"
    RESPONSE_KEY = "included"

    CACHE_RESULTS = True

    @property
    def path(self):
        return "projects.json"

    def get_params(self, page=1):
        return {
            "updatedAfter": None,
            "page": page,
            "pageSize": 250,
            "includeCustomFields": True,
            "fields[customfields]": "[id,entity,name,description,type]",
        }

    def sync_paginated(self, url, params):
        table = self.TABLE
        _next = True
        page = 1

        all_resources = []
        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)
            custom_fields = result.get("included", {}).get("customfields", {})
            raw_records = result.get("included", {}).get("customfieldProjects", {})
            proc_records = []
            for k, v in raw_records.items():
                combined = {**v, **custom_fields[str(v.get("customfieldId"))]}
                proc_records.append(combined)

            data = self.get_stream_data(proc_records)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, data)
                counter.increment(len(data))
                all_resources.extend(data)

            LOGGER.info("Synced page %s for %s", page, self.TABLE)
            params["page"] = params["page"] + 1
            if len(data) < params.get("pageSize", 250):
                _next = None
        return all_resources


class PeopleStream(BaseStream):
    TABLE = "people"
    RESPONSE_KEY = "people"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"people.json"


class ProjectUpdatesStream(BaseStream):
    TABLE = "project_updates"
    RESPONSE_KEY = "projectUpdates"

    CACHE_RESULTS = True

    @property
    def path(self):
        return "projects/updates.json"


class RisksStream(BaseStream):
    TABLE = "risks"
    RESPONSE_KEY = "risks"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"risks.json"


class TagsStream(BaseStream):
    TABLE = "tags"
    RESPONSE_KEY = "tags"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"tags.json"


class TasksStream(BaseStream):
    TABLE = "tasks"
    RESPONSE_KEY = "todo-items"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"tasks.json"

    def get_params(self, page=1):
        return {
            "updatedAfter": None,
            "page": page,
            "pageSize": 250,
            "includeCompletedTasks": True,
        }

    # The 'tasks' endpoint is only in API version 1, so requires a different base
    def get_url_base(self):
        return self.config["hostname"] + "/"


class CategoriesStream(BaseStream):
    TABLE = "categories"
    RESPONSE_KEY = "categories"

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"projectCategories.json"

    def get_params(self, page=1):
        return {
            "updatedAfter": None,
            "page": page,
            "pageSize": 250,
        }

    # The 'tasks' endpoint is only in API version 1, so requires a different base
    def get_url_base(self):
        return self.config["hostname"] + "/"


AVAILABLE_STREAMS = [
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
