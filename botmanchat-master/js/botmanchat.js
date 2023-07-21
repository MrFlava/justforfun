function switchDisplay(max_mobile_width) {
  if (max_mobile_width.matches) {
  	if (document.getElementById('header_v1').classList.contains('d-none') &&
  		  document.getElementById('body_v1').classList.contains('d-none') && 
  		  document.getElementById('footer').classList.contains('d-none'))
    {
  		document.getElementById('first_column').classList.add('d-none');
      document.getElementById('second_column').classList.remove('d-none');
  	}
  	else if (document.getElementById('header_v2').classList.contains('d-none') &&
            document.getElementById('body_v2').classList.contains('d-none'))
    {
        document.getElementById('first_column').classList.remove('d-none');
        document.getElementById('second_column').classList.add('d-none');
  	}
  } else {
  		document.getElementById('first_column').classList.remove('d-none');
  		document.getElementById('second_column').classList.remove('d-none');
  }
}

var max_mobile_width = window.matchMedia("(max-width: 576px)")
switchDisplay(max_mobile_width)
max_mobile_width.addListener(switchDisplay)

function dialogredirectMenu(){
  windowWidth = $(window).width();
  if (windowWidth <=575) {
  		document.getElementById('first_column').classList.remove('d-none');
  		document.getElementById('second_column').classList.add('d-none');
  		document.getElementById('header_v1').classList.remove('d-none');
  		document.getElementById('header_v2').classList.add('d-none');
  		document.getElementById('body_v1').classList.remove('d-none');
  		document.getElementById('body_v2').classList.add('d-none');
  		document.getElementById('footer').classList.remove('d-none');
  }
  else{
  		document.getElementById('header_v1').classList.remove('d-none');
  		document.getElementById('header_v2').classList.add('d-none');
  		document.getElementById('body_v1').classList.remove('d-none');
  		document.getElementById('body_v2').classList.add('d-none');
  		document.getElementById('footer').classList.remove('d-none');
  }
}

function closedialogMenu() {
  windowWidth = $(window).width(); 
  if (windowWidth <= 575) {
   	document.getElementById('first_column').classList.add('d-none');
    document.getElementById('header_v1').classList.add('d-none');
    document.getElementById('header_v2').classList.remove('d-none');
    document.getElementById('body_v1').classList.add('d-none');
    document.getElementById('body_v2').classList.remove('d-none');
    document.getElementById('footer').classList.add('d-none');
		document.getElementById('second_column').classList.remove('d-none');
  }
  else {
  		document.getElementById('header_v1').classList.add('d-none');
  		document.getElementById('header_v2').classList.remove('d-none');
  		document.getElementById('body_v1').classList.add('d-none');
  		document.getElementById('body_v2').classList.remove('d-none');
  		document.getElementById('footer').classList.add('d-none');
  }

 }
