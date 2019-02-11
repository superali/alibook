import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user,verb,target=None):
    now = timezone.now()
    last_minute = now-datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user=user,verb=verb,created__gte=last_minute)
    if target:
        content_type = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(content_type=content_type ,object_id=target.id )
    if not similar_actions:
        action= Action(user=user,verb=verb,content_object=target)
        action.save()
        print('aaaaaaaaaaaaaaaaaaaaaaa')
        return True
    return False