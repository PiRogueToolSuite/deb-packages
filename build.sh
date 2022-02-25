#!/bin/sh

# arch="armhf arm64 amd64"

# for i in `find . -maxdepth 1 -type d -name "pirogue-*"`; do
#     cd $i;
#     for a in $arch; do
#         dpkg-buildpackage -a $a -tc --sign-key=6D49D146B9D61919B96044C43A5B3B14BD040926;
#     done
#     cd ..
# done

mkdir -p dist
find . -maxdepth 1 -type f -name "pirogue-*" -exec mv {} dist/ \;

cd dist

dpkg-scanpackages --multiversion . > Packages
gzip -k -f Packages

apt-ftparchive release . > Release
gpg --default-key "6D49D146B9D61919B96044C43A5B3B14BD040926" -abs -o - Release > Release.gpg
gpg --default-key "6D49D146B9D61919B96044C43A5B3B14BD040926" --clearsign -o - Release > InRelease

cd ..