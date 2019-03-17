import datetime

from datetime import timedelta

from django.test import TestCase

# Create your tests here.
from .models import Customer, Book, CustomerCheckoutHistory, BookCheckoutHistory, DateReturnedCost


class BookstoreTestCase(TestCase):

    def setUp(self):
        Customer.objects.create(code=1, name='Customer 1')
        customer = Customer.objects.get(id=1)

        Book.objects.create(code='A', name='Book A')
        Book.objects.create(code='B', name='Book B')
        Book.objects.create(code='C', name='Book C')

        book_a = Book.objects.get(id=1)
        book_b = Book.objects.get(id=2)
        book_c = Book.objects.get(id=3)

        CustomerCheckoutHistory.objects.create(customer=customer, check_out_date=datetime.date.today())
        customer_checkout_history = CustomerCheckoutHistory.objects.get(id=1)

        # Customer 1 takes three books
        BookCheckoutHistory.objects.create(check_out_history=customer_checkout_history, book=book_a)
        BookCheckoutHistory.objects.create(check_out_history=customer_checkout_history, book=book_b)
        BookCheckoutHistory.objects.create(check_out_history=customer_checkout_history, book=book_c)

    def test_individual_book_charge(self):  # used for checking if books were returned on different dates

        customer_checkout_history = CustomerCheckoutHistory.objects.get(id=1)

        # two books returned after 3 days
        date_returned_object = DateReturnedCost.objects.create(check_out_history=customer_checkout_history)
        days = 3
        book_checkout_history = BookCheckoutHistory.objects.get(id=1)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.date_return_cost = date_returned_object
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 3.00)

        book_checkout_history = BookCheckoutHistory.objects.get(id=2)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.date_return_cost = date_returned_object
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 3.00)

        latest_charge = customer_checkout_history.get_latest_charge()
        self.assertEqual(latest_charge, 6.00)

        # one book returned after 7 days
        date_returned_object = DateReturnedCost.objects.create(check_out_history=customer_checkout_history)
        days = 7
        book_checkout_history = BookCheckoutHistory.objects.get(id=3)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.date_return_cost = date_returned_object
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 7)


