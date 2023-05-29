from typing import Sequence

from django.db.models import Q
from django.shortcuts import render

from common_library import get_filtered_by_startswith_text_and_convert_to_standards
from popup.dtos import HomePopupModalItemDTO
from popup.models import HomePopupModal


def home(request):
    modal_name = 'home_popup_modal_'
    exclude_home_popup_modal_ids = get_filtered_by_startswith_text_and_convert_to_standards(
        modal_name,
        request.COOKIES.keys(),
        True,
    )
    home_popup_modals = [
        HomePopupModalItemDTO.of(
            home_popup, top=index * 50, left=index * 50
        ).to_dict()
        for index, home_popup in enumerate(HomePopupModal.datetime_active_objects.get_actives().filter(
            ~Q(id__in=exclude_home_popup_modal_ids)
        ), start=1)
    ]
    return render(request, 'home.html', {'home_popup_modals': home_popup_modals, 'modal_name': modal_name})
