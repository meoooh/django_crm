function isoFormat2localeString(obj){
	if(!obj){
		$("span.time").each(function(){
			this.title=this.innerText;
			this.innerText="("+new Date(this.innerText).toLocaleString()+")";
		});
	}
	else{
		obj.find("span.time").each(function(){
			if(!this.title){
				this.title=this.innerText;
				this.innerText="("+new Date(this.innerText).toLocaleString()+")";
			}
		});
	}
}

function init(){
	isoFormat2localeString();
}

$(document).ready(init);