```markdown
# 彩票数据抓取系统文档

## 📁 项目目录结构

```tree
lottery-app/
├── FetchData/
│   ├── management/
│   │   └── commands/
│   │       ├── fetch_super_data.py   # 大乐透数据抓取（每周二、四、日）
│   │       ├── fetch_3d_data.py      # 3D数据抓取（每日）
│   │       └── fetch_kl8_data.py     # 快乐8数据抓取（每日）
└── manage.py
```

---

## 🚀 服务启动指南

### 启动开发服务器
```bash
python manage.py runserver
```

### 服务访问地址
- 管理后台：http://localhost:8000/admin/
- 彩票应用：http://localhost:8000/lottery/

### 路由配置（修改 LotteryApp/urls.py）
```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lottery/', include('lottery.urls')),  # 彩票应用路由
]
```

---

## 🗃️ 数据库配置流程

1. **生成数据库迁移文件**
```bash
python manage.py makemigrations FetchData
```

2. **执行数据库迁移**
```bash
python manage.py migrate
```

3. **（可选）查看SQL语句**
```bash
python manage.py sqlmigrate FetchData 0001_initial
```

---

## ⚡ 数据抓取命令

| 彩种        | 执行命令                        | 开奖频率       |
|-------------|-------------------------------|---------------|
| 大乐透       | `python manage.py fetch_super_data` | 每周二、四、日 |
| 3D彩票      | `python manage.py fetch_3d_data`    | 每日          |
| 快乐8       | `python manage.py fetch_kl8_data`   | 每日          |

---

## 📝 使用提示

1. 首次使用前需执行数据库迁移
2. 建议配置定时任务自动执行抓取命令
3. 可通过Django Admin后台管理抓取数据
4. 自定义应用需在lottery/urls.py中添加具体路由
```

### 优化说明：
1. 使用更直观的目录树呈现方式
2. 增加功能对照表格清晰展示不同彩票类型的抓取命令
3. 添加图标提升文档可读性（需支持emoji的环境）
4. 使用标准markdown语法确保兼容性
5. 增加使用提示和注意事项
6. 优化路由配置示例代码的格式
7. 统一命令格式为代码块形式


配置vue 环境
1.从 Node.js 官网 下载并安装最新版本。

2.检查 Node.js 和 npm 是否安装正确
打开终端或命令提示符，运行以下命令：
node -v
npm -v

3.如果出现问题，检查系统环境变量是否正确配置。

4.使用管理员启动命令行，再次运行第2步的命令：

5. 检查当前的执行策略
打开 PowerShell（以管理员身份运行），输入以下命令查看当前的执行策略：

powershell
复制
Get-ExecutionPolicy
常见的执行策略包括：

Restricted: 禁止运行任何脚本。

AllSigned: 只允许运行经过数字签名的脚本。

RemoteSigned: 允许运行本地脚本，但远程脚本必须经过数字签名。

Unrestricted: 允许运行所有脚本。

更改执行策略
为了允许运行 npm.ps1，您需要将执行策略更改为 RemoteSigned 或 Unrestricted。

在 PowerShell 中运行以下命令：

powershell
复制
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
系统会提示您确认更改，输入 Y 并按回车。

验证更改
再次运行以下命令，检查执行策略是否已更改：

powershell
复制
Get-ExecutionPolicy
如果输出为 RemoteSigned，说明更改成功。
