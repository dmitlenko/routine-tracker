from celery import shared_task
from django.utils import translation
from django.utils.translation import gettext as _
from webpush import send_user_notification

from routine_tracker.accounts.models import User, UserProfile


@shared_task
def send_reminders():
    # Get all users
    users = User.objects.all()

    # Loop through all users
    for user in users:
        # Set the user's language
        translation.activate(UserProfile.objects.get_or_create(user=user)[0].preferred_language)

        # Send a notification to the user
        send_user_notification(
            user=user,
            payload={
                'head': _('RoutineTracker'),
                'body': _("Don't forget to complete your routines today."),
                'icon': '/static/images/icon.png',
            },
            ttl=1000,
        )

        # Reset the language
        translation.deactivate()
