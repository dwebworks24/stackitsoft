

function show_success(message, classType = 'success') {
    swal({  
        text: message,  
        icon: "success",  
        button: "ok",  
      });  
    
}

function show_error(message) {
    swal({  
        text: message,  
        icon: "error",  
        button: "ok",  
      });    
}



function show_msg_callback(message, classType = 'success', callback) {
    swal({ text: message, icon: classType }).then((result) => callback());
}

function confirm_dialog(title, message, callback, cancelText = 'No', confirmText = 'Yes', buttonTitle = null) {
    swal({
                title: title,
                text: message,
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                cancelButtonText: cancelText,
                confirmButtonText: confirmText,
                reverseButtons: true
        }).then((result) => {
                if (result.isConfirmed) {
                        callback(buttonTitle)
                }
        });
}
