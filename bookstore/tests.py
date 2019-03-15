import datetime

from datetime import timedelta

from django.test import TestCase

# Create your tests here.
from .models import Customer, Book, CustomerCheckoutHistory, BookCheckoutHistory


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

        # book 1 returned after 3 days
        days = 3
        book_checkout_history = BookCheckoutHistory.objects.get(id=1)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 3.00)
        final_charge = book_charge
        self.assertEqual(final_charge, 3)

        # book 2 returned after 3 days
        days = 1
        book_checkout_history = BookCheckoutHistory.objects.get(id=2)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 1.00)
        final_charge = book_charge
        self.assertEqual(final_charge, 1)

        days = 7
        book_checkout_history = BookCheckoutHistory.objects.get(id=2)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_charge = book_checkout_history.book_charge
        self.assertEqual(book_charge, 7.00)
        final_charge = book_charge
        self.assertEqual(final_charge, 7)


    def test_print_charges_on_returning(self):  # used for getting charge if book or books were returned on same date
        # all three books returned after 6 days of borrowing
        days = 6
        # book 1
        book_checkout_history = BookCheckoutHistory.objects.get(id=1)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_1_charge = book_checkout_history.book_charge
        self.assertEqual(book_1_charge, 6.00)

        # book 2
        book_checkout_history = BookCheckoutHistory.objects.get(id=2)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_2_charge = book_checkout_history.book_charge
        self.assertEqual(book_2_charge, 6.00)

        # book 3
        book_checkout_history = BookCheckoutHistory.objects.get(id=3)
        checkout_date = book_checkout_history.check_out_history.check_out_date
        book_checkout_history.date_returned = checkout_date + timedelta(days=days)
        book_checkout_history.save()
        book_3_charge = book_checkout_history.book_charge
        self.assertEqual(book_3_charge, 6.00)

        final_charge = book_1_charge + book_2_charge + book_3_charge
        self.assertEqual(final_charge, 18)
