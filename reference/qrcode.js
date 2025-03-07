$("head").append("<link>");
$("head").children(":last").attr({
	rel: "stylesheet",
	type: "text/css",
	href: "https://sso.scut.edu.cn/cas/comm/js/scut/code.css"
});
var loginQRCode = function(target,width,height,colorDark,colorLight){
	this.target = target;
	this.width = (width == null)? 128:width;
	this.height = (height == null)? 128:height;
	this.colorDark = (colorDark == null)? "#000000":colorDark;
	this.colorLight = (colorLight == null)? "#ffffff":colorLight;
	this.intcanle = null;
};
loginQRCode.prototype.generateUUID = function() {
	var d = new Date().getTime();
	var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	  var r = (d + Math.random()*16)%16 | 0;
	  d = Math.floor(d/16);
	  return (c=='x' ? r : (r&0x3|0x8)).toString(16);
	});
	return uuid;
};
loginQRCode.prototype.generateLoginQRCode = function(callback){
	var obj = this;
	var uuid = this.generateUUID();
	var target = this.target;
	var width = this.width;
	var height = this.height;
	var qrcode = new QRCode(document.getElementById(target), {
	    width: this.width,
	    height: this.height,
	    colorDark : this.colorDark,
	    colorLight : this.colorLight,
	    correctLevel : QRCode.CorrectLevel.L
	});
	qrcode.makeCode("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx39f121ed798af736&redirect_uri=https%3A%2F%2Fsso.scut.edu.cn%2Fcas%2Fscutwxsso&response_type=code&scope=snsapi_base&state="+uuid+"#wechat_redirect");
	var timesRun = 0;
	var interval = setInterval(function(){
		timesRun += 1;
		if(timesRun === 60){
			clearInterval(interval);
			$("#"+target).addClass("code-box");
			$("#"+target).append("<div class='lose'>" +
					"<div class='code-fail'>二维码已失效</div>" +
					/*"<button class='code-refresh'>刷新</button>" +*/
					"</div>");
			var codeFail = function(a){
			    var wd = width;
			    var ht = height;
			    var fz1 = wd * 0.1;
			    var fz2 = wd * 0.1;
			    $(".code-box").css({"width":wd,"height":ht});
			    $(".code-gray").css({"width":wd,"height":ht});
			    $(".code-fail").css("font-size",fz1);
			    /*$(".code-refresh").css("font-size",fz2);*/
			};
			codeFail();
			$(window).resize(function(){
			    codeFail();
			});
			$(".code-fail").click(function(){
				$("#" + target).empty();
				obj.generateLoginQRCode(callback);
		    });
		}
		$.ajax({  
		    url:"https://sso.scut.edu.cn/cas/scutqqcheck?uuid=" + uuid,  
		    dataType:'jsonp',  
		    jsonp:'jsonpcallback', 
		    success:function(result) {  
		    	if(result!=-1&&result!=0){
		    		clearInterval(interval);
		    		callback(result);
		    	}
		    },
		    error: function(XMLHttpRequest, textStatus, errorThrown) {
			},
			complete: function(XMLHttpRequest, textStatus) {
			}
		});
	}, 2000);
	this.intcanle = interval;
};

loginQRCode.prototype.codeClear = function() {
	$("#qrcodeQQLogin").empty();
	clearInterval(this.intcanle);
};


