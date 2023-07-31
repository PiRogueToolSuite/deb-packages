#!/bin/sh
set -e

# Build packages
for source in `find . -maxdepth 1 -type d -name "pirogue-*"`; do
    cd $source;
    dpkg-buildpackage -b -tc -uc -us -ui
    cd ..
done

# Collect packages
rm -rf dist/pirogue
mkdir -p dist/pirogue
dcmd --deb mv *changes dist/pirogue 

# Copy them into the ppa
cp dist/pirogue/*.deb ../ppa/pirogue/
cd ../ppa/pirogue

# Rebuild the ppa
rm -f Packages* Release*
apt-ftparchive packages . > Packages
gzip -k -f Packages
apt-ftparchive release . > Release.tmp
mv Release.tmp Release
gpg --local-user "6D49D146B9D61919B96044C43A5B3B14BD040926" -abs -o - Release > Release.gpg

