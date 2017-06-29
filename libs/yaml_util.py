#-*-<coding=UTF-8>-*-
import os, time, string
import yaml
class Options(object):
  def __init__(self, path = None):
    self.path = path
    if path is None:
      self.is_init = True
      self.options = {}
    else:
      self.is_init = False

  def load(self):
    fr = open(self.path, 'r')
    self.options = yaml.load(fr)
    if self.options is None:
      self.options = {}
    self.is_init = True

  def get(self, key = None, dfv = None):
    if self.is_init:
      if key is None:
        return self.options
      if key in self.options.keys():
        return self.options[key]
      else:
        return dfv
    
    self.load()
    return self.get(key)

  def set(self, key, val):
    if self.is_init:
      self.options[key] = val
      return self
    self.load()
    return self.set(key, val)

  def save(self):
    try:
      fw = open(self.path, 'w')
      yaml.dump(self.options, fw)
    finally:
      fw.close()
  

if __name__ == "__main__":
  path =  os.path.join(os.getcwd(), 'options.yaml')
  options = Options(path)
  print options.get('limit')
  options.set('limit', {'max': 2.8, 'min': 1.2})

  options.save()