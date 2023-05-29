import attr

from popup.models import Popup


@attr.s
class HomePopupModalItemDTO(object):
    id = attr.ib(type=int)
    description = attr.ib(type=str)
    image = attr.ib(type=str)
    on_click_link = attr.ib(type=str)
    width = attr.ib(type=int)
    height = attr.ib(type=int)
    top = attr.ib(type=int, default=None)
    left = attr.ib(type=int, default=None)

    @classmethod
    def of(cls, popup: Popup, top=None, left=None):
        return cls(
            id=popup.id,
            description=popup.description,
            image=popup.image,
            on_click_link=popup.on_click_link,
            width=popup.width,
            height=popup.height,
            top=top,
            left=left,
        )

    def to_dict(self):
        return attr.asdict(self, recurse=True)
