# Generated by Django 4.1.2 on 2022-10-17 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0007_fixturemodel_fixture_code_gwmodel_is_finished_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gwmodel',
            old_name='is_finished',
            new_name='finished',
        ),
    ]
