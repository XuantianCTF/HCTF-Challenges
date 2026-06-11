<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>试试把方块清空</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a1a;
        }
        
        /* 添加键盘提示 */
        .key-hint {
            position: fixed;
            top: 10px;
            left: 10px;
            color: white;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px 15px;
            border-radius: 5px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            z-index: 1000;
        }
        
        /* 鼠标效果提示 */
        .mouse-effect {
            position: fixed;
            top: 120px;
            left: 10px;
            color: white;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px 15px;
            border-radius: 5px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            z-index: 1000;
        }
        
        /* 鼠标轨迹效果 */
        .mouse-trail {
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 9999;
            transition: width 0.2s, height 0.2s, opacity 0.5s;
        }
    </style>
</head>
<body>
    <!-- 键盘提示 -->
    <div class="key-hint">
        按 R 键：随机颜色<br>
        按 C 键：清空/恢复<br>
        按空格键：重新排列<br>
        点击方块：单独变色
    </div>
    
    <!-- 鼠标效果提示 -->
    <div class="mouse-effect">
        鼠标移动：当前方块变色<br>
        按住鼠标拖动：连续变色<br>
        鼠标速度：<span id="mouseSpeed">0</span> px/s
    </div>
    
    <!-- 鼠标轨迹 -->
    <div id="mouseTrail" class="mouse-trail"></div>
    
    <!-- 原始方块（作为模板） -->
    <div id="box" style="width: 100px; height: 100px; background: yellow; position: absolute; display: none;"></div>
    
    <script src="proplem-mousemove-square-color.js"></script>
    
</body>
</html>
