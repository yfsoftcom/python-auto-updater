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

def un_zip(source_file, output_dir):
  zipf = zipfile.ZipFile(source_file)
  zipf.extractall(output_dir)
  zipf.close()


def deep_list(path, offset = 6, dest_dir = os.getcwd()):
  print path, len(path)
  size = len(path) + offset
  for root, dirs, files in os.walk(path, topdown = False):
    for name in files:
      file_path = os.path.join(root, name)
      print file_path
      dest_file = os.path.join(dest_dir, file_path[size:])
      rm_if_exists(dest_file)
      dir, file = os.path.split(dest_file)
      mkdir_if_not_exists(dir)
      copy(os.path.join(root, name), dest_file)
