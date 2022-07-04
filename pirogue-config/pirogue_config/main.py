import subprocess

from defaults import DEFAULTS, PIROGUE_CONF
from parsers.commander import Commander
from parsers.ini_parser import IniParser
from parsers.key_value_pair import KeyValuePairParser
from parsers.yaml_parser import YamlParser
import os


class PiRogueConfiguration:
    def __init__(self):
        self.default_configuration = {}
        self.load_default_configuration()
        self.configuration = self.default_configuration
        if os.path.exists(PIROGUE_CONF.get('location')):
            self.load_configuration()

    def load_configuration(self):
        kv_file = self._get_service_configuration_handler('PiRogue', PIROGUE_CONF)
        self.configuration = kv_file.get_data()

    def load_default_configuration(self):
        for service, definition in DEFAULTS.items():
            self.default_configuration.update(definition.get('defaults'))

    def generate_configuration_file(self, use_default=False):
        kv_file = self._get_service_configuration_handler('PiRogue', PIROGUE_CONF)
        configuration = self.configuration
        if use_default:
            configuration = self.default_configuration
        for k, v in configuration.items():
            kv_file.set_key(k, v)
        kv_file.write()

    def generate_services_configuration(self):
        pass

    def print_configuration(self):
        print('Current PiRogue configuration')
        for k, v in self.configuration.items():
            print(f'  {k}={v}')
        for service, definition in DEFAULTS.items():
            print(f'{service} configuration')
            for k in definition.get('mappings').keys():
                print(f'  {k}={self.configuration.get(k, None)}')

    def _get_service_configuration_handler(self, service, service_definition):
        handler_name = service_definition.get('handler')
        configuration_location = service_definition.get('location')
        preserve_value = service_definition.get('preserve_value')
        if handler_name == 'yaml_parser':
            return YamlParser(configuration_location, preserve_value=preserve_value)
        elif handler_name == 'key_value_pair':
            return KeyValuePairParser(configuration_location, preserve_value=preserve_value)
        elif handler_name == 'commander':
            return Commander(service_definition.get('mappings'), service)
        elif handler_name == 'ini_parser':
            return IniParser(configuration_location, preserve_value=preserve_value)

    def _handle_service_command(self, service_command):
        if service_command:
            subprocess.check_call(service_command, shell=True)

    def apply_configuration(self, dry_run=False):
        if not os.path.exists(PIROGUE_CONF.get('location')):
            raise Exception('No PiRogue configuration file found')
        self.load_configuration()
        for service, definition in DEFAULTS.items():
            print(f'---- {service}')
            handler = self._get_service_configuration_handler(service, definition)
            for key, specific_key in definition.get('mappings').items():
                handler.set_key(specific_key, self.configuration.get(key))
            if dry_run:
                handler.dry_run()
            else:
                if handler.dirty:
                    print(f'Applying {service} configuration')
                    handler.write()
                    self._handle_service_command(definition.get('post_configuration_command'))
                else:
                    print('Nothing to do')


def _init():
    if not os.path.exists(PIROGUE_CONF.get('location')):
        c = PiRogueConfiguration()
        c.load_default_configuration()
        c.generate_configuration_file()
        c.apply_configuration(dry_run=False)


def _apply():
    if not os.path.exists(PIROGUE_CONF.get('location')):
        print('Run the init command to generate the PiRogue configuration file')
    else:
        c = PiRogueConfiguration()
        c.load_configuration()
        c.apply_configuration(dry_run=False)


def _show():
    if not os.path.exists(PIROGUE_CONF.get('location')):
        print('Run the init command to generate the PiRogue configuration file')
    else:
        c = PiRogueConfiguration()
        c.load_configuration()
        c.print_configuration()


def _dry_run():
    if not os.path.exists(PIROGUE_CONF.get('location')):
        print('Run the init command to generate the PiRogue configuration file')
    else:
        c = PiRogueConfiguration()
        c.load_configuration()
        c.apply_configuration(dry_run=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Manage PiRogue configuration.')
    subparsers = parser.add_subparsers(dest='func')
    init = subparsers.add_parser('init', aliases=['i'])
    apply = subparsers.add_parser('apply', aliases=['a'])
    dry_run = subparsers.add_parser('dry_run', aliases=['dr'])
    show = subparsers.add_parser('show', aliases=['s'])
    args = parser.parse_args()
    if args.func == 'init':
        _init()
    elif args.func == 'apply':
        _apply()
    elif args.func == 'dry_run':
        _dry_run()
    elif args.func == 'show':
        _show()
