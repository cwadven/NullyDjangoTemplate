import attr


@attr.s
class ProductItemInfoInformationReqeustDto(object):
    product_item_infos_information = attr.ib(type=list)
    info_type_id = attr.ib(type=int)
    is_before_last_selection = attr.ib(type=bool)
    is_last_selection = attr.ib(type=bool)

    @classmethod
    def by_request(cls, data) -> 'ProductItemInfoInformationReqeustDto':
        return cls(
            product_item_infos_information=data.get('product_item_infos_information'),
            info_type_id=data.get('info_type_id'),
            is_before_last_selection=data.get('is_before_last_selection'),
            is_last_selection=data.get('is_last_selection'),
        )

    def to_dict(self):
        return attr.asdict(self, recurse=True)
