document.getElementById('end_date').value = moment().format('YYYY-MM-DD');



function button_busy()
{
	//document.getElementById("button").disabled = true;
	//document.getElementById("button").style.cursor = "wait";
}

function html_load()
{
	//document.getElementById("button").disabled = false;
	//document.getElementById("button").style.cursor = "default";
}

const moving_stop_loss_Checkbox = document.getElementById("moving_stop_loss");
const moving_stop_loss_Text = document.getElementById("moving_stop_loss_txt");

moving_stop_loss_Checkbox.addEventListener("change", () => {
  if (moving_stop_loss_Checkbox.checked)
  {
    moving_stop_loss_Text.disabled  = false;
  } else
  {
    moving_stop_loss_Text.disabled  = true;
  }
});