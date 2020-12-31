import singer

from tap_teamwork.base import BaseStream, TimeRangeByObjectStream


LOGGER = singer.get_logger()


class LatestActivityStream(BaseStream):
    TABLE = "latest_activity"
    RESPONSE_KEY= "activities"

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


    @property
    def path(self):
        return f"projects.json"


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


# class TaskStream(TimeRangeByObjectStream):
#     API_METHOD = "GET"
#     TABLE = "tasks"
#     KEY_PROPERTIES = ["id"]
#     REPLACEMENT_STRING = "<VAR>"

#     CACHE_RESULTS = True

#     def get_object_list(self):
#         url = self.get_url_base() + f"/workspaces/{self.config['workspace']}/projects"
#         api_method = "GET"
#         params = {"page-size": 500}
#         results = self.client.make_request(url, api_method, params=params)
#         return [r["id"] for r in results]

#     @property
#     def path(self):
#         return f"/workspaces/{self.config['workspace']}/projects/<VAR>/tasks"


# class TimeEntryStream(TimeRangeByObjectStream):
#     API_METHOD = "GET"
#     TABLE = "time_entries"
#     KEY_PROPERTIES = ["id"]
#     REPLACEMENT_STRING = "<VAR>"

#     CACHE_RESULTS = True

#     def get_object_list(self):
#         url = self.get_url_base() + f"/workspaces/{self.config['workspace']}/users"
#         api_method = "GET"
#         params = {"page-size": 500, "memberships": "NONE"}
#         results = self.client.make_request(url, api_method, params=params)
#         return [r["id"] for r in results]

#     @property
#     def path(self):
#         return f"/workspaces/{self.config['workspace']}/user/<VAR>/time-entries"


AVAILABLE_STREAMS = [
    LatestActivityStream,
    ProjectsStream,
    ProjectUpdatesStream,
    PeopleStream,
    MilestonesStream,
    RisksStream,
    TagsStream,
]
