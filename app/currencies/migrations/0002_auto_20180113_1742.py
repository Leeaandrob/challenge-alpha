# Generated by Django 2.0.1 on 2018-01-13 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='quotation',
            new_name='rate',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='quotation_date',
            new_name='updated_at',
        ),
    ]
