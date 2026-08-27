from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_backfill_admission_ward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admission',
            name='ward_legacy',
        ),
    ]
