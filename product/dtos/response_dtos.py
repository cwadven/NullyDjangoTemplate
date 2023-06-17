import attr


@attr.s
class ProductItemInfoDisplayInformationItemDTO(object):
    information = attr.ib(type=str)
    is_sold_out = attr.ib(type=bool)
    additional_min_price = attr.ib(type=int)
    additional_max_price = attr.ib(type=int)
    display = attr.ib(type=str, default='')

    def __attrs_post_init__(self):
        display = ''
        additional_min_price = f'+{self.additional_min_price}' if self.additional_min_price >= 0 else f'{self.additional_min_price}'
        additional_max_price = f'+{self.additional_max_price}' if self.additional_max_price >= 0 else f'{self.additional_max_price}'

        if self.is_sold_out:
            display += '[품절] '
        display += self.information
        if not (self.additional_min_price == 0 and self.additional_max_price == 0):
            display += f' ({additional_min_price} ~ {additional_max_price})'

        self.display = display

    def to_dict(self):
        return attr.asdict(self, recurse=True)
