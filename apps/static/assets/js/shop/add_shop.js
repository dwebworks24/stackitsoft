function saveshopowner(){
    const clusteraera = $("#clusteraera").val();
    const first_name = $("#first_name").val();
    const last_name = $("#last_name").val();
    const email = $("#email").val();
    const phone = $("#phone").val();
    const shop_name = $("#shop_name").val();
    const shopType = $('#shop_type').val();
    const area = $("#area").val();
    const city = $("#city").val();
    const state = $("#state").val();
    const zip_code = $("#zip_code").val();
    // const rcbAgreement = $('input[name="rcb_agreement"]:checked').val();
   
  
      $.ajax({
        url: '/save_shop/',
        method: 'POST',
        data: {
          'clusteraera':clusteraera,
          'first_name':first_name,
          'last_name':last_name,
          'email':email,
          'phone':phone,
          'shop_name':shop_name,
          'shopType':shopType,
          'area':area,
          'city':city,
          'state':state,
          'zip_code':zip_code,
          'rcbAgreement':true,
        },
        success: function(response){
          show_success(response['message'])
          window.location = response['path']
        },
        error: function(response){
          show_error(response.responseJSON['error'])
        }
      })
  }


  $(document).ready(function() {
    // Initialize Select2 on the select element
    $('#clusteraera').select2();
   
  });  