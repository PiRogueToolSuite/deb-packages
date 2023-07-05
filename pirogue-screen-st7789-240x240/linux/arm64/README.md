# DTB overlay for pirogue-screen

We need to enable SPI, but that's a little tricky since `spidev` isn't
supposed to appear in DTBs (due to fffc84fd87d9 in mainline), that's why
we're also using a udev rule.

 - <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fffc84fd87d963a2ea77a125b8a6f5a3c9f3192d>

To build the DTBO:

    sudo apt-get install device-tree-compiler
    dtc -Idts -Odtb pirogue-screen-overlay.dts > pirogue-screen.dtbo
