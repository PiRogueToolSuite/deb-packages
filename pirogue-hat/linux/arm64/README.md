# DTB overlay for pirogue-hat

We need to combine an I2C/RTC overlay and a GPIO fan one.

The first one is easy, the second one references some labels that are
not found in the mainline kernel. Those `target` references are replaced
with matching `target-path` ones, making the missing labels a non-issue.

To build the DTBO:

    sudo apt-get install device-tree-compiler
    dtc -Idts -Odtb i2c-rtc-overlay.dts > pirogue-hat.dtbo
