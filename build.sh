#!/bin/sh

for i in `find . -maxdepth 1 -type d -name "pirogue-*"`; do
    cd $i;
        dpkg-buildpackage -b -tc -uc -us -ui
    cd ..
done

rm -rf dist/pirogue
mkdir -p dist/pirogue
dcmd --deb mv *changes dist/pirogue 

cd dist/pirogue
apt-ftparchive packages . > Packages
gzip -k -f Packages
apt-ftparchive release . > Release.tmp
mv Release.tmp Release

gpg --default-key "6D49D146B9D61919B96044C43A5B3B14BD040926" -abs -o - Release > Release.gpg

cd ../..

cd dist
gpg --armor --export "6D49D146B9D61919B96044C43A5B3B14BD040926" > Key.gpg
cd ..