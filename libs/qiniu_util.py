# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = '65nep44MNB8Ft1v_L1f7jaSnP8P07buuMMN4kI81'
secret_key = 'kZxy-i93_B98yg4lNn7XmSujeZh_JWRxQOJX3E_m'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'yfsoft'

def upload(key, file):
  #上传到七牛后保存的文件名
  # key = 'app.zip'
  #生成上传 Token，可以指定过期时间等
  token = q.upload_token(bucket_name, key, 3600)
  #要上传文件的本地路径
  ret, info = put_file(token, key, file)
  return ret