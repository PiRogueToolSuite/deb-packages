# Custom DTBs

## What and why

The PiRogue Tool Suite project supports Raspberry Pi 3 and 4. The PiRogue hat
requires enabling some hardware features, implemented via DTBOs. To apply
successfully, some of them require finding references in the base DTB files,
that's why we're building those DTBs with the `-@` flag, cherry-picking mainline
commits 3cdba279c5e9 and e925743edc0d on top of the Debian 12 kernel (6.1.27-1
initially).

 - <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3cdba279c5e9209fc1ffd6e56db1e79421555984>
 - <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e925743edc0d86fb846d952190d005bac8a6e373>

Hopefully those commits will make it into the official Debian package for some
12.x point release, and we'll be able to drop our custom DTBs after a while.


## How

Additionally, we ship a kernel hook running after the raspi-firmware one
(`z50-raspi-firmware`), making sure we override the DTBs it deploys from the
official `linux-image` package.

This hook is deployed on all systems, and uses flag files set by the postinst to
determine whether to act, making its future removal easy (no longer shipping it
should be sufficient).

It is also called from postinst during configuration to ensure custom DTBs are
deployed during installation.
