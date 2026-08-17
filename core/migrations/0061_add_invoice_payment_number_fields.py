from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_pharmacystock_created_by_pharmacystock_updated_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True),
        ),
    ]
