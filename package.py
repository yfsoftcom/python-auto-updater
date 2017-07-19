import libs.file_util as fu
from libs.qiniu_util import upload
import time, datetime
import sys, os
from libs.fpm import FpmLib 
import subprocess
from view.basic_console import VERSION

print VERSION

args = sys.argv
if len(args) < 2:
  c = 'build'
else:
  c = args[1]

# remove
fu.rmdir_if_exists('dist')

# pyinstaller -w -F eggs_bot_gui.spec
retcode = subprocess.call(["pyinstaller", "-w", "-F", "console.spec"])
print retcode

fu.make_zip('dist', 'dist.zip')

fu.mv('dist.zip', 'dist\\')

# clean
fu.rmdir_if_exists('cache')
fu.rmdir_if_exists('build')
fu.rm_if_exists('file.zip')


if c == 'publish':
  # upload to qiniu
  t = time.time()
  v = str(int(t))
  n = 'app-' + str(int(t)) + '.zip'
  ret = upload(n, os.path.join(os.getcwd(), 'dist\\dist.zip'))
  print ret
  # update fpm version lib
  try:
    fpm = FpmLib()
    data = fpm.call_func('common.update',{ 'table': 'cm_version', 'condition': "app='auto-update'", 'row': {'version': VERSION, 'download': 'http://olk3bzfd5.bkt.clouddn.com/' + n}}) 
    print data
  except Exception as e:
    print e

