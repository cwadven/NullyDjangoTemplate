from django.shortcuts import render

from popup.dtos import HomePopupModalItemDTO
from popup.models import HomePopupModal


# 테스트케이스 필요
def home(request):
    home_popup_modals = [
        HomePopupModalItemDTO.of(
            home_popup, top=index * 50, left=index * 50
        ).to_dict()
        for index, home_popup in enumerate(HomePopupModal.datetime_active_objects.get_actives(), start=1)
    ]
    return render(request, 'home.html', {'home_popup_modals': home_popup_modals})
