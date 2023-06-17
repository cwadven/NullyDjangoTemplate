import json

from django.test import TestCase, Client
from django.urls import reverse

from config.test_helpers.helpers import LoginMixin
from product.exception_codes import ProductItemDoesNotExistsException
from product.models import ProductItemInfo, ProductItem, ProductInfo, Product, InfoType


class GetProductItemInfoInformationWithProductItemIdTestCase(LoginMixin, TestCase):
    def setUp(self):
        super(GetProductItemInfoInformationWithProductItemIdTestCase, self).setUp()
        self.c = Client()
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

    def test_get_product_item_info_information_with_product_item_id_valid_request_and_is_last_selection_is_false(self):
        # Given:
        product_id = self.product.id
        info_type_id = self.info_type_size.id
        product_item_infos_information = ['빨강']
        is_last_selection = False
        request_data = {
            'info_type_id': info_type_id,
            'product_item_infos_information': product_item_infos_information,
            'is_last_selection': is_last_selection
        }

        # When:
        response = self.c.post(
            reverse('product:get_product_item_info_information_with_product_item_id', kwargs={'product_id': product_id}),
            data=json.dumps(request_data),
            content_type='application/json'
        )

        # Then:
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        # And: 2 개 (S, M)
        self.assertEqual(len(response_data['info']), 2)
        self.assertEqual(response_data['info'][0], {'information': 'S', 'is_sold_out': False, 'additional_min_price': -5000, 'additional_max_price': -5000, 'display': 'S (-5000)'})
        self.assertEqual(response_data['info'][1], {'information': 'M', 'is_sold_out': False, 'additional_min_price': 5000, 'additional_max_price': 5000, 'display': 'M (+5000)'})
        self.assertEqual(response_data['product_item_id'], None)

    def test_get_product_item_info_information_with_product_item_id_valid_request_and_is_last_selection_true(self):
        # Given:
        product_id = self.product.id
        info_type_id = self.info_type_pattern.id
        product_item_infos_information = ['빨강', 'M']
        is_last_selection = True
        request_data = {
            'info_type_id': info_type_id,
            'product_item_infos_information': product_item_infos_information,
            'is_last_selection': is_last_selection
        }

        # When:
        response = self.c.post(
            reverse('product:get_product_item_info_information_with_product_item_id', kwargs={'product_id': product_id}),
            data=json.dumps(request_data),
            content_type='application/json'
        )

        # Then:
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        # And: 1 개 (물방울)
        self.assertEqual(len(response_data['info']), 1)
        self.assertEqual(response_data['info'][0], {'information': '물방울', 'is_sold_out': False, 'additional_min_price': 5000, 'additional_max_price': 5000, 'display': '물방울 (+5000)'})
        self.assertEqual(response_data['product_item_id'], self.product_item_r_m_b.id)

    def test_get_product_item_info_information_with_product_item_id_invalid_content_type(self):
        # Given:
        product_id = self.product.id
        request_data = {
            'info_type_id': self.info_type_size.id,
            'product_item_infos_information': ['빨강', '파랑'],
            'is_last_selection': True
        }

        # When: content_type 이 text/plain 일 때
        response = self.c.post(
            reverse('product:get_product_item_info_information_with_product_item_id', kwargs={'product_id': product_id}),
            data=json.dumps(request_data),
            content_type='text/plain'
        )

        # Then:
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid content_type')

    def test_get_product_item_info_information_with_product_item_id_invalid_json(self):
        # Given:
        product_id = self.product.id
        request_data = 'invalid-json'

        # When:
        response = self.c.post(
            reverse('product:get_product_item_info_information_with_product_item_id',
                    kwargs={'product_id': product_id}),
            data=request_data,
            content_type='application/json'
        )

        # Given:
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid JSON')


class GetProductItemDataTestCase(LoginMixin, TestCase):
    def setUp(self):
        super(GetProductItemDataTestCase, self).setUp()
        self.c = Client()
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

    def test_get_product_item_data(self):
        # Given:
        # When:
        response = self.c.get(
            reverse('product:get_product_item_data',
                    kwargs={'product_item_id': self.product_item_r_m_b.id}),
            content_type='text/plain'
        )

        # Then:
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.product_item_r_m_b.id)
        self.assertEqual(response_data['good_number'], self.product_item_r_m_b.good_number)
        self.assertEqual(response_data['title'], self.product_item_r_m_b.title)
        self.assertEqual(response_data['additional_payment_price'], self.product_item_r_m_b.additional_payment_price)
        self.assertEqual(response_data['left_quantity'], self.product_item_r_m_b.left_quantity)
        self.assertEqual(response_data['is_sold_out'], self.product_item_r_m_b.is_sold_out)
        self.assertEqual(
            response_data['total_payment_price'],
            self.product_item_r_m_b.additional_payment_price + self.product_item_r_m_b.product.payment_price,
        )

    def test_get_product_item_data_should_raise_exceptions_when_not_exists(self):
        # Given:
        # When:
        response = self.c.get(
            reverse('product:get_product_item_data',
                    kwargs={'product_item_id': 9090000000}),
            content_type='text/plain'
        )

        # Then:
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], ProductItemDoesNotExistsException.default_detail)
