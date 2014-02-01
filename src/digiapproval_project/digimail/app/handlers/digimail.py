from lamson.routing import route, route_like, stateless
from digiapproval_project.apps.digiapproval.models import Message, Workflow
from django.contrib.auth.models import User


@route("workflow-(uuid)@(host)", uuid="[a-fA-F0-9]+")
@stateless
def WORKFLOW_MESSAGE(message, uuid=None, host=None):
    # try to find the relevant workflow and user
    try:
        workflow = Workflow.objects.get(uuid=uuid)
        # this is brutally brittle: your registered email address or a silent
        # drop
        sender = User.objects.get(email=message.From)
    except:
        return ERROR

    # save it
    m = Message()
    m._sent = True
    m.message = message.body()
    m.workflow = workflow
    m.sender = sender
    m.save()


@route_like(WORKFLOW_MESSAGE)
def ERROR(message, uuid=None, host=None):
    pass
