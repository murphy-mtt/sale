import datetime
from django.test import TestCase
from django.utils import timezone
from analysis.models import Orders


# Create your tests here.


class OrdersModelTests(TestCase):
    def test_was_created_recently_with_future_case(self):
        time = timezone.now() + datetime.timedelta(days=31)
        future_order = Orders(create_date=time)
        self.assertIs(future_order.was_created_recently(), False)
