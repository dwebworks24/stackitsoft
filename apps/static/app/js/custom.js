function loginfunc() {
    const employee_id = document.getElementById('employeeId').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!employee_id || !email || !password) {
      document.getElementById('loginMessage').textContent = 'Please enter all details.';
      return;
    }

    const data = {
      employee_id: employee_id,
      email: email,
      password: password
    };

    $.ajax({
      url: '/login/',
      type: "POST",
      data: data,
      headers: { 'X-CSRFToken': '{{ csrf_token }}' },
      success: function (response) {
        if (response.status === 'success') {
          $('#loginMessage')
            .removeClass('text-danger')
            .addClass('text-success')
            .text(response.message);

          document.getElementById('loginForm').reset();

          setTimeout(() => {
            window.location.href = response.redirect_url;
          }, 1000);
        } else {
          $('#loginMessage')
            .removeClass('text-success')
            .addClass('text-danger')
            .text(response.message);
        }
      },
      error: function () {
        $('#loginMessage')
          .removeClass('text-success')
          .addClass('text-danger')
          .text('An unexpected error occurred.');
      }
    });
  }