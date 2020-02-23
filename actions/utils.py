from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone


def create_action(user, verb, target=None):
    # check the operation time
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_action = Action.objects.filter(user_id=user.id, verb=verb, created_gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_action = similar_action.filter(target_ct=target_ct, target_id=target.id)

    if not similar_action:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True

    return False