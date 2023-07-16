// Yes/No Modal
document.body.innerHTML += '<!-- Yes/No Modal -->\
<div class="modal fade" id="yesNoModal" tabindex="-1" role="dialog" aria-labelledby="yesNoModalLabel" aria-hidden="true">\
  <div class="modal-dialog" role="document">\
	<div class="modal-content">\
	  <div class="modal-header">\
		<p class="modal-title" id="yesNoModalLabel">Are you sure?</p>\
	  </div>\
	  <div class="modal-footer">\
		<button type="button" style="text-align: center;font-size: 16px;" class="btn btn-secondary" onclick="cancelModal(\'#yesNoModal\', \'\', \'\');">No</button>\
		<button id="yesNoOnClick" type="button" style="margin-right:10px;text-align: center;font-size: 16px;" class="btn btn-primary" onclick="">Yes</button>\
	  </div>\
	</div>\
  </div>\
</div>\
<!-- Yes/No Modal -->'


// Stock Modal
document.body.innerHTML += '<!-- Password Modal -->\
<div class="modal fade" id="addRowModal" tabindex="-1" role="dialog" aria-labelledby="addRowModalLabel" aria-hidden="true">\
  <div class="modal-dialog" role="document">\
	<div class="modal-content">\
	  <div class="modal-header">\
		<p class="modal-title" id="addRowModalLabel">Add Stock</p>\
	  </div>\
	  <div class="modal-body">\
		<form>\
		  <div class="form-group">\
			<label for="stock-text" class="col-form-label">Stock:</label>\
			<input class="form-control" id="stock-text" style="height: 40px; font-size: 18px;text-transform:uppercase">\
			<label for="stop-loss-text" class="col-form-label">stop-loss:</label>\
			<input class="form-control" id="stop-loss-text" style="height: 40px; font-size: 18px;" value="0">\
		  </div>\
		</form>\
	  </div>\
	  <div class="modal-footer">\
		<button type="button" style="text-align: center;font-size: 16px;" class="btn btn-secondary" onclick="cancelModal(\'#addRowModal\', \'stock-text\', \'stop-loss-text\');">Cancel</button>\
		<button type="button" style="margin-right:10px;text-align: center;font-size: 16px;" class="btn btn-primary" onclick="addRowAndStore(document.getElementById(\'stock-text\').value, document.getElementById(\'stop-loss-text\').value);">Submit</button>\
	  </div>\
	</div>\
  </div>\
</div>\
<!-- Password Modal -->'



// Adding submit event for "Go" keyboard button
document.getElementById("addRowModal").addEventListener("submit", function(event) {
    event.preventDefault();
    addRow(document.getElementById('stock-text').value, document.getElementById('stop-loss-text').value);
});


$('#addRowModal').on('shown.bs.modal', function() {
    $('#stock-text').focus();
})



function addRowAndStore(stock, stop_loss) {
  if (stock == "" || stop_loss == "") {
	  showToast("Empty text is NOT allowed!");
	  return;
  }
	  
  stock = stock.toUpperCase();
  if (isNaN(Number(stop_loss))) {
	  showToast("stop_loss MUST be a numerical value!");
	  return;
  }
	  
  if (typeof android !== 'undefined') {
	  android.storeData(stock, stop_loss);
  }
	
  addRow(stock, stop_loss);
  cancelModal('#addRowModal', 'stock-text', 'stop-loss-text');
}

function addRow(stock, stop_loss) {
  if (stock == "" || stop_loss == "") {
	  showToast("Empty text is NOT allowed!");
	  return;
  }
	
  stock = stock.toUpperCase();
  if (isNaN(Number(stop_loss))) {
	  showToast("stop_loss MUST be a numerical value!");
	  return;
  }
	
  var rowCount = $("#myTable tr").length;	
  for (let i = 0; i < rowCount; i++) {
	if (document.getElementById("myTable").rows[i].cells[0].innerHTML == stock) {
		showToast("Stock already exist!");
		return;
    }
  }	
  
  var table = document.getElementById("myTable");
  var row = table.insertRow(rowCount);
  row.className = "success";
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = stock;
  cell2.innerHTML = stop_loss;
  cell3.innerHTML = "<button type=\"button\" class=\"btn btn-danger\" onclick=\"showRemoveRowModal('" + stock + "');\">-</button>";
}

function showRemoveRowModal(stock) {
	document.getElementById('yesNoOnClick').onclick = function() {
		var rowNum = -1;
		var rowCount = $("#myTable tr").length;
		for (let i = 0; i < rowCount; i++) {
			if (document.getElementById("myTable").rows[i].cells[0].innerHTML == stock) {
				rowNum = i;
				break;
			}
		}
			
		if (rowNum == -1) {
			return;
		}
		
		if (typeof android !== 'undefined') {			
			android.removeData(stock);
		}
  
		var table = document.getElementById("myTable");
		table.deleteRow(rowNum);
		cancelModal('#yesNoModal', '', '');
    };
	
	$('#yesNoModal').modal('show');
}

function showAddRowModal() {
	$('#addRowModal').modal('show');
}

function clearModalContent(textID) {
    document.getElementById(textID).value = '';
}

function cancelModal(modalID, textID1, textID2) {
    $(modalID).modal('hide');
    if (textID1 != '')
        clearModalContent(textID1);
	
	if (textID2 != '')
        clearModalContent(textID2);
}