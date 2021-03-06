from django.conf import settings
from django.core.mail import send_mass_mail

from api_backend.models import ParticipantMatch


def sending_mail(user, participant, participant_email, user_email):
    try:
        participant_matches = ParticipantMatch.objects.get(user=participant.user)
    except:
        participant_matches = None
    if participant_matches:
        if user.participant in participant_matches.participant.all():
            subject = "Любовное совпадение"
            text_to_user = f"У Вас возникла обоюдная симпатия с {participant}. Вот его почта - {participant_email} "
            text_to_participant = f"У Вас возникла обоюдная симпатия с {user}. Вот его почта - {user_email} "
            message_to_user = (subject, text_to_user, settings.EMAIL_HOST_USER, [user_email])
            message_to_participant = (subject, text_to_participant, settings.EMAIL_HOST_USER, [participant_email])
            send_mass_mail(
                (message_to_user, message_to_participant), fail_silently=False
            )
