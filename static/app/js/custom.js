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

 document.getElementById("manual-close-btn").addEventListener("click", function () {
    const modalElement = document.getElementById("editMarketModal");
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    
    // Fallback: if modal is not already instantiated
    const modal = modalInstance || new bootstrap.Modal(modalElement);
    modal.hide();
  });


  function submitEditForm() {
    const formData = {
      id: document.getElementById('edit-id').value,
      name: document.getElementById('edit-name').value,
      unit: document.getElementById('edit-unit').value
    };

    // Get hourly prices
    for (let hour = 2; hour <= 11; hour++) {
      const field = document.getElementById(`edit-price_${hour}pm`);
      formData[`price_${hour}pm`] = field ? field.value : '';
    }

    $.ajax({
        url: '/update-market/', 
        type: 'POST',
        data: formData,
          headers: { 'X-CSRFToken': '{{ csrf_token }}' },
        success: function (response) {
          alert('Market updated successfully!');
          $('#editMarketModal').modal('hide');
          location.reload(); 
        },
        error: function (xhr, status, error) {
          console.error('Error:', error);
          alert('Something went wrong while updating.');
        }
      });
  }