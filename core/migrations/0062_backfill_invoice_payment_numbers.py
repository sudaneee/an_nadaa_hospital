import random

from django.db import migrations


def generate_number(existing_numbers):
    while True:
        candidate = f"{random.randint(0, 9999999999):010d}"
        if candidate not in existing_numbers:
            existing_numbers.add(candidate)
            return candidate


def backfill_numbers(apps, schema_editor):
    Invoice = apps.get_model('core', 'Invoice')
    Payment = apps.get_model('core', 'Payment')

    existing_numbers = set(
        Invoice.objects.exclude(invoice_number__isnull=True)
        .exclude(invoice_number='')
        .values_list('invoice_number', flat=True)
    )

    for invoice in Invoice.objects.filter(invoice_number__isnull=True) | Invoice.objects.filter(invoice_number=''):
        invoice.invoice_number = generate_number(existing_numbers)
        invoice.save(update_fields=['invoice_number'])

    for payment in Payment.objects.select_related('invoice').all():
        if not payment.payment_number and payment.invoice and payment.invoice.invoice_number:
            payment.payment_number = payment.invoice.invoice_number
            payment.save(update_fields=['payment_number'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_add_invoice_payment_number_fields'),
    ]

    operations = [
        migrations.RunPython(backfill_numbers, noop_reverse),
    ]
