$(document).ready(function(){
	var stripe = Stripe('pk_test_OEiMPBtf9FhQ7ZM6rsjjFwKa');
	var elements = stripe.elements();
	var cardElement = elements.create('card');
	cardElement.mount('#card-element');
});

