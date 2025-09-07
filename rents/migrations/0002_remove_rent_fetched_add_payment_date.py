# Generated manually to remove rent_fetched and add payment_date

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentrecord',
            name='rent_fetched',
        ),
        migrations.AddField(
            model_name='rentrecord',
            name='payment_date',
            field=models.DateField(blank=True, help_text='Date when rent was received', null=True),
        ),
    ]
