# Generated by Django 3.1.7 on 2021-04-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_application_transfer_risk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('CREATED', 'отправлено юристу'), ('IN_PROCESS', 'на рассмотрении'), ('SUCCESS', 'согласованно'), ('CANCELED', 'отказ')], default='CREATED', max_length=50),
        ),
    ]
