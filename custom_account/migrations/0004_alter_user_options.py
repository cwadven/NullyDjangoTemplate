# Generated by Django 3.2.12 on 2023-05-29 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0003_create_admin_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True, 'verbose_name': '일반 사용자', 'verbose_name_plural': '일반 사용자'},
        ),
    ]
