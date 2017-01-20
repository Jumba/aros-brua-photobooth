<?php

require("vendor/autoload.php");

/////// CONFIG ///////
$filename = $argv[1];
$username = $argv[2];
$password = $argv[3];
$debug = false;

$caption = '#arosbrua #ron25+1';     // caption
//////////////////////

$i = new \InstagramAPI\Instagram($debug);

$i->setUser($username, $password);

try {
    $i->login();
} catch (Exception $e) {
    $e->getMessage();
    exit();
}

try {
    $i->uploadPhoto($filename, $caption);
} catch (Exception $e) {
    echo $e->getMessage();
}
