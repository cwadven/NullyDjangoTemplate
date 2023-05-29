### image_modal.html 사용방법

`popups` 안에는 아래와 같은 내용이 `list` 안에 `dictionary` 로 들어가야 합니다.<br>
`modal_name` 은 `modal` 의 이름을 지정해주기 위해 설정 됩니다. (쿠키 설정을 위해 이용됩니다.)<br>

```
id: 모달들을 각각 특정할 수 있도록 하는 id
image: 이미지 주소
on_click_link: 이미지 클릭시 이동되는 주소
width: 모달의 가로 크기
height: 모달의 세로 크기
top: 모달이 뜰 위치
left: 모달이 뜰 위치
```

```html
{% include "components/modals/image_modal.html" with popups=home_popup_modals modal_name=modal_name %}
```