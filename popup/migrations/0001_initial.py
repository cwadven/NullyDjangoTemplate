# Generated by Django 3.2.12 on 2023-05-29 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePopupModal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.TextField(blank=True, null=True, verbose_name='이미지')),
                ('description', models.TextField(blank=True, null=True, verbose_name='관리자 보기 위한 설명')),
                ('on_clicK_link', models.TextField(null=True, verbose_name='이미지 클릭 시 링크')),
                ('height', models.PositiveIntegerField(verbose_name='모달 높이')),
                ('width', models.PositiveIntegerField(verbose_name='모달 너비')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
