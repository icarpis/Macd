document.getElementById('end_date').value = moment().format('YYYY-MM-DD');



function button_busy()
{
	var down = document.getElementById("down");
	if (down)
	{
		document.getElementById("button").disabled = true;
		document.getElementById("button").style.cursor = "wait";
	
	    $.ajax({
        url: 'stock.php',
        type: 'get',
        data: {
			"stock_name": $('#stock').val(),
			"stock_name2": $('#stock2').val(),
			"buy": $('#buy').val(),
			"start_date": $('#start_date').val(),
			"end_date": $('#end_date').val(),
			"moving_stop_loss": $('#moving_stop_loss_txt').val()
        }
		}).done(function(result) {
			$('#down').html(result);
			document.getElementById("button").disabled = false;
			document.getElementById("button").style.cursor = "default";
		});
	}
}

function html_load()
{
	
}
