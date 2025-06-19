
const form = document.querySelector("#otp-form");
const inputs = document.querySelectorAll(".otp-input");
const verifyBtn = document.querySelector("#verify-btn");

const isAllInputFilled = () => {
  return Array.from(inputs).every((item) => item.value);
};

const getOtpText = () => {
  let text = "";
  inputs.forEach((input) => {
    text += input.value;
  });
  return text;
};


const toggleFilledClass = (field) => {
  if (field.value) {
    field.classList.add("filled");
  } else {
    field.classList.remove("filled");
  }
};

form.addEventListener("input", (e) => {
  const target = e.target;
  const value = target.value;
  console.log({ target, value });
  toggleFilledClass(target);
  if (target.nextElementSibling) {
    target.nextElementSibling.focus();
  }
  verifyOTP();
});

inputs.forEach((input, currentIndex) => {
  // fill check
  toggleFilledClass(input);

  // paste event
  input.addEventListener("paste", (e) => {
    e.preventDefault();
    const text = e.clipboardData.getData("text");
    console.log(text);
    inputs.forEach((item, index) => {
      if (index >= currentIndex && text[index - currentIndex]) {
        item.focus();
        item.value = text[index - currentIndex] || "";
        toggleFilledClass(item);
        verifyOTP();
      }
    });
  });

  // backspace event
  input.addEventListener("keydown", (e) => {
    if (e.keyCode === 8) {
      e.preventDefault();
      input.value = "";
      // console.log(input.value);
      toggleFilledClass(input);
      if (input.previousElementSibling) {
        input.previousElementSibling.focus();
      }
    } else {
      if (input.value && input.nextElementSibling) {
        input.nextElementSibling.focus();
      }
    }
  });
});




function verify_btn() {
    const entered_otp = getOtpText();
    let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

    if(entered_otp.length < 4){
      show_success('Please enter a valid otp',classType='warning')
      return;
    }
    
    $.ajax({
      url: '/validate_otp/',
      method: 'POST',
      data: {'otp': entered_otp,'csrfmiddlewaretoken': csrfmiddlewaretoken},
      success: function(response){
        window.location = response['path']
      },
      error: function(response){
        show_error(response.responseJSON['error'])
      }
    })
};


function update_neww_password(){
  const password = $("#password").val()
  const confirm_password = $("#confirm_password").val()
  if (password !== confirm_password) {
    show_error("New password and confirm password do not match.");
    return;
  }
  $.ajax({
    url: '/password_updated/',
    method: 'POST',
    data: {'password': password},
    success: function(response){
      show_success(response['message'])
    },
    error: function(response){
      show_error(response.responseJSON['error'])
    }
  })
}