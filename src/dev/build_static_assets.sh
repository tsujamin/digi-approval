#!/bin/bash

cd `dirname $0`  # src/dev
echo "Making docs..."
cd ../../docs/website
python makedocs.py
echo "done"
echo "Load the docs with syncdb."
echo ""

echo "Lessifying every less file in apps/digiapproval/static/less"
cd ../../src/digiapproval_project/digiapproval_project/apps/digiapproval/static/less
for lessfile in $(find . -name "*.less"); do
    lessname=`basename $lessfile .less`
    lessdir=`dirname $lessfile`
    echo "Converting $lessdir/$lessname.less"
    lessc $lessdir/$lessname.less > ../css/$lessdir/$lessname.css
done
echo "done"
echo "Don't forget to collectstatic if deploying with uWSGI."
echo ""
