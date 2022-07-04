import os.path
from configparser import ConfigParser


class IniParser:
    def __init__(self, file_path, delimiter='=', comment_prefix='#', preserve_value=None):
        self.file_path = file_path
        self.delimiter = delimiter
        self.comment_prefix = comment_prefix
        self.preserve_value = preserve_value
        self.data = {}
        self.changes = []
        if os.path.exists(file_path):
            self.read()

    def read(self):
        with open(self.file_path, mode='r', encoding='utf-8') as config_file:
            current_section = None
            for line in config_file.read().splitlines():
                if not line.strip() or line.strip().startswith(';') or line.strip().startswith(self.comment_prefix):
                    continue
                if line.strip().startswith('['):
                    current_section = line.strip()[1:-1]
                    self.data[current_section] = {}
                    continue

                delimiter_pos = line.find(self.delimiter)
                key = line[0:delimiter_pos].strip()
                value = line[delimiter_pos + 1:].strip()
                if current_section:
                    self.data[current_section][key] = value
                else:
                    self.data[key] = value

    def get_data(self):
        if not self.data.keys():
            self.read()
        return self.data

    def set_key(self, attributes, value):
        section, key = attributes
        if value:
            if section:
                old_value = self.data.get(section).get(key, None)
                if old_value != self.preserve_value or self.preserve_value is None:
                    self.data[section][key] = value
                    self.changes.append((old_value, value))
            else:
                old_value = self.data.get(key, None)
                if old_value != self.preserve_value or self.preserve_value is None:
                    self.data[key] = value
                    self.changes.append((old_value, value))

    def dry_run(self):
        print(f'Modifications to be applied in {self.file_path}:')
        for old, new in self.changes:
            print(f'  {old} -> {new}')

    def write(self, overrides=None):
        with open(self.file_path, mode='w') as config_file:
            for k, v in self.data.items():
                if not isinstance(v, dict):
                    config_file.write(f'{k} {self.delimiter} {v}\n')
            for k, v in self.data.items():
                if isinstance(v, dict):
                    config_file.write(f'\n[{k}]\n')
                    for ke, ve in v.items():
                        config_file.write(f'{ke} {self.delimiter} {ve}\n')


if __name__ == '__main__':
    fp = '../config-files/grafana.ini'
    kv = IniParser(fp)
    kv.read()
    print(kv.get_data())
    kv.set_key(('security', 'admin_password'), 'PiRogue34')
    kv.dry_run()
    kv.write()
