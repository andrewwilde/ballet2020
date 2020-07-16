
$(".cf-radio").change(function() {
	filter_classes();	
});

$(".circle-select").change(function() {
	filter_classes();
});

function post_data(url, data, httpCallback){

	$.post( url, data, function(response){ 
		httpCallback(response);
	});
}

function filter_classes(){
	data = {
		'Mon': $("input[name='Mon']:checked").val(),
		'Tue': $("input[name='Tue']:checked").val(),
		'Wed': $("input[name='Wed']:checked").val(),
		'Thu': $("input[name='Thu']:checked").val(),
		'Fri': $("input[name='Fri']:checked").val(),
		'Sat': $("input[name='Sat']:checked").val(),
		'age': $("#age :selected").val(),
		'type': $("#type :selected").val()
	}

	post_data("/filter_classes/", data, update_classes);
}

function update_classes(response) {
	var rendered_classes = [];
	$.each(response, function(idx, dance_class) {
		let template_vars = {
			image: dance_class['image'],
			class_level: dance_class['level'],
			class_type: dance_class['dance_type'],
			class_day: dance_class['day'],
			class_start: dance_class['start_time'],
			class_stop: dance_class['stop_time'],
			class_min: dance_class['min_age'],
			class_max: dance_class['max_age'],
			teacher_image: "",
			teacher_first: "",
			teacher_last: "",
			teacher_title: ""
		};
		let {image, class_level, class_type, class_day, class_start, class_stop, class_min, class_max, teacher_image, teacher_first, teacher_last, teacher_title} = template_vars;

		var class_template = `
<div class="col-md-6">
	<div class="classes-item-warp">
		<div class="classes-item">
			<div class="ci-img">
				<img src="${image}" alt="">
			</div>
			<div class="ci-text">
				<h4>${class_level} ${class_type}</h4>
				<div class="ci-metas">
					<div class="ci-meta"><i class="material-icons">event_available</i>${class_day}</div>
					<div class="ci-meta"><i class="material-icons">alarm_on</i>${class_start} - ${class_stop}</div>
				</div>
				<p>Ages ${class_min} - ${class_max}</p>
			</div>
			<div class="ci-bottom">
				<div class="ci-author">
					<img src="${teacher_image}" alt="">
					<div class="author-text">
						<h6>${teacher_first} ${teacher_last}</h6>
						<p>${teacher_title}</p>
					</div>
				</div>
				<a href="" class="site-btn sb-gradient">register</a>
			</div>
		</div>
	</div>
</div>	
`
	rendered_classes.push(class_template);	
	});

	if (rendered_classes.length == 0) {
		$("#dance_classes").html("");
		$("#class_title").html("No Available Classes with Filtered Items!");
	}
	else {
		$("#dance_classes").html(rendered_classes.join('\n'));	
	}
}

function populate_classes(response){
	var classes_templates = [];
	$.each(response, function(title, classes) {
		var level_classes = [];
		$.each(classes, function(idx, dance_class) {
			let template_vars = {
				start_time: dance_class['start_time'],
				stop_time: dance_class['stop_time'],
				day: dance_class['day']
			};
			let {day, start_time, stop_time, age_min, age_max} = template_vars;
			var class_template = `<div class="ci-metas"><div class="ci-meta"><h6>${day} @ ${start_time} - ${stop_time}</h6></div></div>`
			level_classes.push(class_template);
		});

		let template_vars = {
			image: classes[0]['image'],
			ages: classes[0]['age_range'],
			times: level_classes.join('\n'),
			age_min: classes[0]['min_age'],
			age_max: classes[0]['max_age'],
			price: classes[0]['price']
		}
		let {image, ages, times, age_min, age_max, price} = template_vars;

		var class_template = `
<div class="classes-item">
	<div class="ci-img">
		<img src="${image}" alt="">
	</div>
	<div class="ci-text">
		<h4>${title}</h4>
		<h6 style="margin-bottom:15px">$${price}/month</h6>
		${times}
	</div>
	<div class="ci-bottom">
		<div class="ci-author">
			<div class="author-text">
				<h6>Ages ${age_min} - ${age_max}</h6>
			</div>
		</div>
		<a href="/register" class="site-btn sb-gradient">register</a>
	</div>
</div>
`
		classes_templates.push(class_template);
	});

	$('.classes-slider').trigger('destroy.owl.carousel');
	$('.classes-slider').html(classes_templates.join('\n'));
	$('.classes-slider').owlCarousel({
		loop: true,
		nav: true,
		dots: false,
		margin: 30,
		navText: [' ', ' '],
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
}

function get_classes_by_category(){
	url = "/class_levels/"
	$.get( url, function(response){ 
		populate_classes(response);
	});
}
