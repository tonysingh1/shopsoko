from django.contrib import admin
from django.db.models.aggregates import Sum

from .models import Book, Customer, CustomerCheckoutHistory, BookCheckoutHistory, DateReturnedCost


# Register your models here.
admin.site.register(Book)
admin.site.register(Customer)


class BookCheckoutHistoryInline(admin.TabularInline):
    model = BookCheckoutHistory

    def get_fields(self, request, obj=None):
        if obj:
            fields = ['book', 'date_returned']
        else:
            fields = ['book']
        return fields


@admin.register(CustomerCheckoutHistory)
class CustomerCheckoutHistoryAdmin(admin.ModelAdmin):
    inlines = [BookCheckoutHistoryInline]
    fields = ['customer', 'check_out_date', 'latest_charge']
    readonly_fields = ['latest_charge']

    def latest_charge(self, obj=None):
        last = obj.datereturnedcost_set.last()
        total = BookCheckoutHistory.objects.filter(date_return_cost=last).aggregate(amount=Sum('book_charge'))
        total = total.get('amount', 0)
        return total

    def save_formset(self, request, form, formset, change):
        check_out_history = form.instance
        instances = formset.save(commit=False)  # gets instance from memory and add to it before saving it
        for obj in formset.deleted_objects:
            obj.delete()

        create_date_returned = False
        date_returned_object = None
        for instance in instances:
            if instance.date_returned:
                if not create_date_returned:
                    # create date returned cost object
                    date_returned_object = DateReturnedCost.objects.create(check_out_history=check_out_history)
                    instance.date_return_cost = date_returned_object
                    create_date_returned = True
                else:
                    instance.date_return_cost = date_returned_object
            instance.save()
        formset.save_m2m()






