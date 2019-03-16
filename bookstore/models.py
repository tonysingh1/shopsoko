from django.db import models

# Create your models here.
from django.db import models


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


class Book(DescriptionCommonInfo):
    pass


class CustomerCheckoutHistory(CommonInfo):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_out_date = models.DateField()

    class Meta:
        verbose_name_plural = "check out history"

    def __str__(self):
        return '%s, %s' % (self.id, self.customer)


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

    def get_book_charge(self):
        rate_per_day = self.book_rate
        days = self.get_days()
        book_charge = days * rate_per_day
        return book_charge

    def save(self,  *args, **kwargs):
        if self.id:  # calculate charge and day when updating fields
            self.book_charge = self.get_book_charge()
            self.days_rented = self.get_days()
        super().save(*args, **kwargs)
