<?php

require("vendor/autoload.php");

/////// CONFIG ///////
$username = 'arosbrua';
$password = 'FundashonProBrua2016';
$debug = false;

$photo_id = $argv[1];

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
