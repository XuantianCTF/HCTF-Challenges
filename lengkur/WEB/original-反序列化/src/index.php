<?php

highlight_file(__FILE__);
file_put_contents('/flag', getenv("GZCTF_FLAG"));
class 紧箍咒
{
    public $头;
    public $痛不痛;
    public $身本忧;

    public function __toString()
    {
        $this->头 = '痛';
        $this->痛不痛 = '不痛';
        if ($this->头 == '痛') {
            die('头怎么才能不痛呢？' . "<br>");
        } elseif ($this->头 == '不痛') {
            echo 'level up to 4' . "<br>";
            ($this->身本忧)();
            return "";
        }
    }
}

class 金箍棒
{
    public $身份;
    public $名字;
    public function change($x)
    {
        return str_replace("x", "xx", $x);
    }
    public function __call($func, $args)
    {
        $眼见喜 = $_POST['c'];
        $this->身份 = "ctfer.";
        $arr = [$眼见喜,$this->身份];
        $old = serialize($arr);
        $new = unserialize($this->change($old));

        if ($new[1] === "齐天大圣") {
            echo "level up to 3" . "<br>";
            echo "恭迎" . $this->名字 . '<br>';

        } else {
            echo "去也" . "<br>";
        }
    }
}

class 凤翅紫金冠
{
    public $避火罩 = "不避";
    public $意见欲;
    public $舌尝思;
    public $风火轮;
    public $哪吒;
    public function __invoke()
    {
        if ($this->避火罩 === "不避") {
            die("那别避了" . "<br>");
        }
        if (!preg_match("/exec|popen|popens|system|shell_exec|assert|eval|print|printf|array_keys|sleep|pack|array_pop|array_filter|highlight_file|show_source|file_put_contents|call_user_func|passthru|curl_exec/i", $this->风火轮)) {
            $exploar = new $this->哪吒($this->风火轮);
            $road = $this->意见欲;
            $exploar->$road($this->舌尝思);
        } else {
            die("为何要避" . "<br>");
        }

    }
}

class 锁子黄金甲
{
    public $亢金龙;
    public $定风珠;
    public $丹药;

    public function __get($name)
    {
        $this->定风珠 = $_GET['a'];
        $this->亢金龙 = $_GET['b'];

        if (substr($this->定风珠, 0, 16) !== substr($this->亢金龙, 0, 16) && md5($this->定风珠) === md5($this->亢金龙)) {
            echo "level up to 2" . "<br>";
            $this->丹药->长生丹();
        } else {
            echo '<br>' . 'no' . '<br>';
        }
    }
}


class 藕丝步云履
{
    public $踏云;
    public function __destruct()
    {
        if (preg_match("/^O:\d+/", $_GET["payload"])) {
            die("先学走路");
        }
        echo "level up to 1" . "<br>";
        return $this->踏云->腾云驾雾;
    }
}

$payload = $_GET["payload"];
if (isset($payload)) {
    unserialize($payload);
}
