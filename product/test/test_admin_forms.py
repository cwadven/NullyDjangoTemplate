from unittest.mock import patch, PropertyMock

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.forms.admin_forms import ProductItemAdminForm
from product.models import Product, ProductInfo, InfoType, ProductItem


class TestProductItemAdminForm(TestCase):
    def setUp(self):
        self.info_type=InfoType.objects.create(
            name='test',
        )
        self.product = Product.objects.create(
            title='test',
            description='test',
            real_price=1000,
            payment_price=1000,
        )
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            info_type=self.info_type,
        )
        self.product_item = ProductItem.objects.create(
            product=self.product,
            good_number='test1',
            title='test1',
            description='test1',
            additional_payment_price=1000,
        )
        self.form_data = {
            'product': self.product.id,
            'good_number': '1111111111',
            'title': 'test_title',
            'additional_payment_price': 1000,
            'bought_count': 0,
            'left_quantity': 0,
        }

    def test_clean_should_fail_when_info_type_is_not_same_with_product(self):
        # Given: info_type 가 없는 경우
        self.form_data['product_item_infos-TOTAL_FORMS'] = '0'

        form = ProductItemAdminForm(self.form_data)
        self.assertEqual(form.is_valid(), False)

        # When:
        with self.assertRaises(ValidationError) as e:
            form.clean()

        # Then: ProductItem 에는 info_type 이 Product 와 같게 들어가야 한다.
        self.assertEqual(e.exception.message, '상품 아이템 디테일 정보에 test 정보가 필요합니다.')

    @patch.object(ProductItemAdminForm, 'cleaned_data', new_callable=PropertyMock, create=True)
    def test_clean_should_success(self, mock_cleaned_data):
        # Given: info_type 가 없는 경우
        self.form_data['product_item_infos-TOTAL_FORMS'] = '1'
        self.form_data['product_item_infos-0-info_type'] = self.info_type.id

        # And: cleaned_data 모킹
        mock_cleaned_data.return_value = {
            'product': self.product,
        }

        # When:
        form = ProductItemAdminForm(self.form_data)

        # Then:
        self.assertEqual(form.is_valid(), True)


class InlineDataAdminFormTestCase(TestCase):
    def setUp(self):
        self.form = ProductItemAdminForm()

    def test_set_inline_field_datas(self):
        # Given:
        self.form.data = {
            'product_time_infos-TOTAL_FORMS': '1',
            'product_time_infos-0-info_type': '1',
        }

        # When:
        self.form._set_inline_field_datas(['product_time_info__info_type'])

        # Then:
        self.assertTrue(hasattr(self.form, 'product_time_info__info_type'))
        self.assertEqual(self.form.product_time_info__info_type, ['1'])
