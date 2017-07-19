# -*- coding: utf-8 -*- # 
import os, time, string, json, threading
import wx
from libs.fpm import FpmLib 
import libs.file_util as fu
from libs.yaml_util import Options
from view.basic_console import BasicConsole
import requests
import subprocess

VERSION = '0.0.1'

TAG = 'BasicView'

class UpdateConsole(BasicConsole):
  def __init__(self):
    self.super = super(UpdateConsole, self)
    self.super.__init__()
    
  def ping_server(self):
    try:
      data = self.fpm.ping()
      if data['errno'] == 0:
        return True
      else:
        return False
    except Exception as e:
      print e
      return False

  def check_version(self):
    try:
      data = self.fpm.call_func('application.checkVersion', { 'app': self.options.get('app', 'eggs-plugin')}) 
      return data
    except Exception as e:
      return None

  def on_created(self):
    self.fpm = FpmLib()

  def run(self):
    if self.ping_server():
      version = self.check_version()
      if version is None:
        print ('No Version Info')
      else:
        print 'App: %s Has New Version Avaliable: %s \nURL: %s' % (self.options.get('app', 'eggs-plugin'), version['version'], version['download'])
        if self.version != version['version']:
          self.download(version['download'])
          if 'autorun' in version.keys():
            autorun = version['autorun']
            child = subprocess.Popen([autorun])
    else:
      print('ERROR: Offline! Cant Get The Remote Data~')

  def download(self, url):
    fu.mkdir_if_not_exists('cache')
    rsp = requests.get(url, stream=True)
    content_size = int(rsp.headers['content-length'])
    print 'Total About: %d MB' % (content_size/1024/1024)
    print 'Start Downading ... ...'
    f = open('./file.zip', 'wb')
    chunk_size = 1024 * 512
    counter = 0
    print 'Downloading... 0%'
    for data in rsp.iter_content(chunk_size=chunk_size):
      counter = counter + 1
      print 'Downloading... %s' % ( str(int((counter * chunk_size * 100)/content_size)) + '%' ) 
      f.write(data)
      if (counter * chunk_size)>content_size:
        break
    print 'Download Finished!'
    f.close()
    print 'Ready To UnZip The Apps'
    fu.un_zip(os.path.join(os.getcwd(), 'file.zip'), os.path.join(os.getcwd(), 'cache'))
    self.copy()

  def clean(self):
    fu.rmdir_if_exists('cache')
    fu.rm_if_exists('file.zip')

  def copy(self):
    fu.deep_list(os.path.join(os.getcwd(), './cache'), offset = self.options.get('offset', 6))
    self.clean()
