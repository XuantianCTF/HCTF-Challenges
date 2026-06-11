<?php

$flag = getenv("GZCTF_FLAG");
file_put_content("/flag", $flag)
