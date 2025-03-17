# command_line_journal

命令行里写日记

```sh
# 单行
echo "今天天气\n哈哈哈" | cmd_diary.py

# 多行
cat <<EOF | cmd_diary.py
今天天气
哈哈哈
EOF

# 文件
cmd_diary.py _diary.md
```

买个便宜的OSS, 
比如 腾讯云 10GB, 5年, 46元.

开个子账号，
权限是 "对象存储（COS）数据只写的访问权限（不含删除）"

然后调用api, 上传文本文件, 文件名是时间戳.

可以是 python 或者 其他脚本语言调用。
