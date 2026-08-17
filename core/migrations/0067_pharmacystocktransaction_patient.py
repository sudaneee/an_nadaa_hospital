from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacystocktransaction',
            name='patient',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='stock_transactions',
                to='core.patient',
            ),
        ),
    ]
