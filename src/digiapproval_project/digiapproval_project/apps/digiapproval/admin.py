"""Contains model registration for django.admin page"""

from django.contrib import admin
from digiapproval_project.apps.digiapproval import models
# Register your models here.
admin.site.register(models.UserFile)
admin.site.register(models.Workflow)
admin.site.register(models.WorkflowSpec)
admin.site.register(models.CustomerAccount)
admin.site.register(models.SemanticFieldType)
