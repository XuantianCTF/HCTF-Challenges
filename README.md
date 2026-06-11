# 玄天网安实验室 CTF 赛题仓库

本仓库收录玄天网安实验室成员创作的 CTF 题目，供比赛及交流学习使用。

## 目录结构

实验室成员在仓库根目录下创建以自己命名的独立目录，目录下按题目方向分类存放。

```
成员名/
├── Web/
│   └── 题目名/
│       ├── flag          # 题目 flag
│       ├── container     # 容器地址（如有容器环境）
│       └── ...            # 题目相关文件
├── Pwn/
├── Reverse/
├── Crypto/
├── Misc/
└── ...
```

## 协作规范

本仓库为公共仓库，所有变更请遵循以下流程：

1. 从 `main` 分支创建新分支进行修改
2. 提交 Pull Request
3. 经审核合并至 `main` 分支 （实验室成员都会有审核权限）

禁止直接向 `main` 分支推送，以免造成仓库混乱。

### 常用协作命令

```bash
# 1. 克隆仓库
git clone git@github.com:xtsecurity/HCTF-Challenges.git
cd HCTF-Challenges

# 2. 从 main 创建新分支
git checkout -b yourname/new-feature

# 3. 添加题目并提交
git add .
git commit -m "feat: add yourname/Web/xxx"

# 4. 推送并创建 PR （PR需要在github网页上操作）
git push origin yourname/new-feature

# 5. 同步 main 分支最新代码
git checkout main
git pull
```

## 题目规范

### Flag

每个题目目录下需放置 flag 文件（文件名为 `flag` 或 `flag.txt`），文件中写入该题目的 Flag 值。

### exp

题目尽量附上exp，除非是非常简单的签到题

### 容器地址

如果题目包含容器环境（Docker / docker-compose），需在题目目录下创建 `container` 文件，文件中写入docker hub容器地址（如 `tuxnode/hello-world`），以便部署与访问。
