<?php
if (!isset($_GET["stock_name"])) {
    echo "stock_name must be provided!";
	exit;
}

if (!isset($_GET["start_date"])) {
    echo "start_date must be provided!";
	exit;
}

if (!isset($_GET["end_date"])) {
    echo "end_date must be provided!";
	exit;
}

$script_name = "./MACD.py";
$debug_script_name = "./MACD2.py";

$stock_name_val = $_GET["stock_name"];
$start_date = $_GET["start_date"];
$end_date = $_GET["end_date"];

if (isset($_GET["debug"])) {
    $output = shell_exec("py ".$debug_script_name . " " . $stock_name_val . " " . $start_date . " " . $end_date);
	echo $output;
} else {
	$output = shell_exec("py ".$script_name . " " . $stock_name_val . " " . $start_date . " " . $end_date);
	echo $output;
}




