<?php

highlight_file(__FILE__);
file_put_contents('/flag', getenv("GZCTF_FLAG"));
class A
{
    public $a1;
    public function __call($func, $argv)
    {
        return $this->a1->a2;
    }
}

class B
{
    public $b;
    public function __invoke()
    {
        system($this->b);
    }
}

class C
{
    public $c;
    public function __get($name)
    {
        ($this->c)();
    }
}

class D
{
    public $d;
    public function __destruct()
    {
        echo 'Hello' . $this->d;
    }
}

class E
{
    public $e1;
    public function __toString()
    {
        return $this->e1->e2();
    }
}

$cmd = $_GET['cmd'];
if (isset($cmd)) {
    unserialize($cmd);
}
