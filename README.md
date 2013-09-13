Django_crm
==========

* 구현된 기능
  * 기본 CRUD
  * 비동기 CRUD
  * 자동완성(Typeahead in [Bootstrap][], [Autocomplete] in Jquery plugin)
  * 실시간 처리([SockJS-tornado])
      * 채팅
      * 알림
  * infinite scroll
  * 그래프 그리기(Pie Chart in [Google Charts])
  * 국가 얻어오기 via [http://freegeoip.net]

* 사용된 라이브러리
    * [Django](https://www.djangoproject.com) 1.5.2
    * [SockJs-tornado](https://github.com/mrjoes/sockjs-tornado)
    * [iptools](https://github.com/bd808/python-iptools)
    * [simplejson](http://simplejson.readthedocs.org/)

기능설명
--------
* 기본 CRUD
![기본 CRUD](http://img.naver.net/static/www/u/2013/0819/nmms_111143893.gif)
    * 고객등록시 `작업자`, `담당영업`은 등록된 사용자들의 이름을 입력해야합니다. 현재 등록된 사용자는 (`루트`, `김한기`, `모젯` 등이 있습니다.)

---
[Bootstrap]: http://getbootstrap.com
[Autocomplete]: http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete
[SockJS-tornado]: https://github.com/mrjoes/sockjs-tornado
[Google Charts]: https://google-developers.appspot.com/chart/
[http://freegeoip.net]: http://freegeoip.net