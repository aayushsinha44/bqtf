import os
from yaml import load, Loader

class FileManager:
  __instance = None

  @staticmethod
  def get_instance():
    if FileManager.__instance == None:
      raise Exception("FileManager class has been not initialized yet.")
    return FileManager.__instance

  def __init__(self, path):
    self.__folder = (os.sep).join(path.split(os.sep)[:-1])
    self.__file = path.split(os.sep)[-1]
    self.__path = path

    if FileManager.__instance != None:
      raise Exception("FileManager class has been initialized. Use get_instance().")
    else:
      FileManager.__instance = self

  def get_file_content(self, path):
    path = os.path.join(self.__folder, path)
    file = open(path, 'r')
    content = file.read()
    file.close()
    return content

  def get_yaml_file_content(self, path, is_source = False):
    if is_source:
      path = self.__path
    content = self.get_file_content(path)
    return load(content, Loader=Loader)