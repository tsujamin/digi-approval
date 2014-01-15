from django.contrib import admin
from digiapproval_project.apps.digiapproval.models import *
# Register your models here.
admin.site.register(UserFile)
admin.site.register(Workflow)
admin.site.register(WorkflowSpec)
admin.site.register(CustomerAccount)
