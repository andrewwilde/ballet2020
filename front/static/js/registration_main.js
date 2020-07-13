$(function(){
	form = $("#wizard").show();
	form.steps({
	    headerTag: "h2",
	    bodyTag: "section",
	    transitionEffect: "fade",
            transitionEffectSpeed: 500,
	    labels: {
            	finish: "Submit",
            	next: "Forward",
            	previous: "Backward"
            },

	    onStepChanging: function (event, currentIndex, newIndex)
	    {
	        // Allways allow previous action even if the current form is not valid!
	        if (currentIndex > newIndex)
	        {
	            return true;
	        }
	        // Forbid next action on "Warning" step if the user is to young
	        if (currentIndex === 0){
			$('#register_students').empty();
			console.log("I have just emptied all student class selections.");
		    	if (Number($("#student_count").val()) < 1){
	            		return false;
		    	}
			else{
			    var student_count = $("#student_count").val();
			    student_list = [];		
			    for (i=0; i < student_count; i++){
				var student_num = i + 1;
				var student_form = `
					<div class="form-row">
						<h4>Student #${student_num} </h4>
					</div>
					<div class="form-row">
						<div class="form-holder">
							<input id="student_first_${student_num}" name="first_name_${student_num}" type="text" placeholder="First Name" class="form-control" required>
						</div>
						<div class="form-holder">
							<input id="student_last_${student_num}" name="last_name_${student_num}" type="text" placeholder="Last Name" class="form-control" required>
						</div>
					</div>
					<div class="form-row">
						<div class="form-holder">
							<input id="student_dob_${student_num}" name="dob_${student_num}" type="date" placeholder="Date of Birth" value="" onChange="this.setAttribute('value', this.value)" class="form-control" required>
						</div>
						<div class="form-holder">
							<input id="student_notes_${student_num}" name="notes_${student_num}" type="textarea" placeholder="Other Notes (optional)" class="form-control">
						</div>
					</div>
				`;
				student_list.push(student_form);
			    }

        		    $('#students').html(student_list.join("\n"));    
			}
		}

		if (currentIndex === 1){
			$('#register_students').empty();
			console.log("I have emptied all student selects.");
			let num_students = $('#student_count').val();
			let student_options = [];
			console.log("I have this many students: " + num_students);
			for(i=0; i < num_students; i++){
				let student_num = i + 1;

				let first_name_id = "#student_first_" + student_num;
				let first_name = $(first_name_id).val()

				let last_name_id = "#student_last_" + student_num;
				let last_name = $(last_name_id).val()

				let dob_id = "#student_dob_" + student_num;
				let dob = $(dob_id).val()
				
				let url = "/available_classes?dob=" + dob;
				if (dob != "") {
					$.get(url, function(response){
						var class_option_list = [];

						$.each(response, function(idx, dance_class) {
							let dance_id = dance_class["id"];
							let class_level = dance_class["level"];
							let class_type = dance_class["dance_type"];
							let class_day = dance_class["day"];
							let class_start = dance_class["start_time"];
							let student_options = `<option value="${dance_id}">${class_level} ${class_type} on ${class_day} @ ${class_start}</option>`
							class_option_list.push(student_options);
						});
						let class_selections = class_option_list.join('\n')
						let student_template = `<div class="form-row">
										<select style="100%" name="student_class_${student_num}" class="selectpicker" id="student_classes_${student_num}" multiple required>
											${class_selections}
										</select>
	    								</div>
						`
						$('#register_students').append(`${student_template}`);
						console.log("I have just added a new student: " + student_template);

						$('#student_classes_' + student_num).selectpicker('render');
						console.log("Rendering #student_classes_" + student_num);
					});
				}
			}
		}
	        // Needed in some cases if the user went back (clean up)
	        if (currentIndex < newIndex)
	        {
	            // To remove error styles
	            form.find(".body:eq(" + newIndex + ") label.error").remove();
	            form.find(".body:eq(" + newIndex + ") .error").removeClass("error");
	        }
	        form.validate().settings.ignore = ":disabled,:hidden";
	        return form.valid();
	    },
	    onFinishing: function (event, currentIndex)
	    {
	        form.validate().settings.ignore = ":disabled";
	        return form.valid();
	    },
	    onFinished: function (event, currentIndex)
	    {
	        alert("Submitted!");
	    }
	}).validate({
    		errorPlacement: function errorPlacement(error, element) { element.before(error); }
	});

    $('.wizard > .steps li a').click(function(){
    	$(this).parent().addClass('checked');
		$(this).parent().prevAll().addClass('checked');
		$(this).parent().nextAll().removeClass('checked');
    });
    // Custome Jquery Step Button
    $('.forward').click(function(){
    	$("#wizard").steps('next');
    })
    $('.backward').click(function(){
        $("#wizard").steps('previous');
    })
    // Select Dropdown
    $('html').click(function() {
        $('.select .dropdown').hide(); 
    });
    $('.select').click(function(event){
        event.stopPropagation();
    });
    $('.select .select-control').click(function(){
        $(this).parent().next().toggle();
    })    
    $('.select .dropdown li').click(function(){
        $(this).parent().toggle();
        var text = $(this).attr('rel');
        $(this).parent().prev().find('div').text(text);
    })
    $('ul[role="tablist"]').hide();	
    $('.actions').hide();	
    $('#student_count').change(function(){
	var student_count = $('#student_count').val();
	var rounded_down = Math.floor(student_count);
        $('#student_count').val(rounded_down);	
    });
});

