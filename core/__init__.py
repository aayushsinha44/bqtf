from .file_manager import FileManager
import common.constants as constants
from services.test_service import TestService
from google.cloud import bigquery

def execute():
  content = FileManager.get_instance().get_yaml_file_content("", True)
  if constants.VERSION_KEY not in content:
    raise Exception("version is required.")
  if content[constants.VERSION_KEY] != constants.VERSION_1:
    raise Exception("Version " + str(content[constants.VERSION_KEY]) + " not supported.")
  if content[constants.TYPE] != constants.TYPE_TEST:
    raise Exception("type test is required.")
  test_service = TestService(content)
  query = test_service.get_query()
  
  for test_name, q in query.items():
    print("===============" + test_name + "===============")
    print(q)
  # SET ENV 'GOOGLE_APPLICATION_CREDENTIALS'
  

def get_big_query_output(query):
  client = bigquery.Client()
  results = query_job.result() 
  return result