from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_backfill_invoice_payment_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(blank=True, editable=False, max_length=10),
        ),
    ]
