from django.test import TestCase

from common_library import get_filtered_by_startswith_text_and_convert_to_standards


class CommonLibraryTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_filtered_by_startswith_text_and_convert_to_standards(self):
        # Given:
        keys = [
            'home_popup_modal_1',
            'home_popup_modal_2',
            'home_popup_modal_3',
            'home_popup_modal_4',
            'k_popup_modal_10',
            'popup_modal_5',
        ]
        expected_output_no_conversion = ['1', '2', '3', '4']
        expected_output_with_conversion = [1, 2, 3, 4]

        # When: is_integer=False
        output_no_conversion = get_filtered_by_startswith_text_and_convert_to_standards('home_popup_modal_', keys)
        # Then:
        self.assertEqual(output_no_conversion, expected_output_no_conversion)

        # When: is_integer=True
        output_with_conversion = get_filtered_by_startswith_text_and_convert_to_standards(
            'home_popup_modal_', keys, is_integer=True)
        # Then:
        self.assertEqual(output_with_conversion, expected_output_with_conversion)
