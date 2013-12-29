from SpiffWorkflow.storage import JSONSerializer, DictionarySerializer
from SpiffWorkflow import Workflow
from SpiffWorkflow.specs import WorkflowSpec
from django.db import models
try:
    from django.utils.six import with_metaclass
except ImportError:
    from six import with_metaclass
    
_jserializer = JSONSerializer()
_dserializer = DictionarySerializer()

    
class WorkflowField(with_metaclass(models.SubfieldBase, models.Field)):
    
    description = "Workflow object"
    _jserializer = JSONSerializer()
    _dserializer = DictionarySerializer()
    
    
    def __init__(self, *args, **kwargs):
        super(WorkflowField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(WorkflowField, self).deconstruct()
        return name, path, args, kwargs
        
    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90300:
            return 'json'
        else:
            return super(WorkflowField, self).db_type(connection)
            
    #Deserialise JSON and return appropriate SpiffWorkflow type        
    def to_python(self, value):
        if isinstance(value, Workflow):
            return value
        elif isinstance(value, dict):
            return _dserializer.deserialize_workflow(value)
        else:
            return _jserializer.deserialize_workflow(value)
            
    def get_prep_value(self, value):
            return _jserializer.serialize_workflow(value)

class WorkflowSpecField(with_metaclass(models.SubfieldBase, models.Field)):
    
    description = "WorkflowSpec object"
    
    def __init__(self, *args, **kwargs):
        super(WorkflowSpecField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(WorkflowSpecField, self).deconstruct()
        return name, path, args, kwargs
        
    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90300:
            return 'json'
        else:
            return super(WorkflowSpecField, self).db_type(connection)
            
    #Deserialise JSON and return appropriate SpiffWorkflow type        
    def to_python(self, value):
        if isinstance(value, WorkflowSpec):
            return value
        elif isinstance(value, dict):
            return _dserializer.deserialize_workflow_spec(value)
        else:
            return _jserializer.deserialize_workflow_spec(value)
            
    def get_prep_value(self, value):
            return _jserializer.serialize_workflow_spec(value)
            

        
#to make south happy with our custom fields
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^digiapproval_project\.apps\.digiapproval\.fields\.(WorkflowField|WorkflowSpecField)"])       