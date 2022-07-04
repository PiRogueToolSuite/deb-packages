import os.path


class KeyValuePairParser:
    def __init__(self, file_path, delimiter='=', comment_prefix='#', preserve_value=None):
        self.file_path = file_path
        self.delimiter = delimiter
        self.comment_prefix = comment_prefix
        self.preserve_value = preserve_value
        self.data = {}
        self.dirty = False
        self.changes = []
        if os.path.exists(file_path):
            self.read()

    def read(self):
        with open(self.file_path, mode='r', encoding='utf-8') as config_file:
            for line in config_file.read().splitlines():
                if line.strip() and not line.strip().startswith(';'):
                    delimiter_pos = line.find(self.delimiter)
                    key = line[0:delimiter_pos].strip()
                    value = line[delimiter_pos + 1:].strip()
                    if self.comment_prefix in value:
                        comment_pos = value.find(self.comment_prefix)
                        value = line[delimiter_pos + 1:comment_pos].strip()
                    self.data[key] = value

    def get_data(self):
        if not self.data:
            self.read()
        return self.data

    def set_key(self, key, value):
        if value:
            old_value = self.data.get(key, None)
            if old_value != self.preserve_value or self.preserve_value is None:
                if old_value != value:
                    self.dirty = True
                    self.data[key] = value
                    self.changes.append((old_value, value))

    def dry_run(self):
        print(f'Modifications to be applied for {self.file_path}:')
        if self.dirty:
            for old, new in self.changes:
                print(f'  {old} -> {new}')
        else:
            print(' no modification to apply')

    def write(self, overrides=None):
        if self.dirty:
            with open(self.file_path, mode='w') as config_file:
                for k, v in self.data.items():
                    config_file.write(f'{k}{self.delimiter}{v}\n')


if __name__ == '__main__':
    fp = '../config-files/hostapd.conf'
    kv = KeyValuePairParser(fp)
    kv.read()
    print(kv.get_data())
    kv.set_key('ssid', 'PiRogue34')
    print(kv.get_data())
    kv.write()
