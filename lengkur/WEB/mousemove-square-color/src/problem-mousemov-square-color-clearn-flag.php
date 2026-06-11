<?php
if(!isset($_SERVER['HTTP_X_CHALLENGE_TOKEN'])||$_SERVER['HTTP_X_CHALLENGE_TOKEN']!=='clearn')
{
	header("HTTP/1.1 403 Forbidden");
	exit(0);
}
$flag=getenv('GZCTF_FLAG');
echo $flag;
?>
