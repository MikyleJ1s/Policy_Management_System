
function validate_new_credentials() {
      alert("Your Credentials have been Updated :)");
      return true;
}

function update_button_logic() {
  var x = document.forms["update_form"]["new_username"].value;
  var y = document.forms["update_form"]["new_password"].value;
  if (x == "" || x == null ||y == ""|| y == null) { 
           document.getElementById('updating_button').disabled = true; 
             return true;
       } else { 
           document.getElementById('updating_button').disabled = false;
           return false;
       }

   }

function validate_payment() {
      alert("You made a Successful Payment :)");
      return true;
}

function button_logic() {
  var account = document.forms["payment_form"]["account_number"].value;
  var expiry = document.forms["payment_form"]["expiry_date"].value;
  var cvv = document.forms["payment_form"]["cvv"].value;
  var amount = document.forms["payment_form"]["amount_paid"].value;
  if (amount == "" || amount == null ||expiry == ""|| expiry == null || account == "" || account == null || cvv == "" || cvv == null) { 
           document.getElementById('pay_button').disabled = true; 
             return true;
       } else { 
           document.getElementById('pay_button').disabled = false;
           return false;
       }

   }
