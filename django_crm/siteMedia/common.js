function isoFormat2localeString(obj){
	if(!obj){
		$("span.time").each(function(){
			this.title=this.innerHTML;
			this.innerHTML="("+new Date(this.innerHTML).toLocaleString()+")";
		});
	}
	else{
		obj.find("span.time").each(function(){
			if(!this.title){
				this.title=this.innerHTML;
				this.innerHTML="("+new Date(this.innerHTML).toLocaleString()+")";
			}
		});
	}
}

function init(){
	isoFormat2localeString();
}

$(document).ready(init);