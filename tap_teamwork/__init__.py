#!/usr/bin/env python3

import singer

from tap_teamwork.runner import teamworkRunner
from tap_teamwork.client import teamworkClient
from tap_teamwork.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=["api_key", "workspace"])
    client = teamworkClient(args.config)
    runner = teamworkRunner(args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == "__main__":
    main()
