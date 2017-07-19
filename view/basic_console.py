#-*-<coding=UTF-8>-*-
import os, time, string, threading
from libs.yaml_util import Options
import libs.file_util as fu
from libs.logger_util import getLogger
import subprocess

TAG = 'BasicConsole'
VERSION = '1.0.0'
class BasicConsole(object):
  def __init__(self):
    self.logger = getLogger()
    self.presenter = None
    self.version = VERSION
    print '\033[1;32;40m'
    print 'Version: %s' % (self.version)
    self.on_create()

  def on_create(self):
    # 初始化配置文件
    # load config
    path =  os.path.join(os.getcwd(), 'update.yaml')
    if fu.exists(path):
      self.options = Options(path)
    else:
      self.options = Options()
    self.on_created()
    self._quit_flag = False

  def on_created(self):
    pass

  def on_destory(self):
    print '%s : on_destory' % (TAG)
    if self.presenter != None:
      self.presenter.finish()
    self._quit_flag = True
    self.stop()

  def exit(self):
    self.on_destory()

  def run(self):
    print 'type : start to run or q,exit to stop'
    while self._quit_flag == False:
      command = raw_input('')
      if command == 'exit' or command == 'q':
        self.on_destory()
        break
      # run command
      self.do_input(command)

  def do_input(self, command):
    if self.presenter != None:
      self.presenter.do_input(command)
      return
    print '%s : do_input , you have to impl the presenter' % (TAG)