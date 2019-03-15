from django.contrib import admin
from .models import Book, Customer, CustomerCheckoutHistory, BookCheckoutHistory


# Register your models here.
admin.site.register(Book)
admin.site.register(Customer)


class BookCheckoutHistoryInline(admin.TabularInline):
    model = BookCheckoutHistory
    fields = ['book']


@admin.register(CustomerCheckoutHistory)
class CustomerCheckoutHistoryAdmin(admin.ModelAdmin):
    inlines = [BookCheckoutHistoryInline]
