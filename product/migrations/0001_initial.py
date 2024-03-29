# Generated by Django 3.2.12 on 2023-05-29 17:16

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='디테일 설정')),
            ],
            options={
                'verbose_name': '디테일 종류',
                'verbose_name_plural': '디테일 종류',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='시작 시간')),
                ('end_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='종료 시간')),
                ('is_active', models.BooleanField(db_index=True, default=False, verbose_name='활성화 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='삭제 여부')),
                ('title', models.CharField(db_index=True, max_length=120, verbose_name='상품명')),
                ('description', models.TextField(blank=True, null=True, verbose_name='상품 설명')),
                ('real_price', models.IntegerField(db_index=True, verbose_name='정가')),
                ('payment_price', models.IntegerField(db_index=True, verbose_name='판매가')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=1, help_text='숫자가 작을수록 앞에 있음', verbose_name='순서')),
                ('bought_count', models.BigIntegerField(db_index=True, default=0, verbose_name='구매 수')),
                ('review_count', models.BigIntegerField(db_index=True, default=0, verbose_name='리뷰 수')),
                ('review_rate', models.FloatField(db_index=True, default=0, verbose_name='리뷰 평점')),
            ],
            options={
                'verbose_name': '상품 틀',
                'verbose_name_plural': '상품 틀',
            },
            managers=[
                ('datetime_active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='시작 시간')),
                ('end_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='종료 시간')),
                ('is_active', models.BooleanField(db_index=True, default=False, verbose_name='활성화 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='삭제 여부')),
                ('good_number', models.CharField(db_index=True, max_length=120, unique=True, verbose_name='고유 상품 번호')),
                ('title', models.CharField(db_index=True, max_length=120, verbose_name='상품명')),
                ('description', models.TextField(blank=True, null=True, verbose_name='상품 설명')),
                ('additional_payment_price', models.IntegerField(db_index=True, default=0, verbose_name='추가 판매가')),
                ('bought_count', models.BigIntegerField(db_index=True, default=0, verbose_name='구매 수')),
                ('left_quantity', models.IntegerField(db_index=True, default=0, verbose_name='상품 재고')),
                ('is_sold_out', models.BooleanField(db_index=True, default=False, verbose_name='품절 여부')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='product.product', verbose_name='상품')),
            ],
            options={
                'verbose_name': '상품 아이템',
                'verbose_name_plural': '상품 아이템',
            },
            managers=[
                ('datetime_active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='상품 타입')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=1, help_text='숫자가 작을수록 앞에 있음', verbose_name='순서')),
            ],
            options={
                'verbose_name': '상품 타입',
                'verbose_name_plural': '상품 타입',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('image', models.TextField(blank=True, null=True, verbose_name='이미지')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=1, help_text='숫자가 작을수록 앞에 있음', verbose_name='순서')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='상품')),
            ],
            options={
                'verbose_name': '상품 이미지들',
                'verbose_name_plural': '상품 이미지들',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ManyToManyField(blank=True, null=True, to='product.ProductType', verbose_name='상품 타입'),
        ),
        migrations.CreateModel(
            name='ProductItemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=1, help_text='숫자가 작을수록 앞에 있음', verbose_name='순서')),
                ('information', models.CharField(db_index=True, max_length=120, verbose_name='정보')),
                ('info_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.infotype', verbose_name='상품 아이템 디테일 설정')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_item_infos', to='product.productitem', verbose_name='상품 아이템')),
            ],
            options={
                'verbose_name': '상품 아이템 디테일',
                'verbose_name_plural': '상품 아이템 디테일',
                'unique_together': {('product_item', 'info_type')},
            },
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=1, help_text='숫자가 작을수록 앞에 있음', verbose_name='순서')),
                ('info_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.infotype', verbose_name='디테일 설정')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_infos', to='product.product', verbose_name='상품')),
            ],
            options={
                'verbose_name': '상품 필수 디테일',
                'verbose_name_plural': '상품 필수 디테일',
                'unique_together': {('product', 'info_type')},
            },
        ),
    ]
