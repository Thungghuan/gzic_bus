$(function() {
	var setting = {
		imageWidth : 1680,
		imageHeight : 1050
	};
	var init = function() {
		var windowHeight = $(window).height();
		var windowWidth = $(window).width();
		$(".login_conatiner").css("height",windowHeight);
		$(".login_conatiner").css("width",windowWidth);

		$("#container_bg").css("height",windowHeight);
		$("#container_bg").css("width",windowWidth);

		$("#login_right_box").css("height",windowHeight);

		var imgW = setting.imageWidth;
		var imgH = setting.imageHeight;
		var ratio = imgH / imgW; // 图片的高宽比

		imgW = windowWidth; // 图片的宽度等于窗口宽度
		imgH = Math.round(windowWidth * ratio); // 图片高度等于图片宽度 乘以 高宽比

		if (imgH < windowHeight) { // 但如果图片高度小于窗口高度的话
			imgH = windowHeight; // 让图片高度等于窗口高度
			imgW = Math.round(imgH / ratio); // 图片宽度等于图片高度 除以 高宽比
		}

		$(".login_img_01").width(imgW).height(imgH); // 设置图片高度和宽度
	};

	init();

	$(window).resize(function() {
		init();
	});

	//登录按钮触发
	$("#index_login_btn").unbind("click").bind("click", function(){
		login();
	});

	//文本域keyup事件
	$("#PM1").keyup(function(e){
		if(e.which == 13) {
			login();
		}
	}).keydown(function(e){
		$(this).parent().removeClass("login_error_border");
		$("#errormsg").parent().hide();
	}).focus();


	//如果有错误信息，则显示
	if($("#errormsg").text()){
		$("#errormsg").parent().show();
	}

	//密码找回的中英文切换
	if($("#change_language").attr("value") == "中文"){
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=en");
	}else{
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=zh_CN");
	}
	$("#change_language").unbind("click").click(function(){
		var re=eval('/(locale=)([^&]*)/gi');
		var url = window.location.href;
		if($("#change_language").attr("value") == "中文"){
			if(url.indexOf("locale") >= 0 ) {
				url=url.replace(re,'locale=zh_CN');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=zh_CN";
				}else{
					location.href=url+"?locale=zh_CN";
				}
			}
		}else if($("#change_language").attr("value") == "English") {
			if(url.indexOf("locale") >= 0 ) {
				url=url.replace(re,'locale=en');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=en";
				}else{
					location.href=url+"?locale=en";
				}
			}
		}
	});

});

function login(){
	$("#loginForm")[0].submit();
}

var times=0//计时器初始化

/**
 *
 * @param id 被修改的id
 * @constructor
 */
function Interval(id, time, max, text, text2){
	if(max == 1){
		var id1 = document.getElementById(id);//动态显示计时器
		id1.textContent=text2;
		$("#"+id).unbind('click');
	}else{
		times = time;
		var oo=setInterval(function(){
			if (times-1<=0){
				Close(oo)
			}
			times--
			// console.log(times)
			if (times<=0){//当计时器小于0
				var id1 = document.getElementById(id);
				id1.textContent=text//修改指定id的数据
				$("#"+id).click(function(){
					window.location.reload();
				});
				$("#"+id).css('color','');
			}else {
				var id1 = document.getElementById(id);//动态显示计时器
				id1.textContent=text+'('+times+')';
				$("#"+id).unbind('click');
				$("#"+id).css('color','#666');
			}

		},1000)  //每隔一秒钟
	}
}

/**
 * 关闭计时器
 * @param id 要关闭计时器的变量名
 * @constructor
 */
function Close(id){
	clearInterval(id)
}

function ATimer(id,time) {
	times = time;
	if (times <= 0) {
		Interval(id);
	}else {
		alert("请在"+times+"秒后再试")

	}
}