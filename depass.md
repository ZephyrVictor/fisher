# 密码哈希与验证

## check_password_hash
- **目的**: 验证密码是否与给定的哈希匹配
- **步骤**:
  - 检查哈希格式
  - 拆分哈希值为方法、盐和哈希值
  - 使用`_hash_internal`重新计算哈希
  - 比较两个哈希值

## safe_str_cmp
- **目的**: 安全地比较两个字符串
- **步骤**:
  - 确保两个字符串都是字节串
  - 检查长度
  - 逐字节比较

## _hash_internal
- **目的**: 生成密码哈希
- **步骤**:
  - 检查方法
  - 确保密码是字节串
  - 解析'pbkdf2:'方法
  - 从`_hash_funcs`获取哈希函数
  - 根据方法选择生成哈希的方式

## pbkdf2_hex & pbkdf2_bin
- **目的**: 生成PBKDF2哈希
- **步骤**:
  - 确定哈希函数
  - 检查Python环境支持
  - 使用hmac和伪随机函数
  - 迭代生成哈希块