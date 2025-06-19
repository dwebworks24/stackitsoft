$(document).ready(function() {
    // Initialize Select2 on the select element
    $('#Select2').select2();
    $('#cluster_aera').select2();
    $('#waste_type_select2').select2();
   
  });

// sum_of_tot_amount = 0
  function cluster_aera_shop_list(){
    var clusterAreaId =  $("#cluster_aera :selected").val();
    $.ajax({
        url: '/get_shop_list/',
        data: {
            'cluster_area_id': clusterAreaId
        },
        success: function (response) {
          $('#Select2').html(null);
          let $option = `<option value="">All</option>`;
          let shops = JSON.parse(response['shops']);  // Parse the JSON string

          $.each(shops, function(index, value){
              $option += `<option value="${value.pk}">${value.fields.user} | ${value.fields.shop_name}</option>`;
          });
          $('#Select2').html($option);
          $('#Select2').select2({width: '100%'});
      },
      error: function(response){
        show_error(response.responseJSON['message']);
    }
    });
  }
  
  var counter = 2;

  function addProductField() {
    var waste_obj = $('#waste_obj').val();
    var waste_list = JSON.parse(waste_obj);
    var container = document.getElementById("dynamicFieldsContainer");
  
    var newRow = document.createElement("div");
    newRow.className = "row mt-3";
    newRow.id = "row_" + counter;
  
    var materialId = "wast_id_" + counter;
    var materialPrice = "price_" + counter;
    var materialQuantity = "quantity_" + counter;
    var materialTotal = "total_" + counter; 
  
    newRow.innerHTML = `
      <div class="col-sm-12 col-md-6 col-lg-3">
        <label for="${materialId}" class="form-label">Waste Type</label>
        <select class="form-select" id="${materialId}" name="${materialId}" aria-label="Waste type select">
          <option selected>Open this select menu</option>
        </select>
      </div>
      <div class="col-sm-12 col-md-6 col-lg-2">
        <label for="${materialQuantity}" class="form-label">Quantity</label>
        <input type="text" class="form-control" id="${materialQuantity}" name="${materialQuantity}" placeholder="Please enter quantity" aria-label="Quantity" autocomplete="off">
      </div>
      <div class="col-sm-12 col-md-3 col-lg-2">
        <label for="${materialPrice}" class="form-label">Price</label>
        <input type="text" class="form-control" id="${materialPrice}" name="${materialPrice}" placeholder="Please enter price" aria-label="Price" autocomplete="off">
      </div>
      <div class="col-sm-12 col-md-3 col-lg-2">
        <label for="${materialTotal}" class="form-label">Total Price</label>
        <input type="text" class="form-control" id="${materialTotal}" name="${materialTotal}" readonly>
      </div>
      <div class="col-sm-12 col-md-6 col-lg-3 my-auto">
        <button type="button" class="btn btn-primary mt-4" onclick="addProductField()">+ADD</button>
        <button type="button" class="btn btn-danger mt-4" onclick="removeProductField('row_${counter}')">-REMOVE</button>
      </div>
    `;
  
    container.appendChild(newRow);
  
    // Populate the new select element with waste list
    var selectElement = document.getElementById(materialId);
    waste_list.forEach(function(material) {
        var option = document.createElement("option");
        option.text = material.fields.wastename;
        option.value = material.pk;
        selectElement.appendChild(option);
    });
  
    // Initialize Select2 on the newly created select element
    $(document).ready(function() {
      $('#materialId').select2({
          placeholder: "Select Material",
          theme: "bootstrap5",
          width: "100%" 
      });
    })
  
    // Add event listeners to quantity and price to calculate the total
    document.getElementById(materialQuantity).addEventListener('input', function() {
      calculateRowTotal(materialQuantity, materialPrice, materialTotal);
    });
  
    document.getElementById(materialPrice).addEventListener('input', function() {
      calculateRowTotal(materialQuantity, materialPrice, materialTotal);
    });
  
    counter++;
  }
  

//  static code 
  function calculateTotal() {
    const quantity = parseFloat(document.getElementById('quantity_1').value) || 0;
    const price = parseFloat(document.getElementById('price_1').value) || 0;
    const total = price * quantity;
  
    document.getElementById('total_price_1').value = total.toFixed(2);
    updateTotalAmount();
    // sum_of_tot_amount += parseFloat(total.toFixed(2));
    // document.getElementById("total_amount").value = sum_of_tot_amount;
  
  }
  
  document.getElementById('quantity_1').addEventListener('input', calculateTotal);
  document.getElementById('price_1').addEventListener('input', calculateTotal);
  
  
  
// dyanamic Function to calculate total price for each row
  function calculateRowTotal(quantityId, priceId, totalId) {
    var quantity = parseFloat(document.getElementById(quantityId).value) || 0;
    var price = parseFloat(document.getElementById(priceId).value) || 0;
    var total = quantity * price;
    
    document.getElementById(totalId).value = total.toFixed(2); 
    updateTotalAmount();
    // sum_of_tot_amount += parseFloat(total.toFixed(2));
    // document.getElementById("total_amount").value = sum_of_tot_amount;
  }
  
  function removeProductField(rowId) {
    var row = document.getElementById(rowId);
    if (row) {
        row.parentNode.removeChild(row);
        updateTotalAmount(); // Update total after removal
    }
    // var row = document.getElementById(rowId);
    // row.parentNode.removeChild(row);
  }
  

function removeProductField(rowId) {
  var row = document.getElementById(rowId);
    if (row) {
        row.parentNode.removeChild(row);
        updateTotalAmount(); // Update total after removal
    }
  // var row = document.getElementById(rowId);
  // row.parentNode.removeChild(row);
}

function updateTotalAmount() {
  let totalAmount = 0;

  // Add the static total price
  totalAmount += parseFloat(document.getElementById("total_price_1").value) || 0;

  // Add the dynamic row totals (if there are any)
  for (let i = 2; i < counter; i++) {
      let rowTotal = parseFloat(document.getElementById("total_" + i)?.value || 0);
      totalAmount += rowTotal;
  }

  // Set the cumulative total in the total_amount field
  document.getElementById("total_amount").value = totalAmount.toFixed(2);
}




function save_trnscation(){
    const cluster_aera = $("#cluster_aera :selected").val();
    const owner = $("#Select2 :selected").val();
    const paid_amount = $("#paid_amount").val();
    const given_bags = $('input[name="gridRadios"]:checked').val();
    const lifted_status = $('input[name="gridRadios1"]:checked').val();
    const waste_type = $("#waste_type_select2 :selected").val();
    const startprice = $("#price_1").val();
    const startquantity = $("#quantity_1").val();
  
  
    var wasteData = [];
    wasteData.push({
        wasteType: waste_type,
        price: startprice,
        quantity: startquantity
    })
    for (var i = 1; i < counter; i++) {
        if (document.getElementById(`wast_id_${i}`)) {
            var wasteType = $(`#wast_id_${i} :selected`).val();
            var price = $(`#price_${i}`).val();
            var quantity = $(`#quantity_${i}`).val();
            
            if (wasteType && price && quantity) {
                wasteData.push({
                    wasteType: wasteType,
                    price: price,
                    quantity: quantity
                });
            }
        }
    }
 
    $.ajax({
      url: '/save_transaction_data/',
      method: 'POST',
      data: {
        'owner':owner,
        'cluster_aera':cluster_aera,
        'paid_amount':paid_amount,
        'given_bags':given_bags,
        'lifted_status':lifted_status,
        'wasteData':wasteData
    
        
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



  function fetchDataAndPopulateTable(id) {
    const material_id = id;
    $.ajax({
        url: '/get_materials_list/' + material_id + '/',
        method: 'GET',
        success: function(response) {
            console.log(response);

            if (response.materials && Array.isArray(response.materials)) {

                $('#materialtable tbody').empty();
                let totalAmount = 0;  
                // Populate the table with the new data
                response.materials.forEach(function(item) {
                  const amount = item.price * item.quantity;
                    totalAmount += amount; 
                    let row = '<tr data-id="1" style="cursor: pointer;">' +
                                '<td data-field="item.id" style="width: 107.26px;">' + item.id + '</td>' +
                                '<td data-field="id" style="width: 107.26px;">' + item.waste_type__wastename + '</td>' +
                                '<td data-field="name" style="width: 417.708px;">' + item.price + '</td>' +
                                '<td data-field="age" style="width: 167.438px;">' + item.quantity + '</td>' +
                                '<td data-field="gender" style="width: 184.385px;">' +'₹'+ (item.price * item.quantity)+ '</td>' +
                              '</tr>';
                    $('#materialtable tbody').append(row);
                });
                $('#totalAmount').text('₹' + totalAmount);
            } else {
                console.error('Invalid response format:', response);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error fetching data:', error);
        }
    });
}


