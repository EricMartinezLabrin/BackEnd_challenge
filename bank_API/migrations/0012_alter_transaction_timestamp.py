# Generated by Django 4.1.2 on 2023-03-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_API', '0011_alter_account_account_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
