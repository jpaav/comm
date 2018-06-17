from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# Makes a hash value for the unique Registration Token
# Extends a PasswordResetTokenGenerator and makes a hash value to use as a url
class JoinOrgTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, org, timestamp):
        return (six.text_type(org.pk) + six.text_type(timestamp)) + six.text_type(org.members.count())

join_org_token = JoinOrgTokenGenerator()
