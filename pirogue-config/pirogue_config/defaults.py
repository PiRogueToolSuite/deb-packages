DEFAULTS = {
    'hostapd': {
        'handler': 'key_value_pair',
        'location': '/home/esther/Gre/projects/pts/deb-packages/pirogue-config/pirogue_config/config-files/hostapd.conf',
        # 'location': '/etc/hostapd/hostapd.conf',
        'preserve_value': None,
        'mappings': {
            'wifi>name': 'ssid',
            'wifi>interface': 'interface',
            'wifi>driver': 'driver',
            'wifi>country_code': 'country_code',
            'wifi>passphrase': 'wpa_passphrase',
        },
        'defaults': {
            'wifi>name': 'PiRogue1',
            'wifi>driver': 'nl80211',
            'wifi>interface': 'wlan0',
            'wifi>country_code': 'FR',
            'wifi>passphrase': 'superlongkey',
        },
        'post_configuration_command': 'systemctl restart hostapd.service',
    },
    'suricata': {
        'handler': 'yaml_parser',
        'location': '/home/esther/Gre/projects/pts/deb-packages/pirogue-config/pirogue_config/config-files/suricata.yaml',
        # 'location': '/etc/suricata/suricata.yaml',
        'preserve_value': 'default',
        'mappings': {
            'wifi>interface': ('af-packet', 'interface'),
        },
        'defaults': {
            'wifi>interface': 'wlan0',
        },
        'post_configuration_command': 'systemctl restart suricata.service',
    },
    'grafana': {
        'handler': 'commander',
        'mappings': {
            'dashboard>password': lambda passwd: f'grafana-cli admin reset-admin-password {passwd}',
        },
        'defaults': {
            'dashboard>password': 'PiRogue',
        },
        'post_configuration_command': None,
    },
}
PIROGUE_CONF = {
    'handler': 'ini_parser',
    'location': '/home/esther/Gre/projects/pts/deb-packages/pirogue-config/pirogue_config/config-files/pirogue.conf',
    # 'location': '/etc/pirogue.conf',
    'preserve_value': None,
    'mappings': {},
    'defaults': {},
    'post_configuration_command': None,
}
