
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