
var total_entry = `
<tr>
    <td>   </td>
    <td>   </td>
    <td class="text-right"><h4><strong>Total: </strong></h4></td>
    <td class="text-center text-danger"><h4><strong>{0}</strong></h4></td>
</tr>

`
$(document).ready(function(){
	//var stripe = Stripe('pk_test_OEiMPBtf9FhQ7ZM6rsjjFwKa');
	var stripe = Stripe('pk_live_H3TAzRTFkl3SkgTY8EZqwgXw');
	var elements = stripe.elements();
	
	var style = {
	  base: {
	    color: '#32325d',
	    lineHeight: '18px',
	    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
	    fontSmoothing: 'antialiased',
	    fontSize: '16px',
	    '::placeholder': {
	      color: '#aab7c4'
	    }
	  },
	  invalid: {
	    color: '#fa755a',
	    iconColor: '#fa755a'
	  }
	};
	
	var card = elements.create('card', {style: style});
	
	card.addEventListener('change', function(event) {
	  var displayError = document.getElementById('card-errors');
	  if (event.error) {
	    displayError.textContent = event.error.message;
	  } else {
	    displayError.textContent = '';
	  }
	});
	
	function stripeTokenHandler(token) {
	  var wizard = document.getElementById('wizard');
	  var hiddenInput = document.createElement('input');
	  hiddenInput.setAttribute('type', 'hidden');
	  hiddenInput.setAttribute('name', 'stripeToken');
	  hiddenInput.setAttribute('value', token.id);
	  wizard.appendChild(hiddenInput);
	}

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
							<label for="student_dob_${student_num}">Date of Birth</label>
							<input id="student_dob_${student_num}" readOnly="readOnly" style="background: white;" placeholder="yyyy-mm-dd" class="form-control" name="dob_${student_num}" type="text" required>
						</div>
						<div class="form-holder">
							<input id="student_notes_${student_num}" name="notes_${student_num}" type="textarea" placeholder="Other Notes (optional)" class="form-control">
						</div>
					</div>
				`;
				student_list.push(student_form);
			    }

        		    $('#students').html(student_list.join("\n"));    

			    for (i=0; i < student_count; i++) {
				var student_num = i + 1;
			        $("#student_dob_" + student_num).datepicker({
					changeMonth: true,
					changeYear: true,
					dateFormat: "yy-mm-dd",
					yearRange: "-100:0",
					defaultDate: '2015-01-01'
				});
			    }
			}
		}

		if (currentIndex === 1){
   		        $('.class_forward').prop('disabled', true);
			$('#register_students').empty();
			let num_students = $('#student_count').val();
			let student_options = [];
			for(i=0; i < num_students; i++){
				let student_num = i + 1;

				let first_name_id = "#student_first_" + student_num;
				let first_name = $(first_name_id).val()

				let last_name_id = "#student_last_" + student_num;
				let last_name = $(last_name_id).val()

				let dob_id = "#student_dob_" + student_num;
				let dob = $(dob_id).val()
				
				let url = "/available_classes?dob=" + dob;

				let hrwidth = "40";
				if ( student_num == 1 ){
					hrwidth = "0";
				}
				if (dob != "") {
					$.get(url)
						.done( function(response){
							$('.selectHeader').html('Select Your Classes');
							var class_option_list = [];

							$.each(response, function(idx, dance_class) {
								let dance_id = dance_class["id"];
								let class_level = dance_class["level"];
								let dance_type = dance_class["dance_type"];
								let class_type = dance_class["class_type"];
								let class_day = dance_class["day"];
								let class_start = dance_class["start_time"];
								let class_end = dance_class["stop_time"];
								let day_start = dance_class["start_day"];
								let day_end = dance_class["end_day"];
								let description = dance_class["description"];
								let student_options = "";
								console.log(dance_class["class_type"]);

								if (dance_class["dance_type"] == "Dance") {
									student_options = `<option value="${dance_id}">${class_level} ${class_type} (${description}) ${day_start} - ${day_end} on ${class_day
									} from ${class_start} - ${class_end}</option>`;
								} else {
									student_options = `<option value="${dance_id}">${class_level} ${dance_type} ${class_type} on ${class_day} @ ${class_start}</option>`;
								}

								let title = "Select a Class";
								class_option_list.push(student_options);
							});
							let class_selections = class_option_list.join("\n");
							let title = "Select a Class";
							if (response.length == 0){
								title = "No Classes Available";
							}
								
							let student_template = `<div class="form-row">
											<h6>${first_name}'s Classes:</h6>
										</div>
										<div class="form-row">
											<select data-width="95%" title="${title}" name="student_class_${student_num}" class="selectpicker" id="student_classes_${student_num}" multiple data-selected-text-format="static" required>
												${class_selections}
											</select>
	    									</div>
										<hr style="width:${hrwidth}%">
							`


							$('#register_students').append(`${student_template}`);

							$('#student_classes_' + student_num).selectpicker('render');
   		        				$('.class_forward').prop('disabled', false);
						})
						.fail(function(jqXHR, textStatus, errorThrown) {
							$('.selectHeader').html("There was an error with the date submitted. Please go back and check that it's in the right format.");
						});
					
				}
			}
		}

		if (currentIndex === 3) {
			card.mount('#card-element');
			$('#purchase_items').empty();
			let num_students = Number($("#student_count").val());
			let payload = {};
			for (i=0; i < num_students; i++){
				let student_num = i + 1;
				let selected_vals = $('#student_classes_' + student_num).val();
				let first_name_id = "#student_first_" + student_num;
				let first_name = $(first_name_id).val();
				payload[first_name] = selected_vals;
			}
			let url = "/register_payments?payload=" + JSON.stringify(payload)
			$.get(url, function(response) {
				let fees = response["fees"];
				for (i=0; i < fees.length; i++){
					let fee = fees[i];
					let payment_entry = `
					 <tr>
					    <td>${fee['title']}</td>
					    <td> ${fee['description']} </td>
					    <td class="text-center">$${fee['price']}</td>
					</tr>`
					$('#purchase_items').append(payment_entry);
				}

				let classes = response["classes"];
				for (i=0; i < classes.length; i++){
					let myclass = classes[i];
					var description = "";
					if (myclass['payment_frequency'] == 'each month'){
						description = "First month's tuition.";
					} else {
						description = "One-time payment.";
					}

					let class_title = "";
					if (myclass['type'] == "Dance"){
						class_title = `${myclass['name']}'s ${myclass['level']} ${myclass['type']} (${myclass['description']}): ${myclass['start_day']} - ${myclass['end_day']} on ${myclass['day']} @ ${myclass['start_time']} - ${myclass['stop_time']}`;
					} else {
						class_title = `${myclass['name']}'s ${myclass['level']} ${myclass['type']} ${myclass['class_type']} on ${myclass['day']} @ ${myclass['start_time']} - ${myclass['stop_time']}`;

					}

					let payment_entry = `
					 <tr>
					    <td> ${class_title} </td>
					    <td> ${description} </td>
					    <td class="text-center">$${myclass['price']}</td>
					</tr>`
					$('#purchase_items').append(payment_entry);
				}

				let total_entry = `
					<tr>
					    <td>   </td>
					    <td class="text-right"><h4><strong>Total: </strong></h4></td>
					    <td class="text-center text-success"><h4><strong>$${response['total']['price']}</strong></h4></td>
					    <input type="hidden" value=${response['total']['price']} name="total">
					</tr>`

				$('#purchase_items').append(total_entry);


			})

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
		stripe.createToken(card).then(function(result) {
			if (result.error) {
			    	var errorElement = document.getElementById('card-errors');
				errorElement.textContent = result.error.message;
			}
			else {
				stripeTokenHandler(result.token);
				confirmation = confirm("Confirm transaction by pressing OK.");
				if (confirmation == true) {
					$(".finish").attr("disabled", true);	
					$(".finish").html("Processing...");
					document.getElementById("wizard").submit();
				}
			}
		})
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
    $('.finish').click(function(){
	$("#wizard").steps('finish');
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
	$(".main-menu").slicknav({
        appendTo: '.header-section',
		allowParentLinks: true,
		closedSymbol: '<i class="fa fa-angle-right"></i>',
		openedSymbol: '<i class="fa fa-angle-down"></i>'
	});

});

