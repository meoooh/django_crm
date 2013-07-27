function read(pk){
    var text = [];
    text.push("read");
    text.push({});
    text[1].msgPk=pk;

    conn.send( JSON.stringify(text) );
}

function init(){
    // https://github.com/sockjs/sockjs-client#sockjs-class
    // var sockjs = new SockJS(url, _reserved, options);
    // option을 비워두면 모든 프로토콜 사용이 기본값.
    
    $("form#chat_broadcast").children().each(function(){$(this).attr('disabled',true);});
    var chatTable = $('table#chatTable');
    var result = '';

    conn.onopen = function() {
        $(window).scrollTop($(window).scrollTop()+10000) // 스크롤 맨 밑으로 내리기
        $("form#chat_broadcast").children().each(function(){$(this).attr('disabled',false);});
        $("#id_message").focus();
        console.log('open');
        var text = [];
        text.push("join"); // ['join',{'join': roomId}]
        text.push({});
        text[1].join=roomId;

        conn.send( JSON.stringify(text) );

        $("ul.isRead").each(function(){read($(this).attr('data-pk'));});

    };
    conn.onmessage = function(e) {
        var tr = '';
        console.log('message', e.data);
        result = $.parseJSON(e.data)||'';

        if(result == ''){
            alert('오류');
        }
        if(result[0] == 'msg'){
            result = result[1];

            if(result['id'] == userId){
                tr =  '<tr>';
                tr +=   '<td>&nbsp;</td>';
                tr +=   '<td width="50%">';
                tr +=       '<ul class="unstyled" data-pk="'+result['pk']+'" title="'+result['date']+'">';
                tr +=           '<li><strong>'+result['name']+'</strong></li>';
                tr +=           '<li>'+result['msg']+'</li>';
                tr +=           '<li><font size="1">'+Date.create(result['date']).relative('ko')+'</font></li>';
                tr +=       '</ul>';
                tr +=   '</td>'
                tr += '</tr>';

                noti('msg', roomId);
            }
            else{
                tr =  '<tr>';
                tr +=   '<td width="50%">';
                tr +=       '<ul class="unstyled" data-pk="'+result['pk']+'" title="'+result['date']+'">';
                tr +=           '<li><strong>'+result['name']+'</strong></li>';
                tr +=           '<li>'+result['msg']+'</li>';
                tr +=           '<li><font size="1">'+Date.create(result['date']).relative('ko')+'</font></li>';
                tr +=       '</ul>';
                tr +=   '</td>'
                tr +=   '<td>&nbsp;</td>';
                tr += '</tr>';

                read(result['pk']);
            }

            chatTable.append(tr);
            $(window).scrollTop($(window).scrollTop()+10000) // 스크롤 맨 밑으로 내리기
        }
        else if(result[0] == 'typing'){
            $('#typing').html(result[1]+'입력하고있습니다.');
        }
    };
    conn.onclose = function() {
        console.log('close');
    };

/*    $('#id_message').keyup(function(){
        var text=[];

        text.push('typing');
        text.push({'roomId': roomId});

        conn.send(JSON.stringify(text));
    });
*/
    $('form').submit(function(){
        var form = this;
        var contents = $(form).serializeArray()[0].value;

        var text = []; // ['msg',{'roomId': roomId, 'msg':'바보'}]
        text.push("msg");
        text.push({});
        text[1].roomId=roomId;
        text[1].msg=contents;

        conn.send( JSON.stringify(text) );

        form.reset();
        $('#id_message').val('').focus();
        return false;
    });
}

$(document).ready(init);