// MASTER OBJ TO HOLD EVERYTHING
var mv={};

mv.isIOS = false;

// AHA BANNER - SERVE JPG/GIF IF IOS DETECTED
if(/(iPhone|iPod|iPad)/i.test(navigator.userAgent)) {
    if(/OS [2-4]_\d(_\d)? like Mac OS X/i.test(navigator.userAgent)) {
        // iOS 2-4 so Do Something
		mv.isIOS = true;
    } else if(/CPU like Mac OS X/i.test(navigator.userAgent)) {
        // iOS 1 so Do Something
		mv.isIOS = true;
    } else {
        // iOS 5 or Newer so Do Nothing
		mv.isIOS = true;
    }
}
//mv.isIOS=true;
// BUILD BANNER IF DIV EXISTS
if(document.getElementById('mvBanner')){
	mv.buildBanner = function(){
		var b = document.getElementById('mvBanner');
		var s = "";
		if(mv.isIOS===true){
			//
		}else{
			s+='<object id="ahaBanner" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" height="90" width="728">';
			s+='<param name="type" value="application/x-shockwave-flash" />';
			s+='<param name="name" value="ahaBanner" />';
			s+='<param name="quality" value="high" />';
			s+='<param name="movie" value="media/AHA728x90.swf" />';
			s+='<param name="flashvars" value="clickTAG=http://www.cnet.com" />';
			s+='<embed name="ahaBanner" src="media/AHA728x90.swf" quality="high" bgcolor="#ffffff" width="728" height="90" FlashVars="clickTAG=http://www.cnet.com" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />';
			s+='</object>';
		}
		b.innerHTML=s;
	}
	mv.buildBanner();
}

// IDENTIFY ALL JS DEPENDENT ELEMENTS TO DISPLAY
mv.jsEl=['jsCal'];
for(var x=0,y=mv.jsEl.length;x<y;x+=1){
	if(document.getElementById(mv.jsEl[x]))
		document.getElementById(mv.jsEl[x]).style.display="block";
}
	
// Float the Calendar to the right
if(document.getElementById("mvSubCol"))
	document.getElementById("mvSubCol").style.cssFloat="right";

// Lets do some dd (drop down) stuff

// Init dd vars
mv.dd={};
mv.dd.timeout=500;
mv.dd.closetimer=0;
mv.dd.curHov=null;
mv.dd.curA=null;

// pull all the anchor tags for the main drop down
mv.atags=document.getElementById("mvNavBar").getElementsByTagName("a");
// go through them and add mouseover event handlers to enable drop down functionality
for(var x=0,y=mv.atags.length;x<y;x+=1){
  if(mv.atags[x].className==="mainDrop"){
    mv.atags[x].addEventListener('mouseover', function() { hoverOn(this); }, false);
    mv.atags[x].addEventListener('mouseout', function() { hoverOff(); }, false);
	var d = mv.atags[x].parentNode.getElementsByTagName("div");
    d[0].addEventListener('mouseover', function() { ddHoverOn(this); }, false);
    d[0].addEventListener('mouseout', function() { hoverOff(this); }, false);
  }
}

function hoverOn(a){
	// if no hover make this the active hover
	if(mv.dd.curA===null){
		a.style.backgroundColor="#996633";
		var d = a.parentNode.getElementsByTagName("div");
		d[0].style.display="block";
		mv.dd.curA=a;
		mv.dd.curHov=d[0];
	// if this is the same hover turn timer off do nothing else
	}else if(a.isEqualNode(mv.dd.curA)){
		// cancel close timer
		closeHoverTimer();
	// Is this is not the current active hover, shut previous hover off, turn this one on
	}else{
		hoverClose();
		// cancel close timer
		closeHoverTimer();
		a.style.backgroundColor="#996633";
		var d = a.parentNode.getElementsByTagName("div");
		d[0].style.display="block";
		mv.dd.curA=a;
		mv.dd.curHov=d[0];
	}
}

function ddHoverOn(d){
	//Cancel Close timer
	if(mv.dd.closetimer){
		window.clearTimeout(mv.dd.closetimer);
		mv.dd.closetimer = null;
	}
}


function hoverOff(a){
	mv.dd.closetimer = window.setTimeout(hoverClose, mv.dd.timeout);
}

function hoverClose(){
	mv.dd.curA.style.backgroundColor="#663300";	
	mv.dd.curHov.style.display="none";
	mv.dd.curHov=null;
	mv.dd.curA=null;
}

function closeHoverTimer(){
	if(mv.dd.closetimer){
		window.clearTimeout(mv.dd.closetimer);
		mv.dd.closetimer = null;
	}
}