from view.app import App
from view.main import MainApp
if __name__ == "__main__":
  app = App()
  view = MainApp()
  try:
    app.startup(view)
    
  except Exception as e:
    print('Error: ' +e.message) 