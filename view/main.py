# -*- coding: utf-8 -*- # 
import os, time, string, json, threading
import wx
from libs.fpm import FpmLib 
import libs.file_util as fu
from libs.yaml_util import Options
import requests
import subprocess
import libs.logger as logger

logger = logger.getLogger()

VERSION = '0.0.1'

TAG = 'BasicView'
class MainApp(wx.Frame):
  def __init__(self):
    self.fpm = FpmLib()
    self.version = VERSION
    self.on_create()
    
  def ping_server(self):
    try:
      data = self.fpm.ping() 
      if data['errno'] == 0:
        return True
      else:
        return False
    except Exception as e:
       return False

  def check_version(self):
    try:
      data = self.fpm.call_func('application.checkVersion', { 'app': self.options.get('app', 'eggs-plugin')}) 
      return data
    except Exception as e:
      return None

  def on_create(self):
    # load config
    path =  os.path.join(os.getcwd(), 'update.yaml')
    if fu.exists(path):
      self.options = Options(path)
    else:
      self.options = Options()
    # make cache dir
    fu.mkdir_if_not_exists('cache')
    
    if self.ping_server():
      version = self.check_version()
      if version is None:
        self.alert('No Version Info')
        wx.Exit()
      else:
        if self.version != version['version']:
          print ('Download URL: ' + version['download'])
          self.download(version['download'])
          autorun = self.options.get('main', None)
          if autorun != None:
            child = subprocess.Popen([autorun])
        wx.Exit()
    else:
      self.alert('Offline')

  def download(self, url):
    rsp = requests.get(url, stream=True)
    content_size = int(rsp.headers['content-length'])
    print content_size
    dialog = wx.ProgressDialog("Loading", "Downloading", 100,  
            style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME) 
    dialog.Update(0)

    f = open('./file.zip', 'wb')
    chunk_size = 1024
    counter = 0
    for data in rsp.iter_content(chunk_size=chunk_size):
      counter = counter + 1
      dialog.Update(int((counter * chunk_size * 100)/content_size))      
      f.write(data)
      if (counter * chunk_size)>content_size:
        break
    dialog.Update(100)
    f.close()

    fu.un_zip(os.path.join(os.getcwd(), 'file.zip'), os.path.join(os.getcwd(), 'cache'))
    self.copy()

  def clean(self):
    fu.rmdir_if_exists('cache')
    fu.rm_if_exists('file.zip')

  def copy(self):
    fu.deep_list(os.path.join(os.getcwd(), './cache'), offset = self.options.get('offset', 6))
    self.clean()

  def alert(self, message):
    wx.MessageBox(message, 'tips')

  def confirm(self, message):
    dlg = wx.MessageDialog(None, message, u"Question", wx.YES_NO | wx.ICON_QUESTION)
    return dlg.ShowModal() == wx.ID_YES
