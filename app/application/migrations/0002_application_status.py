# Generated by Django 3.1.7 on 2021-03-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Application Created'), ('IN_PROCESS', 'Application In Process'), ('SUCCESS', 'Application Succeed'), ('CANCELED', 'Application Canceled')], default='CREATED', max_length=50),
        ),
    ]