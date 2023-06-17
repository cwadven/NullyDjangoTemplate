from unittest.mock import patch

from django.test import TestCase

from product.exception_codes import ProductDoesNotExistsException
from product.models import Product, ProductItem, ProductItemInfo, InfoType, ProductInfo
from product.services import get_active_product, get_active_product_item_filter, \
    get_product_item_id_by_product_item_info, get_left_product_item_infos, apply_additional_prices, \
    apply_information_sold_out


class TestGetActiveProduct(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
        )

    def test_get_active_product_should_raise_when_is_deleted(self):
        # Given: is_delete True 인 경우
        self.product.is_deleted = True
        self.product.is_active = True
        self.product.save()

        # When: 에러 반환
        with self.assertRaises(ProductDoesNotExistsException) as e:
            get_active_product(self.product.id)

        # Then:
        self.assertEqual(e.exception.default_detail, ProductDoesNotExistsException.default_detail)

    def test_get_active_product_should_return_product(self):
        # Given: is_delete False 인 경우
        self.product.is_deleted = False
        self.product.is_active = True
        self.product.save()

        # When:
        product = get_active_product(self.product.id)

        # Then: product 반환
        self.assertEqual(product.id, self.product.id)


class TestGetActiveProductItemFilter(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
        )
        self.product_item_deleted = ProductItem.objects.create(
            product=self.product,
            good_number='test1',
            title='test1',
            description='test1',
            additional_payment_price=1000,
            is_active=True,
            is_deleted=True
        )
        self.product_item_not_deleted = ProductItem.objects.create(
            product=self.product,
            good_number='test2',
            title='test2',
            description='test2',
            additional_payment_price=1000,
            is_active=True,
        )

    def test_get_active_product_item_filter_should_raise_when_is_deleted(self):
        # Given:
        # When:
        qs = get_active_product_item_filter()

        # Then: 삭제되지 않은 것 조회 성공
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].id, self.product_item_not_deleted.id)


class TestGetProductItemIdByProductItemInfo(TestCase):
    def setUp(self):
        self.info_type_color = InfoType.objects.create(
            name='색상',
        )
        self.info_type_size = InfoType.objects.create(
            name='사이즈',
        )
        self.info_type_pattern = InfoType.objects.create(
            name='패턴',
        )

        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
            is_active=True,
        )
        self.product_info_color = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_color,
            sequence=1,
        )
        self.product_info_size = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_size,
            sequence=2,
        )
        self.product_info_pattern = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_pattern,
            sequence=3,
        )

        self.product_item_r_s_b = ProductItem.objects.create(
            product=self.product,
            good_number='001',
            title='Test Item1',
            description='Test description1',
            additional_payment_price=5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_s_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_s_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_size,
            sequence=2,
            information='S',
        )
        self.product_item_r_s_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )
        self.product_item_r_m_b = ProductItem.objects.create(
            product=self.product,
            good_number='002',
            title='Test Item2',
            description='Test description2',
            additional_payment_price=5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_m_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_m_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_size,
            sequence=1,
            information='M',
        )
        self.product_item_r_m_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )

    def test_get_product_item_id_by_product_item_info(self):
        # Given: 빨강을 가지고 있는 product_item 을 구합니다.
        product_item_infos_information = ['빨강']

        # When:
        result = get_product_item_id_by_product_item_info(self.product.id, product_item_infos_information)

        # Then: product_id 에 묶여있는 product_item 들중 빨강을 가지고 있는 product_item 을 구합니다.
        self.assertEqual(result.count(), 2)
        self.assertEqual(result[0], self.product_item_r_s_b.id)
        self.assertEqual(result[1], self.product_item_r_m_b.id)

        # Given: 빨강, S 를 가지고 있는 product_item 을 구합니다.
        product_item_infos_information = ['빨강', 'S']

        # When:
        result = get_product_item_id_by_product_item_info(self.product.id, product_item_infos_information)

        # Then: product_id 에 묶여있는 product_item 들중 빨강, S을 가지고 있는 product_item 을 구합니다.
        self.assertEqual(result.count(), 1)
        self.assertEqual(result[0], self.product_item_r_s_b.id)

        # Given: 빨강, 물방울 를 가지고 있는 product_item 을 구합니다.
        product_item_infos_information = ['빨강', '물방울']

        # When:
        result = get_product_item_id_by_product_item_info(self.product.id, product_item_infos_information)

        # Then: product_id 에 묶여있는 product_item 들중 빨강, 물방울 가지고 있는 product_item 을 구합니다.
        self.assertEqual(result.count(), 2)
        self.assertEqual(result[0], self.product_item_r_s_b.id)
        self.assertEqual(result[1], self.product_item_r_m_b.id)

        # Given: product_item 을 구합니다.
        product_item_infos_information = []

        # When:
        result = get_product_item_id_by_product_item_info(self.product.id, product_item_infos_information)

        # Then: product_id 에 묶여있는 product_item 들을 전부 구합니다.
        self.assertEqual(result.count(), 2)
        self.assertEqual(result[0], self.product_item_r_s_b.id)
        self.assertEqual(result[1], self.product_item_r_m_b.id)


class TestGetLeftProductItemInfos(TestCase):
    def setUp(self):
        self.info_type_color = InfoType.objects.create(
            name='색상',
        )
        self.info_type_size = InfoType.objects.create(
            name='사이즈',
        )
        self.info_type_pattern = InfoType.objects.create(
            name='패턴',
        )

        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
            is_active=True,
        )
        self.product_info_color = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_color,
            sequence=1,
        )
        self.product_info_size = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_size,
            sequence=2,
        )
        self.product_info_pattern = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_pattern,
            sequence=3,
        )

        self.product_item_r_s_b = ProductItem.objects.create(
            product=self.product,
            good_number='001',
            title='Test Item1',
            description='Test description1',
            additional_payment_price=5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_s_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_s_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_size,
            sequence=2,
            information='S',
        )
        self.product_item_r_s_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )
        self.product_item_r_m_b = ProductItem.objects.create(
            product=self.product,
            good_number='002',
            title='Test Item2',
            description='Test description2',
            additional_payment_price=5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_m_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_m_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_size,
            sequence=1,
            information='M',
        )
        self.product_item_r_m_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )

    def test_get_left_product_item_infos(self):
        # Given: product_item_infos_information 아무것도 없을 경우
        product_item_infos_information = []
        # When:
        result = get_left_product_item_infos(self.product.id, self.info_type_color.id, product_item_infos_information)
        # Then:
        self.assertEqual(result, (['빨강'], [self.product_item_r_s_b.id, self.product_item_r_m_b.id]))

        # Given: 빨강을 알아내고 사이즈를 알고 싶은 경우
        product_item_infos_information = ['빨강']
        # When:
        result = get_left_product_item_infos(self.product.id, self.info_type_size.id, product_item_infos_information)
        # Then: M, S 정렬 순서를 기준으로 가져옵니다. (S 가 2고 M 이 1 입니다)
        self.assertEqual(result, (['M', 'S'], [self.product_item_r_m_b.id, self.product_item_r_s_b.id]))

        # Given:
        product_item_infos_information = ['빨강', 'S']
        # When:
        result = get_left_product_item_infos(self.product.id, self.info_type_pattern.id, product_item_infos_information)
        # Then:
        self.assertEqual(result, (['물방울'], [self.product_item_r_s_b.id]))

        # Given:
        product_item_infos_information = ['물방울']
        # When:
        result = get_left_product_item_infos(self.product.id, self.info_type_size.id, product_item_infos_information)
        # Then:
        self.assertEqual(result, (['M', 'S'], [self.product_item_r_m_b.id, self.product_item_r_s_b.id]))


class ApplyInforamtionInfoTestCase(TestCase):

    def setUp(self):
        self.info_type_color = InfoType.objects.create(
            name='색상',
        )
        self.info_type_size = InfoType.objects.create(
            name='사이즈',
        )
        self.info_type_pattern = InfoType.objects.create(
            name='패턴',
        )

        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
            is_active=True,
        )
        self.product_info_color = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_color,
            sequence=1,
        )
        self.product_info_size = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_size,
            sequence=2,
        )
        self.product_info_pattern = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type_pattern,
            sequence=3,
        )

        self.product_item_r_s_b = ProductItem.objects.create(
            product=self.product,
            good_number='001',
            title='Test Item1',
            description='Test description1',
            additional_payment_price=-5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_s_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_s_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_size,
            sequence=2,
            information='S',
        )
        self.product_item_r_s_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_s_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )
        self.product_item_r_m_b = ProductItem.objects.create(
            product=self.product,
            good_number='002',
            title='Test Item2',
            description='Test description2',
            additional_payment_price=5000,
            bought_count=10,
            left_quantity=5,
            is_sold_out=False,
            is_active=True,
        )
        self.product_item_r_m_b_color = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_color,
            sequence=1,
            information='빨강',
        )
        self.product_item_r_m_b_size = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_size,
            sequence=1,
            information='M',
        )
        self.product_item_r_m_b_pattern = ProductItemInfo.objects.create(
            product_item=self.product_item_r_m_b,
            info_type=self.info_type_pattern,
            sequence=1,
            information='물방울',
        )

    def test_apply_additional_prices(self):
        # Given:
        information = ['S', 'M']
        product_item_ids = [self.product_item_r_s_b.id, self.product_item_r_m_b.id]

        # When: apply_additional_prices 함수를 호출합니다.
        result = apply_additional_prices(information, product_item_ids)

        # Then: 예상되는 결과와 일치하는지 확인합니다.
        expected_result = [
            f'S ({self.product_item_r_s_b.additional_payment_price})',
            f'M (+{self.product_item_r_m_b.additional_payment_price})',
        ]
        self.assertEqual(result, expected_result)

    def test_apply_information_sold_out(self):
        # Given:
        information = ['S', 'M']
        product_id = self.product.id
        # And:
        self.product_item_r_m_b.is_sold_out = True
        self.product_item_r_m_b.save()

        # When: apply_information_sold_out 함수를 호출합니다.
        result = apply_information_sold_out(information, product_id, self.info_type_size.id)

        # Then: 예상되는 결과와 일치하는지 확인합니다.
        expected_result = ['S', '[품절] M']
        self.assertEqual(result, expected_result)
