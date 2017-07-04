# -*- coding: utf-8 -*-
import shutil, os, zipfile

def copy(src, dest):
  shutil.copy(src, dest)

def copytree(src, dest):
  shutil.copytree(src, dest)

def rmdir(dir):
  shutil.rmtree(dir)

def rm(f):
  os.remove(f)

def rm_if_exists(f):
  if exists(f):
    os.remove(f)

def mkdir(dir):
  os.makedirs(dir)

def mkdir_if_not_exists(dir):
  if exists(dir):
    return
    
  mkdir(dir)

def mv(src, dest):
  shutil.move(src, dest)

def rmdir_if_exists(dir):
  if exists(dir):
    rmdir(dir)

# 删除文件夹下的子目录和文件    
def rmsub_if_exists(dir):
  for f in os.listdir(dir):   
    fullfile = os.path.join(dir, f)
    if os.path.isdir(fullfile):
      rmdir_if_exists(fullfile)
    else:
      rm_if_exists(fullfile)
  pass

def exists(dir):
  return os.path.exists(dir)

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()
