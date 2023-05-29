from django.db import models

from config.model_interfaces.common_model_interfaces import DateTimeActiveMixin, CreateModifyTimeMixin, SoftDeleteMixin


class ProductType(models.Model):
    name = models.CharField(verbose_name='상품 타입', max_length=120, db_index=True)
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )

    def __str__(self):
        return f'{self.name}'


class Product(SoftDeleteMixin, DateTimeActiveMixin, CreateModifyTimeMixin):
    good_number = models.CharField(
        verbose_name='고유 상품 번호',
        max_length=120,
        db_index=True,
        null=True,
        blank=True,
        unique=True,
    )
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )
    product_type = models.ForeignKey(
        ProductType,
        verbose_name='상품 타입',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(verbose_name='상품명', max_length=120, db_index=True)
    description = models.TextField(verbose_name='상품 설명', null=True, blank=True)
    real_price = models.IntegerField(verbose_name='정가', db_index=True)
    payment_price = models.IntegerField(verbose_name='판매가', db_index=True)
    left_quantity = models.IntegerField(verbose_name='상품 재고', default=0, db_index=True)
    is_sold_out = models.BooleanField(verbose_name='품절 여부', default=False, db_index=True)
    bought_count = models.BigIntegerField(verbose_name='구매 수', default=0, db_index=True)
    review_count = models.BigIntegerField(verbose_name='리뷰 수', default=0, db_index=True)
    review_rate = models.FloatField(verbose_name='리뷰 평점', default=0, db_index=True)
    final_product_info_type = models.ForeignKey(
        'product.ProductInfoType',
        verbose_name='마지막 선택하는 경우 구매 활성화 되는 상품 설정',
        on_delete=models.SET_NULL,
        help_text='마지막 선택하는 경우 구매 활성화 되는 상품 설정',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.title} - {self.description}'


class ProductImage(CreateModifyTimeMixin):
    product = models.ForeignKey(
        Product,
        verbose_name='상품',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.TextField(verbose_name='이미지', blank=True, null=True)
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )

    def __str__(self):
        return f'{self.product.title} - {self.sequence}'


class ProductInfoType(CreateModifyTimeMixin):
    name = models.CharField(verbose_name='상품 디테일 설정', max_length=120, db_index=True)
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )

    def __str__(self):
        return f'{self.name}'


class ProductInfo(CreateModifyTimeMixin):
    product = models.ForeignKey(
        Product,
        verbose_name='상품',
        related_name='additional_products',
        on_delete=models.CASCADE,
    )
    product_info_type = models.ForeignKey(
        ProductInfoType,
        verbose_name='상품 디테일 설정',
        on_delete=models.CASCADE
    )
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )
    title = models.CharField(verbose_name='상품명', max_length=120, db_index=True)
    description = models.TextField(verbose_name='상품 설명', null=True, blank=True)
    payment_price = models.IntegerField(verbose_name='판매가', db_index=True)
    left_quantity = models.IntegerField(verbose_name='상품 재고', default=0, db_index=True)
    is_sold_out = models.BooleanField(verbose_name='품절 여부', default=False, db_index=True)

    def __str__(self):
        return f'{self.title} - {self.description}'
