<?php
header('Content-Type: text/html; charset=utf-8');
$ua=$_SERVER["HTTP_USER_AGENT"];
if(preg_match("/sqlmap/i",$ua)){
  die("使用sqlmap是没有灵魂的");
}

$realFlag = getenv('GZCTF_FLAG');

$host = getenv('DB_HOST') ?: '127.0.0.1';
$user = getenv('DB_USER') ?: 'root';
$pass = getenv('DB_PASS') ?: '';
$db   = getenv('DB_NAME') ?: 'cttraining';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("系统维护中，请稍后再试...");
}
$conn->set_charset("utf8mb4");
$conn->query("SET NAMES utf8mb4");
$conn->query("SET CHARACTER_SET_CLIENT=utf8mb4");
$conn->query("SET CHARACHTER_SET_RESULTS=utf8mb4");
$check = $conn->query("SELECT * FROM user WHERE password = 'f14g'");
if ($check && $check->num_rows > 0) {
    $stmt = $conn->prepare("UPDATE user SET password = ? WHERE password = 'f14g'");
    $stmt->bind_param("s", $realFlag);
    $stmt->execute();
    $stmt->close();
}

$bg_image = "ikun03.jpg";
$result_msg = "";

if (isset($_POST['name'])) {
    $name = $_POST['name'];

    if ($name === 'ikun') {
        $bg_image = "ikun02.jpg";
    } elseif ($name === 'flag') {
        $bg_image = "ikun03.jpg";
    } elseif ($name === 'Re0l flag') {
        $bg_image = "ikun01.jpg";
    } else {
        $bg_image = "ikun03.jpg";
    }

    $sql = "SELECT password FROM user WHERE name = '$name' LIMIT 0,1";
    $res = $conn->query($sql);

    if($res){
        if ($res && $res->num_rows > 0) {
            $row = $res->fetch_assoc();
            $result_msg = $row['password'];
        } else {
            $result_msg = "?鸡公煲？？";
        }
    }else{
        $result_msg = $conn->error;
    }
}
?>

<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <title>注入点为name</title>
    <style>
        body {
            background: url('/Picture/<?php echo $bg_image; ?>') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: "Microsoft YaHei", sans-serif;
            transition: background 0.5s ease;
        }

        .container {
            background: rgba(255, 255, 255, 0.85);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 450px;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
        }

        input[type="text"] {
            width: 80%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            outline: none;
            font-size: 18px;
        }

        input[type="submit"] {
            margin-top: 20px;
            padding: 10px 30px;
            background: #ffcc00;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
        }

        input[type="submit"]:hover {
            background: #e6b800;
        }

        .result {
            margin-top: 25px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.05);
            color: #d9534f;
            font-weight: bold;
            word-break: break-all;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>你是谁来着？</h1>
        <form action="" method="POST">
            <input type="text" name="name" value="<?php echo isset($_POST['name']) ? htmlspecialchars($_POST['name']) : 'ikun'; ?>">
            <br>
            <input type="submit" value="是的..嗯对">
        </form>

        <?php if ($result_msg): ?>
            <div class="result">
                <?php echo $result_msg; ?>
            </div>
        <?php endif; ?>
    </div>
</body>

</html>
