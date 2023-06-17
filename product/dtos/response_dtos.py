import attr


@attr.s
class ProductItemInfoDisplayInformationItemDTO(object):
    information = attr.ib(type=str)
    is_sold_out = attr.ib(type=bool)
    additional_min_price = attr.ib(type=int)
    additional_max_price = attr.ib(type=int)
    left_quantity = attr.ib(type=int)
    display = attr.ib(type=str, default='')

    def __attrs_post_init__(self):
        display_parts = []

        if self.is_sold_out:
            display_parts.append('[품절]')
            self.left_quantity = 0

        display_parts.append(self.information)

        if self.additional_min_price != 0 or self.additional_max_price != 0:
            if self.additional_min_price != self.additional_max_price:
                additional_price_range = f'{self.additional_min_price:+} ~ {self.additional_max_price:+}'
                display_parts.append(f'({additional_price_range})')
            else:
                additional_price = f'{self.additional_min_price:+}'
                display_parts.append(f'({additional_price})')

        if not self.left_quantity:
            display_parts.append('(수량 없음)')

        self.display = ' '.join(display_parts)

    def to_dict(self):
        return attr.asdict(self, recurse=True)
