<?php
header("Content-Type: application/json; charset=UTF-8");
//$_POST['pattern'] = ["wx4g28p","wx4g0y9","wx4g0jk"];
$path = json_encode($_POST['pattern']);
$min = intval($_POST['start']);
$max = intval($_POST['end']);
$gap = intval($_POST['gap']);
$matches = intval($_POST['match']);
$input = "$path $min $max $gap $matches";
//echo $input;

//$output = shell_exec("C:\Users\maros\.virtualenvs\zobrazenie-SYSuuEtd\Scripts\python.exe .\geohash.py $input");

$output = shell_exec("python3 geohash.py ".$input);
echo $output;
 
?>