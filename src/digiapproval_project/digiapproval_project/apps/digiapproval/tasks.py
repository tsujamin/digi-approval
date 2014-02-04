from __future__ import absolute_import
import pyclamd
from celery import shared_task
from .models import UserFile


@shared_task
def virus_scan(userfile_pk):
    # todo: move this string to config.
    conn = pyclamd.ClamdUnixSocket('/var/run/clamav/clamd.ctl')

    userfile = UserFile.objects.filter(pk=userfile_pk)[0]
    stream = userfile._file.read()
    result = conn.scan_stream(stream)

    if result is not None:
        userfile.virus_status = "THREATFOUND"
    else:
        userfile.virus_status = "CLEAN"

    userfile.save()
