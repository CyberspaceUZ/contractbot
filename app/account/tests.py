from django.test import TestCase

from app.account.models import BotUser


class BotUserTestCase(TestCase):
    def setUp(self) -> None:
        BotUser.objects.create(phone_number='+998944984921', first_name='Abdullah', last_name="Saydumarov",
                               company="Cyberspace", occupation="developer", chat_id="-11100235")
        BotUser.objects.create(phone_number='+998944984121', first_name='Maxim', last_name="Petrov",
                               company="Cyberspace", occupation="developer", chat_id="-111002444")

    def test_botuser_created(self):
        botuser1 = BotUser.objects.filter(first_name='Abdullah').first()
        botuser2 = BotUser.objects.filter(first_name='Maxim').first()
        self.assertEqual(botuser1.phone_number, '+998944984921')
        self.assertEqual(botuser2.chat_id, '-111002444')

