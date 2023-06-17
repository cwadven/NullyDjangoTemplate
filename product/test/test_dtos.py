from django.test import TestCase

from product.dtos import ProductDetailDTO, ProductItemDTO
from product.models import Product, ProductInfo, InfoType, ProductType, ProductImage, ProductItem


class TestProductDetailDTO(TestCase):
    def setUp(self):
        self.product_type1 = ProductType.objects.create(
            name='의류1',
            sequence=1,
        )
        self.product_type2 = ProductType.objects.create(
            name='의류2',
            sequence=2,
        )
        self.info_type1 = InfoType.objects.create(
            name='사이즈',
        )
        self.info_type2 = InfoType.objects.create(
            name='색상',
        )
        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
        )
        self.product.product_type.add(self.product_type1)
        self.product.product_type.add(self.product_type2)
        self.product_image1 = ProductImage.objects.create(
            product=self.product,
            image='https://image1.com',
            sequence=1,
        )
        self.product_image2 = ProductImage.objects.create(
            product=self.product,
            image='https://image2.com',
            sequence=2,
        )
        self.product_info1 = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type1,
            sequence=1,
        )
        self.product_info2 = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type2,
            sequence=2,
        )

    def test_product_detail_dto(self):
        # Given:
        # When:
        product_detail = ProductDetailDTO.of(self.product).to_dict()

        # Then:
        self.assertEqual(product_detail['id'], self.product.id)
        self.assertEqual(product_detail['title'], self.product.title)
        self.assertEqual(product_detail['description'], self.product.description)
        self.assertEqual(product_detail['real_price'], self.product.real_price)
        self.assertEqual(product_detail['payment_price'], self.product.payment_price)
        self.assertEqual(product_detail['bought_count'], self.product.bought_count)
        self.assertEqual(product_detail['review_count'], self.product.review_count)
        self.assertEqual(product_detail['review_rate'], self.product.review_rate)
        # And: product_type 정렬에 맞게 설정
        self.assertEqual(product_detail['product_type_names'][0], self.product_type1.name)
        self.assertEqual(product_detail['product_type_names'][1], self.product_type2.name)
        # And: product_image 정렬에 맞게 설정
        self.assertEqual(product_detail['product_images'][0], self.product_image1.image)
        self.assertEqual(product_detail['product_images'][1], self.product_image2.image)
        # And: product_info 정렬에 맞게 설정
        self.assertEqual(product_detail['info_types'][0]['info_type_id'], self.info_type1.id)
        self.assertEqual(product_detail['info_types'][0]['info_type__name'], self.info_type1.name)
        self.assertEqual(product_detail['info_types'][1]['info_type_id'], self.info_type2.id)
        self.assertEqual(product_detail['info_types'][1]['info_type__name'], self.info_type2.name)


class TestProductItemDTO(TestCase):
    def setUp(self):
        self.product_type1 = ProductType.objects.create(
            name='의류1',
            sequence=1,
        )
        self.product_type2 = ProductType.objects.create(
            name='의류2',
            sequence=2,
        )
        self.info_type1 = InfoType.objects.create(
            name='사이즈',
        )
        self.info_type2 = InfoType.objects.create(
            name='색상',
        )
        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
        )
        self.product.product_type.add(self.product_type1)
        self.product.product_type.add(self.product_type2)
        self.product_image1 = ProductImage.objects.create(
            product=self.product,
            image='https://image1.com',
            sequence=1,
        )
        self.product_image2 = ProductImage.objects.create(
            product=self.product,
            image='https://image2.com',
            sequence=2,
        )
        self.product_info1 = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type1,
            sequence=1,
        )
        self.product_info2 = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type2,
            sequence=2,
        )
        self.product_item = ProductItem.objects.create(
            product=self.product,
            good_number='test1',
            title='test1',
            description='test1',
            additional_payment_price=1000,
        )

    def test_product_item_dto(self):
        # Given:
        # When:
        product_item = ProductItemDTO.of(self.product_item).to_dict()

        # Then:
        self.assertEqual(product_item['id'], self.product_item.id)
        self.assertEqual(product_item['good_number'], self.product_item.good_number)
        self.assertEqual(product_item['title'], self.product_item.title)
        self.assertEqual(product_item['additional_payment_price'], self.product_item.additional_payment_price)
        self.assertEqual(product_item['left_quantity'], self.product_item.left_quantity)
        self.assertEqual(product_item['is_sold_out'], self.product_item.is_sold_out)
