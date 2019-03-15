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


class BookCheckoutHistory(CommonInfo):
    check_out_history = models.ForeignKey(CustomerCheckoutHistory, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_returned = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "book checkout history"

    def __str__(self):
        return '%s, %s' % (self.check_out_history.id, self.book)

