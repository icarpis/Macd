
function readData() {
	if (typeof android !== 'undefined')
	{
		var strJSON = android.readData();
		const mapJSON = new Map(Object.entries(JSON.parse(strJSON)));
		for (let [key, value] of mapJSON) {
			addRow(key, value);
		}
	}
}

window.addEventListener("load", function(){
    if (typeof android !== 'undefined') {
		readData();
		android.pageIsReady();
	}
});

function showToast(text) {
  if (typeof android !== 'undefined')
	  android.showToast(text);
}


$(function() {
    $("td[colspan=3]").find("p").hide();
    $("table").click(function(event) {
        event.stopPropagation();
        var $target = $(event.target);
		if ( $target[0].colSpan == 1 ) {
			$target.closest("tr").next().find("p").slideToggle();
		}
    });
});