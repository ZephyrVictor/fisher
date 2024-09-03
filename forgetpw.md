

**我的重置密码功能思维导图**

- **忘记密码请求 (`forget_password_request` 函数)**
  - 验证邮箱是否存在于数据库
  - 生成令牌
  - 使用`send_mail`发送邮件
    - 邮件内容包括重置链接

- **令牌生成**
  - 使用`TimedJSONWebSignatureSerializer`类
    - 默认有效期：3600秒（1小时）
    - 令牌头部字段
      - `iat`：生成时间
      - `exp`：过期时间

- **JSON Web Signature (JWS)**
  - 使用`JSONWebSignatureSerializer`类
    - 支持的哈希算法：HS256、HS384、HS512等
    - 验证令牌时检查`alg`字段

- **令牌的验证**
  - 用户点击邮件中的链接
  - 异常处理
    - `SignatureExpired`：令牌过期
    - `BadSignature`：令牌无效或被篡改

