#!/usr/bin/env python
import argparse
import sys
import os
import logging
import datetime
from qcloud_cos import CosConfig, CosS3Client

Region = ""
Bucket = ""
SecretId = os.environ.get('COS_SECRET_ID')
SecretKey = os.environ.get('COS_SECRET_KEY')

filepath = os.path.join(os.path.expanduser("~"), ".cmd_diary_cos.ini")
if os.path.exists(filepath):
    with open(filepath, "r") as f:
        for _ in f.readlines():
            if _.startswith("Region"):
                Region = _.split("=")[1].strip()
            if _.startswith("Bucket"):
                Bucket = _.split("=")[1].strip()
            if _.startswith("SecretId"):
                SecretId = _.split("=")[1].strip()
            if _.startswith("SecretKey"):
                SecretKey = _.split("=")[1].strip()

def upload(content):
    # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    return CosS3Client(CosConfig(
        Region=Region,
        SecretId=SecretId,
        SecretKey=SecretKey,
    )).put_object(
        Bucket=Bucket,  # Bucket 由 BucketName-APPID 组成
        Body=content,
        Key=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".txt",
        StorageClass='MAZ_STANDARD', # 单AZ: STANDARD, 多AZ: MAZ_STANDRD
        ContentType='text/html; charset=utf-8'
    )["ETag"]

def main():
    parser = argparse.ArgumentParser(
        description='文件/标准输入内容',
    )
    parser.add_argument(
        'filename',
        nargs='?',  # 将文件名改为可选参数
        help='输入文件路径（如果不提供则读取标准输入）'
    )
    args = parser.parse_args()

    # 判断输入来源
    if not sys.stdin.isatty():  # 检测是否有管道输入
        content = sys.stdin.buffer.read().decode('utf-8', errors='replace')
    elif args.filename:         # 从文件读取
        try:
            with open(args.filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"错误：文件 '{args.filename}' 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"读取文件时发生错误：{str(e)}")
            sys.exit(1)
    else:
        print("错误：需要提供文件或输入内容")
        parser.print_help()
        sys.exit(1)

    print(upload(content))

if __name__ == "__main__":
    main()
