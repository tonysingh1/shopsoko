# Generated by Django 2.1.7 on 2019-03-15 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcheckouthistory',
            name='date_returned',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
