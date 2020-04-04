# from api.handler import Handler
import os
from core.file_manager import FileManager
from core import execute
import argparse

def main():
  parser = argparse.ArgumentParser(description = "BIG Query Testing Framework")
  parser.add_argument("-p", "--path", nargs = 1, metavar = "path", type = str, help="test file path")
  args = parser.parse_args() 
  if len(args.path) != 0: 
    path = args.path[0]
    FileManager(path)
    execute()
  else:
    raise Exception("File Path is required. --path")

if __name__ == '__main__':
  main()