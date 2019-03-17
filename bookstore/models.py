from django.db import models

# Create your models here.
from django.db import models
from django.db.models.aggregates import Sum


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DescriptionCommonInfo(CommonInfo):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s, %s' % (self.code, self.name)

    class Meta:
        abstract = True


class Customer(DescriptionCommonInfo):
    pass


class BookCategory(DescriptionCommonInfo):
    charge_per_day = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    starting_charge = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    starting_charge_day_limit = models.PositiveIntegerField(null=True, blank=True)
    minimum_charge = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    minimum_charge_day_limit = models.PositiveIntegerField(null=True, blank=True)

    def _check_starting_charge(self, days):
        days = days
        if self.starting_charge_day_limit and self.starting_charge:
            extra_days = days - self.starting_charge_day_limit
            initial_charge = self.starting_charge_day_limit * self.starting_charge
            extra_day_charges = extra_days * self.charge_per_day
            book_charge = initial_charge + extra_day_charges
        else:
            book_charge = days * self.charge_per_day
        return book_charge

    def _check_minimum_charge(self, book_charge, days):
        if self.minimum_charge and self.minimum_charge_day_limit:
            if days < self.minimum_charge_day_limit:
                book_charge = self.minimum_charge
        return book_charge

    def get_book_charge(self, days):
        book_charge = self._check_starting_charge(days)
        book_charge = self._check_minimum_charge(book_charge=book_charge, days=days)
        return book_charge


class Book(DescriptionCommonInfo):
    book_category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s, %s, %s' % (self.code, self.name, self.book_category.name)


class CustomerCheckoutHistory(CommonInfo):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_out_date = models.DateField()

    class Meta:
        verbose_name_plural = "check out history"

    def __str__(self):
        return '%s, %s' % (self.id, self.customer)

    def get_latest_charge(self):
        last = self.datereturnedcost_set.last()
        total = BookCheckoutHistory.objects.filter(date_return_cost=last).aggregate(amount=Sum('book_charge'))
        total = total.get('amount', 0)
        return total


class DateReturnedCost(CommonInfo):  # Get the exact charge when books are returned
    check_out_history = models.ForeignKey(CustomerCheckoutHistory, on_delete=models.CASCADE)


class BookCheckoutHistory(CommonInfo):
    check_out_history = models.ForeignKey(CustomerCheckoutHistory, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_returned = models.DateField(null=True, blank=True)
    book_rate = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    days_rented = models.IntegerField(null=True, blank=True)
    book_charge = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_return_cost = models.ForeignKey(DateReturnedCost, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "book checkout history"

    def __str__(self):
        return '%s, %s' % (self.check_out_history.id, self.book)

    def get_days(self):
        days = 0
        check_out_date = self.check_out_history.check_out_date
        date_returned = self.date_returned
        if date_returned:
            delta = date_returned - check_out_date
            days = delta.days
        return days

    def get_rate_per_day(self):
        rate_per_day = 0
        days = self.get_days()
        book_charge = self.book.book_category.get_book_charge(days)
        if days:
            rate_per_day = book_charge / days
        return rate_per_day

    def get_book_charge(self):
        days = self.get_days()
        book_charge = self.book.book_category.get_book_charge(days)
        return book_charge

    def save(self,  *args, **kwargs):
        if self.id:  # calculate charge and day when updating fields
            self.book_rate = self.get_rate_per_day()
            self.book_charge = self.get_book_charge()
            self.days_rented = self.get_days()
        super().save(*args, **kwargs)
