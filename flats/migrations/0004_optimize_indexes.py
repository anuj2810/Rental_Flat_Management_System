from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('flats', '0003_alter_renterprofile_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_flat_owner_number ON flats_flat(owner_id, flat_number);",
            reverse_sql="DROP INDEX IF EXISTS idx_flat_owner_number;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_rent_flat_month ON flats_rentrecord(flat_id, month);",
            reverse_sql="DROP INDEX IF EXISTS idx_rent_flat_month;"
        ),
    ]