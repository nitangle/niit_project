from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from portal.models import UserProfile


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        email_confirmed = UserProfile.objects.get(username=user.username).email_confirmed
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()
