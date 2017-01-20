<?php

require("vendor/autoload.php");

/////// CONFIG ///////
$username = $argv[1];
$password = $argv[2];
$debug = false;

$photo_id = $argv[3];

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
    $i->deleteMedia($photo_id);
} catch (Exception $e) {
    echo $e->getMessage();
}
