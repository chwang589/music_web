# 📧 邮件发送配置指南

目前系统处于演示模式，验证码显示在后端控制台。要启用真实邮件发送，请按以下步骤操作：

## 🚀 快速启用邮件发送

### 1. 配置Gmail邮箱（推荐）

1. **准备Gmail账号**
   - 确保已开启两步验证
   - 生成应用专用密码（不是你的登录密码）

2. **编辑配置文件**
   ```bash
   # 编辑 backend/email_config.py
   nano backend/email_config.py
   ```

3. **修改配置**
   ```python
   # 启用真实邮件发送
   ENABLE_EMAIL_SENDING = True
   
   # 配置你的Gmail
   EMAIL_ADDRESS = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-16-digit-app-password"
   ```

4. **重启后端服务**
   ```bash
   # 重启后端让配置生效
   # 配置完成后，验证码将发送到用户邮箱
   ```

### 2. 获取Gmail应用专用密码

1. 前往 [Google Account Settings](https://myaccount.google.com/)
2. 安全性 → 两步验证 → 应用专用密码
3. 选择"邮件"和"Windows计算机"
4. 复制生成的16位密码

### 3. 其他邮箱服务

如果不使用Gmail，可以修改SMTP配置：

```python
# Outlook/Hotmail
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

# Yahoo
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

# QQ邮箱
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
```

## 🔍 故障排除

- **演示模式**：验证码在后端控制台显示
- **邮件发送失败**：检查应用专用密码是否正确
- **连接超时**：确保网络能访问SMTP服务器

## 💡 安全建议

- 使用应用专用密码，不要使用账号密码
- 建议创建专门的邮箱用于发送系统邮件
- 不要将密码提交到代码仓库

---

当前状态：**演示模式** - 验证码在后端控制台显示
要启用邮件发送：编辑 `backend/email_config.py` 并重启服务