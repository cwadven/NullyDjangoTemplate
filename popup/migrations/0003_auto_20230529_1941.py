# Generated by Django 3.2.12 on 2023-05-29 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popup', '0002_rename_on_click_link_homepopupmodal_on_click_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepopupmodal',
            options={'verbose_name': '홈 팝업 모달', 'verbose_name_plural': '홈 팝업 모달'},
        ),
        migrations.AlterField(
            model_name='homepopupmodal',
            name='end_time',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='종료 시간'),
        ),
        migrations.AlterField(
            model_name='homepopupmodal',
            name='is_active',
            field=models.BooleanField(db_index=True, default=False, verbose_name='활성화 여부'),
        ),
        migrations.AlterField(
            model_name='homepopupmodal',
            name='start_time',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='시작 시간'),
        ),
    ]