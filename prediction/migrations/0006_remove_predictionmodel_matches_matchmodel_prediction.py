# Generated by Django 4.1.2 on 2022-10-16 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0005_remove_fixturemodel_date_remove_fixturemodel_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predictionmodel',
            name='matches',
        ),
        migrations.AddField(
            model_name='matchmodel',
            name='prediction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='prediction.predictionmodel'),
        ),
    ]
