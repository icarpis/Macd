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


$stock_name_val = $_GET["stock_name"];
$start_date = $_GET["start_date"];
$end_date = $_GET["end_date"];

$output = shell_exec("py ./MACD.py $stock_name_val $start_date $end_date");

echo $output;

$filepath1 = '.\Cash.png'; 
echo '<img src="'.$filepath1.'">';

$filepath2 = '.\StockPrice.png'; 
echo '<img src="'.$filepath2.'">';