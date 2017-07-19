from view.update_console import UpdateConsole
if __name__ == "__main__":
    console = UpdateConsole()
    try:
      console.run()
    except Exception, e:
      print e
      console.exit()