<?php

include "./12345.php";
function getFlag()
{
    system('cat /flag');
}

if (isset($_GET['code'])) {
    $code = $_GET['code'];
    if (strlen($code) > 40) {
        die("Long.");
    }
    if (preg_match("/[A-Za-z0-9~]+/", $code)) {
        die("NO.");
    }
    @eval($code);
} else {
    highlight_file(__FILE__);
}
