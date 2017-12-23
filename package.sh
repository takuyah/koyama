cd $VIRTUAL_ENV
rm koyama.zip -f
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 $VIRTUAL_ENV/koyama.zip *
cd $VIRTUAL_ENV
zip -g koyama.zip koyama.py