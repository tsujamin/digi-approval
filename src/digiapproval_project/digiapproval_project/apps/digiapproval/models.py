from __future__ import absolute_import
from django.db import models

class UserFile(models.Model):
    VIRUS_STATUS_CHOICES = (
        ('UNSCANNED', "Unscanned, not queued for scanning."),
        ('PENDING', "Queued for scanning, scan pending."),
        ('THREATFOUND', "Scanned, a threat was found."),
        ('CLEAN', "Scanned, no threat found."),
        ('ERROR', "An error occured during virus scanning.")
        )

    
    name = models.CharField(max_length=255)
    _file = models.FileField(upload_to="userfiles")
    virus_status = models.CharField(max_length=16,
                                    choices=VIRUS_STATUS_CHOICES, 
                                    default='UNSCANNED')

    def save(self, *args, **kwargs):
        """Save the user file, queueing up the virus scan if the file
        is UNSCANNED."""

        # first save, to get a primary key to pass to the task
        super(UserFile, self).save(*args, **kwargs)

        # then if necessary, scan and save PENDING status.
        if self.virus_status == 'UNSCANNED':
            from .tasks import virus_scan
            self.virus_status == 'PENDING'
            super(UserFile, self).save(*args, **kwargs)
            # scan *after* we set the PENDING state to avoid a race
            # condition were an actual status could be overwritten
            virus_scan.delay(self.pk)

        

    @property
    def file(self):
        """Return the file only if it is safe to do so, otherwise
        return None."""

        if not self.virus_status == 'CLEAN':
            return None

        return self._file
