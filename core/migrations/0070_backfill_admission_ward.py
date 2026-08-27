from django.db import migrations

# Known historical spellings/casing seen in production -> canonical Ward name.
# ('SCUB' is kept as-is rather than "corrected" to e.g. 'SCBU', so existing
# admission records keep displaying exactly what they always have.)
KNOWN_WARDS = {
    'maternity': 'Maternity',
    'pediatrics': 'Pediatrics',
    'scub': 'SCUB',
}

# The old "create admission" dropdown offered a "Labour" option, but a
# template bug meant selecting it always saved "Pediatrics" instead, so no
# admission ever actually has this value. Create it anyway so it's available
# going forward now that wards are database-managed.
EXTRA_WARDS = ['Labour']


def backfill_wards(apps, schema_editor):
    Ward = apps.get_model('core', 'Ward')
    Admission = apps.get_model('core', 'Admission')

    cache = {}

    def get_ward(raw_name):
        key = raw_name.strip().lower()
        if key in cache:
            return cache[key]
        canonical = KNOWN_WARDS.get(key, raw_name.strip())
        ward, _ = Ward.objects.get_or_create(name=canonical)
        cache[key] = ward
        return ward

    for admission in Admission.objects.exclude(ward_legacy__isnull=True).exclude(ward_legacy=''):
        admission.ward = get_ward(admission.ward_legacy)
        admission.save(update_fields=['ward'])

    for name in EXTRA_WARDS:
        Ward.objects.get_or_create(name=name)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_create_ward_and_admission_ward_fk'),
    ]

    operations = [
        migrations.RunPython(backfill_wards, noop_reverse),
    ]
