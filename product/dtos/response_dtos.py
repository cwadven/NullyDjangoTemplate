import attr


@attr.s
class ProductItemInfoDisplayInformationItemDTO(object):
    information = attr.ib(type=str)
    is_sold_out = attr.ib(type=bool)
    additional_min_price = attr.ib(type=int)
    additional_max_price = attr.ib(type=int)
    display = attr.ib(type=str, default='')

    def __attrs_post_init__(self):
        display_parts = []

        if self.is_sold_out:
            display_parts.append('[품절]')
        display_parts.append(self.information)

        if self.additional_min_price != 0 or self.additional_max_price != 0:
            if self.additional_min_price != self.additional_max_price:
                additional_price_range = f'{self.additional_min_price:+} ~ {self.additional_max_price:+}'
                display_parts.append(f'({additional_price_range})')
            else:
                additional_price = f'{self.additional_min_price:+}'
                display_parts.append(f'({additional_price})')

        self.display = ' '.join(display_parts)

    def to_dict(self):
        return attr.asdict(self, recurse=True)
