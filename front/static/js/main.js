'use strict';

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(window).on('load', function() {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(100).fadeOut("slow");

});

(function($) {
	/*------------------
		Navigation
	--------------------*/
	$(".main-menu").slicknav({
        appendTo: '.header-section',
		allowParentLinks: true,
		closedSymbol: '<i class="fa fa-angle-right"></i>',
		openedSymbol: '<i class="fa fa-angle-down"></i>'
	});
	
	/*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function() {
		var bg = $(this).data('setbg');
		$(this).css('background-image', 'url(' + bg + ')');
	});


	/*------------------
		Back to top
	--------------------*/
	$(window).scroll(function() {
		if ($(this).scrollTop() >= 500) {
			$('.back-to-top').fadeIn();
			$('.back-to-top').css('display','flex');
		} else {
			$('.back-to-top').fadeOut();
		}
	});

	$(".back-to-top").click(function() {
		$("html, body").animate({scrollTop: 0}, 1000);
	 });



	/*------------------
		Hero Slider
	--------------------*/
	$('.hero-slider').owlCarousel({
		loop: true,
		nav: false,
		dots: true,
		mouseDrag: false,
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		items: 1,
		autoplay: true,
		autoplayTimeout: 2000,
		smartSpeed: 500,
		autoplayHoverPause: true,
	});

	/*------------------
		Review Slider
	--------------------*/
	$('.review-slider').owlCarousel({
		loop: true,
		nav: false,
		dots: true,
		items: 1,
		autoplayHoverPause: true,
		autoplay: true
	});

	/*------------------
		Classes Slider
	--------------------*/
	$('.classes-slider').owlCarousel({
		loop: true,
		nav: false,
		dots: true,
		margin: 30,
		autoplay: true,
		autoplayTimeout: 4000,
		autoplayHoverPause: true,
		responsive : {
			0 : {
				items: 1
			},
			768 : {
				items: 2
			},
			1170 : {
				items: 3,
			}
		},
	});

	/*------------------
		Trainer Slider
	--------------------*/
	$('.trainer-slider').owlCarousel({
		loop: true,
		nav: true,
		dots: false,
		navText:[' ',' '],
		autoplay: true,
		autoplayTimeout: 4000,
		autoplayHoverPause: true,
		responsive : {
			0 : {
				items: 1
			},
			768 : {
				items: 1
			},
			992 : {
				items: 2,
			}
		},
	});

	/*------------------
		Gallery Slider
	--------------------*/
	$('.gallery-slider').owlCarousel({
		loop: true,
		nav: false,
		dots: false,
		items: 6,
		autoplayHoverPause: true,
		responsive : {
			0 : {
				items: 2
			},
			475 : {
				items: 3
			},
			768 : {
				items: 4,
			},
			992 : {
				items: 6,
			}
		},
	});
})(jQuery);
