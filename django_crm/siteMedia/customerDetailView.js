function init(){
    $("table#equipmentList .equipmentAdd").click(function(){
        getEquipmentAddForm.call(this);
    });
    
    $("div.addCustomerNotes form").submit(function(){
        saveCustomerNote.call(this);
        return false;
    });
    
    $("textarea").autosize({className:"mirroredText"}); // textarea 늘어나는거...
    
    $("textarea").keydown(function(e) { // textarea에서 엔터치면 submit되도록...
        if(e.keyCode == 13) {
            $(this).parent().submit();
        }
    });
    
    $("div.addCustomerIPaddrs form").submit(function(){
        saveCustomerIPaddrs.call(this);
        return false;
    });
    
    $("div.more").each(function(){
        var more = this;
        
        $(more).click(function(){
            if($(more).attr('data-start')){
                listView.call(more, $(more).parent().find("ul.customerDetailViewList > li:first").attr('data-next'));
            }
            else{
                listView.call(more, $(more).parent().find("ul.customerDetailViewList > li:last").attr('data-next'));
            }
        });
        $(more).parent().find("ul.customerDetailViewList").dblclick(function(){
            if($(more).attr('data-start')){
                listView.call(more, $(more).parent().find("ul.customerDetailViewList > li:first").attr('data-next'));
            }
            else{
                listView.call(more, $(more).parent().find("ul.customerDetailViewList > li:last").attr('data-next'));
            }
        });
        listView.call(more);
    });
    
    $("div.addCustomerDomains form").submit(function(){
        saveCustomerDomains.call(this);
        return false;
    });
    
    $("div.addCustomerEquipments form").submit(function(){
        saveCustomerEquipments.call(this);
        return false;
    });
    
    $("div.addCustomerPersonInCharges > form").submit(function(){
        saveCustomerPersonInCharges.call(this);
        return false;
    });
    
    isoFormat2localeString();
}

function deleteCustomerPersonInCharges(){
    var _button = this;
    var _li = $(_button).parent().parent().parent().parent();
    var _url = customerPersonInChargeURL;
    
    if(confirm('삭제하시겠습니까?')){
        $.ajax({
            url: _url+_li.attr('data-id'),
            type: "DELETE",
            statusCode:{
                204:function(){
                    _li.remove();
                }
            },
        });
    }
}

function saveCustomerPersonInCharges(){
    var _form = this;
    var _url = customerPersonInChargeURL;
    var _div = $(_form).parent().parent();
    var _ul = _div.find("ul.customerDetailViewList");
    
    $.ajax({
        url: _url,
        type: "POST",
        data: $(_form).serialize(),
        statusCode:{
            200:function(result){
                _div.find("ul.customerDetailViewList").append('<li class="customerDetailViewList" data-id="'+result['id']+'" data-next="'+_ul.find(">li:last").attr("data-next")+'"><ul class="unstyled"><li><span class="name">'+$(_form).serializeArray()[0].value+'</span><span class="button"><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerPersonInCharges.call(this);">x</button></span></li><li><span class="tel">'+$(_form).serializeArray()[1].value+'</span></li><li><span class="mobile">'+$(_form).serializeArray()[2].value+'</span></li><li><span class="email">'+$(_form).serializeArray()[3].value+'</span></li></ul></li>');
                
                _form.reset();
                $(_form).find("input:first").focus();
            },
        },
    });
}

function deleteCustomerEquipments(){
    var _button = this;
    var _url = customerEquipmentURL;
    var _li = $(_button).parent().parent().parent();
    
    if(confirm('삭제하시겠습니까?')){
        $.ajax({
            url: _url+_li.attr('data-id'),
            type: "DELETE",
            statusCode:{
                204:function(){
                    _li.remove();
                },
            },
        });
    }
}

function saveCustomerEquipments(){
    var _form = this;
    var _url = customerEquipmentURL;
    var _div = $(_form).parent().parent();
    var _ul = _div.find("ul.customerDetailViewList");
    
    $.ajax({
        url: _url,
        type: "POST",
        data: $(_form).serialize(),
        success: function(result){ // 자식만 검색하는 방법 (">li"), $.children("li"), jQuery(">li", abc);
            _ul.append('<li class="customerDetailViewList" data-id="'+result['id']+'" data-next="'+_ul.find('>li:last').attr('data-next')+'"><ul class="unstyled"><li><span class="type">'+$(_form).serializeArray()[0].value+'</span><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerEquipments.call(this);">x</button></li><li><span class="ipaddr">'+$(_form).serializeArray()[1].value+'</span></li>');
            
            _form.reset();
            $(_form).find("input:first").focus();
        },
    });
}

function deleteCustomerDomains(){
    var _button=$(this);
    var _li=_button.parent();
    
    if(confirm('삭제하시겠습니까?')){
        $.ajax({
            url: customerDomainURL+_li.attr('data-id'),
            type: "DELETE",
            statusCode:{
                204: function(){
                    _li.remove();
                }
            }
        });
    }
}

function saveCustomerDomains(){
    var _form=$(this);
    var _div=_form.parent().parent();
    var _ul=_div.find("ul.customerDetailViewList");
    var _li=_ul.find("ul.customerDetailViewList > li:last");
    
    $.ajax({
        url: customerDomainURL+"?ajax",
        type: "POST",
        data: _form.serialize(),
        success: function(result){
            if(result['id']){
                _ul.append('<li class="customerDetailViewList" data-id="'+result['id']+'" data-next="'+_li.attr("data-next")+'"><span class="domain">'+_form.serializeArray()[0].value+'</span><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerDomains.call(this);">x</button></li>');
                
                _form[0].reset();
                _form.find("input:first").focus();
            }
        },
        statusCode:{
            500: function(){
                $('#myModal').find(".modal-body p").html("URL이 잘못되었습니다.");
                $('#myModal').modal('show');
                $('#myModal').on('hide', function(){
                    _form.find("input:first").focus();
                });
            }
        }
    });
}

function deleteCustomerIPaddrs(){
    var _button = $(this);
    var _li = _button.parent().parent();
    if(confirm('삭제하시겠습니까?')){
        $.ajax({
            url: customerIPaddrURL+_li.attr('data-id')+"/",
            type: "DELETE",
            success: function(){
                _li.remove();
            }
        });
    }
}

function listView(page){
    var more = $(this);
    if(!more.find(".loading").length){ // 이미 삽입되어있나 검사
        more.append("<img src='/siteMedia/img/ajax-loader.gif' class='loading'>");
    }
    var _url = listViewURL;
    var kind = more.attr('data-kind');
    var _ul=more.parent().find("ul.customerDetailViewList");
    var _col="?col=";
    col=more.attr('data-col');
    dsc=more.attr('data-dsc');
    last=more.attr('data-start');
    page=page||"";
    
    _url+=kind+"/"+page;
    if(page=="none"){
        return false;
    }
    else if(page){
        $.ajax({
            url:_url,
            type: "GET",
            data: {"col":col, "dsc":dsc, "last":last},
            success:function(result){
                if($(more).attr('data-start')=="last"){
                    _ul.prepend(result)
                }
                else{
                    _ul.append(result);
                }
                
                isoFormat2localeString(_ul);
                
                if($(more).attr('data-start')=="last"){
                    if(more.parent().find("ul.customerDetailViewList > li:first").attr('data-next')=="none"){
                        more.hide();
                    }
                }
                else{
                    if(more.parent().find("ul.customerDetailViewList > li:last").attr('data-next')=="none"){
                        more.hide();
                    }
                }
                more.find(".loading").remove();
            }
        });
    }
    else{
        _ul.load(_url, $.param({"col":col, "dsc":dsc, "last":last}), function(){
            if(more.parent().find("ul.customerDetailViewList > li:last").attr('data-next')=="none" || !more.parent().find("ul.customerDetailViewList > li:last").length){
                more.hide();
            }
            isoFormat2localeString(_ul);
            more.find(".loading").remove();
        });
    }
}

function saveCustomerIPaddrs(){
    var _form = $(this);
    var _div = _form.parent().parent();
    var _ul=_div.find("ul.customerDetailViewList");
    var _li=_ul.find(">li.customerDetailViewList:last");
    
    $.post(customerIPaddrURL+"?ajax", _form.serialize(), function(result){
        if(result != "0"){
            $.each(result, function(){
                _div.find("ul.customerDetailViewList").append('<li class="customerDetailViewList" data-id="'+this.pk+'" data-next="'+_li.attr('data-next')+'"><span class="ipaddr">'+this.addr+'</span><span class="button"><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerIPaddrs.call(this);;">x</button></span></li>');
            });
            _form[0].reset();
            _form.find("input:first").focus();
        }
        else{
            $('#myModal').find(".modal-body p").html("IP가 잘못되었습니다.");
            $('#myModal').modal('show');
            $('#myModal').on('hide', function(){
                _form.find("input[name=ip]").focus();
            });
        }
    });
}

function ModifyCustomerNote(){
    var _button = this;
    var _li = $(_button).parent().parent();
    var _div = _li.parent().parent().parent();
    
    _div.find("form.form-inline").children().each(function(){
        $(this).attr("disabled", true)
    });
    
    $.get(customerNoteURL+_li.attr("data-id")+"/?ajax", function(result){
        var backup_li = _li.html();
        _li.html('<form method="post" style="margin-bottom: 0" action="/" class="form-inline"><textarea name="contents" placeholder="내용" style="width:714px; height:35px;">'+result['contents']+'</textarea><button class="btn btn-mini" type="submit">완료</button></form>');
        
        _li.find("form").submit(backup_li, function(){
            saveModifyCustomerNote.call(this, backup_li);
            return false;
        });
        
        _li.find("textarea").autosize({className:"mirroredText"}); // textarea 늘어나는거...
    
        _li.find("textarea").keydown(function(e){ // textarea에서 엔터치면 submit되도록...
            if(e.keyCode == 13){
                $(this).parent().submit();
            }
        });
        
        var _tmp = _li.find("textarea").val()
        _li.find("textarea").focus().val('').val(_tmp); // 그냥 _li.find("textarea").focus()하면 커서가 맨 앞으로 간다.
                                                        // 그런데 여기처럼 하면 맨뒤로 간다.
                                                        // _li.find("textarea").focus()
    });
}

function saveModifyCustomerNote(li){
            var _form = $(this);
            var contents = _form.children().first().val()
            $.ajax({
                url: customerNoteURL+_form.parent().attr("data-id")+"/?ajax",
                type: "PUT",
                data: _form.serialize(),
                success: function(result){
                    if(result == "1"){
                        var _li=_form.parent().html(li).find("strong").html(contents).parent();
                        
                        if(!_li.parent().find('button.delete').attr('onclick')){
                            _li.parent().find('button.delete').click(function(){
                                deleteCustomerNote.call(this);
                            });
                        }
                        
                        if(!_li.parent().find("button.modify").attr('onclick')){
                            _li.parent().find("button.modify").click(function(){
                                ModifyCustomerNote.call(this);
                            });
                        }
                        
                        //위 두부분을 주석처리 해야하는 이유는 노트(이력사항)부분을 ajax로 구현하기 전에는
                        //버튼에 onclick를 직접 코딩해주지않고, 이 js파일에서 바인드 시켰었다.
                        //하지만 노트를 아작스로 바꾸고 직접 응답에 온크릭에 함수호출을 하였으므로,
                        // 위 두부분까지 작동하면 바인드가 두번되므로 함수가 두번 호출되어 오작동을 일으킨다.
                        
                        //다시 주석을 해제하였다. 이유는 아작스로 노트를 새로 추가할때에는 버튼에 onclick를 
                        //입력하지 않는다 그렇기 때문에 onclick속성에 뭔가 있으면 추가 바인딩을 안해주는걸로 바꿨다.
                        // 근데 항상 바인딩할때 어떤 값이 들어있나 확인해보고 바인딩하는게 좋은 습관인것같다.
                        
                        _li.parent().parent().parent().parent().find("form.form-inline").children().each(function(){
                            $(this).attr("disabled", false)
                        });
                    }
                    else{
                        alert("실패");
                    }
                }
            });
}

function deleteCustomerNote(){
    var _button=this;
    var li=$(_button).parent().parent(); // li
    
    if(confirm('삭제하시겠습니까?')){
        $.ajax({
            url: customerNoteURL+li.attr("data-id")+"/?ajax",
            type: "DELETE",
            success: function(result){
                if(result == "1"){
                    li.remove();
                }
                else{
                    alert("실패");
                }
            }
        });
    }
}

function getEquipmentAddForm(){
    var _button=this;
    var equipmentListTable = $(_button).parent();
}

function saveCustomerNote(){
    var _form=$(this);
    
    $.post(customerNoteURL+"?ajax", _form.serialize(), function(result){
        _form.each(function(){
            this.reset();
        });
        _form.children()[0].style.height="35px";
        
        var _li = $('<li class="customerDetailViewList" data-id='+result['id']+'></li>').append('<span class="time">'+result['date']+'</span>').append('<span class="contents"><strong>'+result['contents']+'</strong></span>').append('<span class="name">['+result['name']+']</span>').append('<span class="button"><button class="btn btn-mini modify" type="button" onclick="ModifyCustomerNote.call(this);">수정</button><button class="btn btn-mini delete" type="button" onclick="deleteCustomerNote.call(this);">삭제</button></span>');
        
        isoFormat2localeString(_li);
        
        _form.parent().parent().find('ul.customerDetailViewList').append(_li);
        
        if(!_li.find('button.delete').attr('onclick')){
            _li.find('button.delete').click(function(){
                deleteCustomerNote.call(this);
            });
        }
        
        if(!_li.find("button.modify").attr('onclick')){
            _li.find("button.modify").click(function(){
                ModifyCustomerNote.call(this);
            });
        }
    });
}

$(document).ready(init);