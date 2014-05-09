/*
 * 
 * Author			:	Yogesh Kumar
 * Project			:	UNMP
 * Version			:	0.1
 * File Name		:	ccpl_utility.js
 * Creation Date	:	12-September-2011
 * Modify Date		:	15-September-2011
 * Purpose			:	Define All Required Javascript & jQuery Functions
 * Require Library	:	jquery 1.4 or higher version and jquery.validate 
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 * 
 * Copyright (c) 2011 Codescape Consultant Private Limited
 * 
 */


/*
 * This function add new validation to check the number should be less than the defined number.
 * 
 * Related With:
 * 				Number and Calculation
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check number must be less than the defined number.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							my_age:{
 * 									lessThan : "#min_age"
 * 							}
 * 					},
 * 					messages:{
 * 							my_age:{
 * 									lessThan : "Age should not less than 0"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("lessThan", function (value, element, param) {
    return parseInt($(param).val()) >= parseInt(value);
}, ' It show be less than the value');


/*
 * This function add new validation to check the number should be greater than the defined number.
 * 
 * Related With:
 * 				Number and Calculation
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check number must be greater than the defined number.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							my_age:{
 * 									greaterThan : "#min_age"
 * 							}
 * 					},
 * 					messages:{
 * 							my_age:{
 * 									greaterThan : "Age should not greater than 100"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("greaterThan", function (value, element, param) {
    return parseInt($(param).val()) <= parseInt(value);
}, ' It show be greater than the value');

/*
 * This function add new validation to check the number should be positive.
 * 
 * Related With:
 * 				Number and Calculation
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check number must be positive.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							my_age:{
 * 									positiveNumber : true
 * 							}
 * 					},
 * 					messages:{
 * 							my_age:{
 * 									positiveNumber : "Age should be a positive number"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("positiveNumber", function (value, element) {
    return Number(value) >= 0; // Number is a function that responsible for creating new instances of Number objects
}, ' Enter a positive number');

/*
 * This function add new validation to check the number should be negative.
 * 
 * Related With:
 * 				Number and Calculation
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check number must be nagative.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							temperature:{
 * 									nagativeNumber : true
 * 							}
 * 					},
 * 					messages:{
 * 							temperature:{
 * 									nagativeNumber : "Cold temperature should be in nagative"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("nagativeNumber", function (value, element) {
    return Number(value) < 0; // Number is a function that responsible for creating new instances of Number objects
}, ' Enter a nagative number');

/*
 * This function add new validation to check the maximum word length.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the maximum length of the word.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							first_name:{
 * 									maxWords : 20
 * 							}
 * 					},
 * 					messages:{
 * 							first_name:{
 * 									maxWords : "Please enter 20 words or less"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("maxWords", function (value, element, params) {
    return this.optional(element) || value.match(/\b\w+\b/g).length < params;
}, $.validator.format("Please enter {0} words or less."));

/*
 * This function add new validation to check the minimum word length.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the minimum length of the word.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							first_name:{
 * 									minWords : 5
 * 							}
 * 					},
 * 					messages:{
 * 							first_name:{
 * 									minWords : "Please enter at least 5 words"
 * 							}
 * 					}
 * 				});
 * 				
 */
// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("minWords", function (value, element, params) {
    return this.optional(element) || value.match(/\b\w+\b/g).length >= params;
}, $.validator.format("Please enter at least {0} words."));

/*
 * This function add new validation to check the mac address.
 * 
 * Related With:
 * 				Networking
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the mac address.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							mac_address:{
 * 									macAddress : true
 * 							}
 * 					},
 * 					messages:{
 * 							mac_address:{
 * 									macAddress : "Please enter valid MAC Address"
 * 							}
 * 					}
 * 				});
 * 				
 */
// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("macAddress", function (value, element) {
    return this.optional(element) || value.match("^([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}$|([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$|([0-9a-fA-F]{4}.){2}[0-9a-fA-F]{4}$");
//	return this.optional(element) || value.match("^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"); 
}, $.validator.format("Please enter valid MAC Address"));

/*
 * This function add new validation to check the ip address [IPv4].
 * 
 * Related With:
 * 				Networking
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the ip address [IPv4].
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							ip_address:{
 * 									ipv4Address : true
 * 							}
 * 					},
 * 					messages:{
 * 							ip_address:{
 * 									ipv4Address : "Please enter valid IP Address"
 * 							}
 * 					}
 * 				});
 * 				
 */
// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("ipv4Address", function (value, element) {
    return this.optional(element) || value.match("^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$");
}, $.validator.format("Please enter valid IP Address"));

/*
 * This function add new validation to check the ip address [IPv6].
 * 
 * Related With:
 * 				Networking
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the ip address [IPv6].
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							ip_address:{
 * 									ipv6Address : true
 * 							}
 * 					},
 * 					messages:{
 * 							ip_address:{
 * 									ipv6Address : "Please enter valid IP Address"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("ipv6Address", function (value, element) {
    return this.optional(element) || value.match(/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/);
}, $.validator.format("Please enter valid IP Address [IPv6]"));

/*
 * This function add new validation to no space allow.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check the character with no space.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							first_name:{
 * 									noSpace : true
 * 							}
 * 					},
 * 					messages:{
 * 							first_name:{
 * 									noSpace : "No space please and don't leave it empty"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("noSpace", function (value, element) {
    return value.indexOf(" ") < 0 && value != "";
}, "No space please and don't leave it empty");

/*
 * This function add new validation to allow only characters.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that allow only characters.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							first_name:{
 * 									alpha : true
 * 							}
 * 					},
 * 					messages:{
 * 							first_name:{
 * 									alpha : "Only Characters Allowed"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("alpha", function (value, element) {
    return this.optional(element) || value == value.match(/^[a-zA-Z._\n ]+$/);
}, "Only Characters Allowed.");

/*
 * This function add new validation that allow only characters & numbers.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that allow only characters & numbers.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							address:{
 * 									alphaNumeric : true
 * 							}
 * 					},
 * 					messages:{
 * 							address:{
 * 									alphaNumeric : "Only Characters & Numbers Allowed"
 * 							}
 * 					}
 * 				});
 * 				
 */

// jQuery validation library has a validation method which used to add custom validation with jQuery object.
$.validator.addMethod("alphaNumeric", function (value, element) {
    return this.optional(element) || value == value.match(/^[a-z0-9A-Z\n._ ]+$/);
}, "Only Characters & Numbers Allowed.");

/*
 * This function add new validation that check fields has to be different.
 * 
 * Related With:
 * 				String
 * 
 * Parameter:
 * 				None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				Add new validation that check fields has to be different.
 * 
 * How to Use:
 * 				$(#my_from_id).validate({
 *					rules: {
 * 							username:{
 * 									notEqualTo : "#other_username"
 * 							}
 * 					},
 * 					messages:{
 * 							username:{
 * 									notEqualTo : "Username has to be different"
 * 							}
 * 					}
 * 				});
 * 				
 */
jQuery.validator.addMethod("notEqualTo", function (value, element, param) {
    return this.optional(element) || value != $(param).val();
}, "This has to be different.");


jQuery.validator.addMethod('classCIPChecker', function (value, element) {
    return this.optional(element) || value.match("^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$");
}, 'Invalid Class C IP address');


/*
 * To Disable Key and Right Click 
 */
$.fn.DisableKeyAndRightClick = function () {
    return this.each(function () {
        $(this).bind("contextmenu", function (e) {
            e.preventDefault();
        });
        $(this).keydown(function (e) {
            return false;
        });
    });
};

//Checking the ipaddress octactes
//Type 1: (1-254).(0-255).(0-255).(1-254)System ip
//Type 2: (255).(0-255).(0-255).(0-255) Subnet mask
//Type 3: (0-254).(0-255).(0-255).(0-254) DNS IP -->
//
