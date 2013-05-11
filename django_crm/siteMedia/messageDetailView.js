var conn = null;

function init(){
    // https://github.com/sockjs/sockjs-client#sockjs-class
    // var sockjs = new SockJS(url, _reserved, options);
    // option을 비워두면 모든 프로토콜 사용이 기본값.
    if(conn==null){
        conn = new SockJS('http://meoooh.iptime.org:7070/chat');
    }
    else{
        conn.close();
    }

    var chatTable = $('table#chatTable');
    var result = '';

    conn.onopen = function() {
        console.log('open');
    };
    conn.onmessage = function(e) {
        var tr = '';
        console.log('message', e.data);
        result = $.parseJSON(e.data)||'';

        if(result == ''){
            alert('오류');
        }

        if(result['id'] == userId){
            tr =  '<tr>';
            tr +=   '<td>&nbsp;</td>';
            tr +=   '<td width="50%">';
            tr +=       '<ul class="unstyled" title="'+result['date']+'">';
            tr +=           '<li><strong>'+result['name']+'</strong></li>';
            tr +=           '<li>'+result['msg']+'</li>';
            tr +=       '</ul>';
            tr +=   '</td>'
            tr += '</tr>';
        }
        else{
            tr =  '<tr>';
            tr +=   '<td width="50%">';
            tr +=       '<ul class="unstyled" title="'+result['date']+'">';
            tr +=           '<li><strong>'+result['name']+'</strong></li>';
            tr +=           '<li>'+result['msg']+'</li>';
            tr +=       '</ul>';
            tr +=   '</td>'
            tr +=   '<td>&nbsp;</td>';
            tr += '</tr>';
        }

        chatTable.append(tr);
    };
    conn.onclose = function() {
        console.log('close');
    };

    $('form').submit(function(){
        var form = this;
        var text = $(form).serializeArray()[0].value;

        var text = '{"roomId":"'+roomId+'", "msg": "'+text+'"}';

        conn.send(text);

        form.reset();
        return false;
    });
}

$(document).ready(init);