```markdown
## 项目结构

```plaintext
lottery-app/
├── FetchData/
│   ├── management/
│   │   └── commands/
│   │       ├── fetch_super_data.py  # 大乐透抓取逻辑（每周二、四、日开奖）
│   │       ├── fetch_3d_data.py     # 3D抓取逻辑（每天开奖）
│   │       └── fetch_kl8_data.py    # 快乐8抓取逻辑（每天开奖）
└── manage.py
```

---

## Django 数据库生成步骤

1. **生成迁移文件**  
   在项目根目录下运行以下命令，生成数据库迁移文件：  
   ```bash
   python manage.py makemigrations FetchData
   ```

2. **应用迁移到数据库**  
   执行以下命令后会创建数据表：  
   ```bash
   python manage.py migrate
   ```

3. **（可选）查看生成的 SQL 语句**  
   使用以下命令可以查看生成的 SQL 语句，用于验证迁移内容：  
   ```bash
   python manage.py sqlmigrate FetchData 0001_initial
   ```

---

## 数据抓取命令

- **获取超级大乐透数据**（每周二、四、日开奖）  
  ```bash
  python manage.py fetch_super_data
  ```

- **获取3D数据**（每天开奖）  
  ```bash
  python manage.py fetch_3d_data
  ```

- **获取快乐8数据**（每天开奖）  
  ```bash
  python manage.py fetch_kl8_data
  ```
```