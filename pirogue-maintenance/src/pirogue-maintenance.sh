#!/bin/sh

set -e

/usr/bin/suricata-update --no-check-certificate --no-test
/usr/bin/suricatasc -c reload-rules
