Django_crm
==========

* [http://192.241.237.170:8080](http://192.241.237.170:8080)
  * 계정: mo/1313

* 구현된 기능
  * 기본 CRUD
  * 비동기 CRUD
  * 자동완성(Typeahead in [Bootstrap][], [Autocomplete] in Jquery plugin)
  * 실시간 처리([SockJS-tornado])
      * 채팅
      * 알림
  * infinite scroll
  * 차트 그리기(Pie Chart in [Google Charts])
  * 국가 얻어오기 via [http://freegeoip.net]

* 사용된 라이브러리
    * [Django](https://www.djangoproject.com) 1.5.2
    * [SockJs-tornado](https://github.com/mrjoes/sockjs-tornado)
    * [iptools](https://github.com/bd808/python-iptools)
    * [simplejson](http://simplejson.readthedocs.org/)

기능설명
--------
* 기본 CRUD

  ![기본 CRUD](https://raw.github.com/meoooh/django_crm/1.5.2/image/basicCRUD.jpg)
    
  * 고객등록시 `작업자`, `담당영업`은 등록된 사용자들의 이름을 입력해야합니다. 현재 등록된 사용자는 (`루트`, `김한기`, `모젯` 등이 있습니다.)

* 비동기 CRUD

  ![비동기 CRUD](https://raw.github.com/meoooh/django_crm/1.5.2/image/ajaxCRUD.jpg)

  * `대상자`엔 자동완성이 구현되어있어, 등록된 사용자의 첫번째 글자를 입력하면 자동완성이 되고, 그 사용자에겐 `확인`버튼이 생성됩니다. `확인`역시 비동기 통신을 지원합니다.

* 자동완성

  ![자동완성](https://raw.github.com/meoooh/django_crm/1.5.2/image/autocomplete.jpg)

  ![자동완성2](https://raw.github.com/meoooh/django_crm/1.5.2/image/autocomplete2.jpg)

* 실시간 처리([SockJS-tornado])
    * 채팅

      ![채팅](https://raw.github.com/meoooh/django_crm/1.5.2/image/chat.jpg)

      ![채팅](https://raw.github.com/meoooh/django_crm/1.5.2/image/chat2.jpg)

          * 자신의 채팅은 오른에, 타인의 채팅은 왼쪽에 표시되고 여러명이 동시에 채팅이 가능합니다.(채팅방 생성시 `대화상대`에 `,`(쉼표)로 구분하여 등록된 사용자의 이름을 넣으면 됩니다.)

    * 알림

      ![알림](https://raw.github.com/meoooh/django_crm/1.5.2/image/noti.jpg)

          * 메세지가 아닌 다른페이지에 머물고 있을때 다른 사용자가 `메세지(채팅)`를 보내면 `메세지`버튼이 변하고, 클릭했을때 해당 채팅방으로 바로 이동합니다.

* infinite scroll

  ![infinite scroll](https://raw.github.com/meoooh/django_crm/1.5.2/image/infiniteScroll.jpg)

  ![infinite scroll2](https://raw.github.com/meoooh/django_crm/1.5.2/image/infiniteScroll2.jpg)

* 차트 그리기(Pie Chart in [Google Charts])

  ![chart](https://raw.github.com/meoooh/django_crm/1.5.2/image/chart.jpg)

* 국가 얻어오기 via [http://freegeoip.net]

  ![country](https://raw.github.com/meoooh/django_crm/1.5.2/image/country.jpg)


[Bootstrap]: http://getbootstrap.com
[Autocomplete]: http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete
[SockJS-tornado]: https://github.com/mrjoes/sockjs-tornado
[Google Charts]: https://google-developers.appspot.com/chart/
[http://freegeoip.net]: http://freegeoip.net