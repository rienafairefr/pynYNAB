from __future__ import print_function
import os

import argparse
import re
import six
import yaml


DEFAULT_CONFIG_FILE = 'ynab.yaml'


class ConfigEnvArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ConfigEnvArgumentParser, self).__init__(*args, **kwargs)

        try:
            self.add_argument('--config', dest='config',
                          help='a yaml file containing the config')
        except argparse.ArgumentError:
            # --config already exists
            pass

    def parse_args(self, *args, **kwargs):
        parsed_args = vars(super(ConfigEnvArgumentParser, self).parse_args(*args, **kwargs))

        parsed_args_config = merge_config(parsed_args)
        if parsed_args_config is None:
            self.error('invalid config file was passed')

        return AttrDict(**parsed_args_config)


def get_config_from_yaml(config_file=DEFAULT_CONFIG_FILE):
    try:
        with open(config_file, 'r') as stream:
            yaml_content = yaml.load(stream)
            if yaml_content is not None:
                return yaml_content
    except:
        return {}


def get_config_from_env():
    valid_key = re.compile(r'^N?YNAB_(?P<key>.*)$')
    returnvalue = {}
    for key, value in os.environ.items():
        match = valid_key.match(key)
        if match:
            key_name = match.group('key').lower()
            returnvalue[key_name] = value
    return returnvalue


def merge_config(arguments=None, nominal=DEFAULT_CONFIG_FILE):
    if arguments is None:
        arguments = {}
    cli_config = arguments
    env_config = get_config_from_env()
    ynab_yaml_config = get_config_from_yaml(nominal)

    # cli-passed > cli-passed-config > ynab.yaml > ENV
    merged_config = merge(ynab_yaml_config, env_config)
    if hasattr(arguments, 'config') and arguments.config:
        cli_passed_config = get_config_from_yaml(arguments.config)
        merged_config = merge(cli_passed_config, merged_config)
    merged_config = merge(cli_config, merged_config)

    print('Config used:')
    print('------------')
    print(yaml.dump(merged_config), end='')
    print('------------')
    return merged_config


def merge(user, default):
    if isinstance(user, dict) and isinstance(default, dict):
        for key, value in six.iteritems(default):
            if key not in user:
                user[key] = value
            else:
                user[key] = merge(user[key], value)
    return user


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
