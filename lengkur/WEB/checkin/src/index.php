<?php

highlight_file(__FILE__);

$FLAG = getenv("GZCTF_FLAG");
file_put_contents('/flag', $FLAG);
$cmd = $_GET['cmd'];
if (!preg_match("/\//i", $cmd)) {
    eval($cmd);
}
