import common.constants as constants
from core.file_manager import FileManager
from services.data_service import DataService
from models.test_case import TestCase

class Test():

  def __init__(self, data):
    self.__data = data
    self.__validate()
    self.__initialize()

  def __validate(self):
    for key in constants.TEST_KEYS_MUST:
      if key not in self.__data:
        raise ValueError(key+ " is required in testcase file")

    if self.__data[constants.VERSION_KEY] != constants.VERSION_1:
      raise ValueError("Version " + str(self.__data[constants.VERSION_KEY]) + " not supported.")

    for key in self.__data[constants.TEST_KEY_TESTCASES]:
      if constants.TEST_KEY_TESTCASE not in key:
        raise ValueError("testcase is required in testcases")

    # unique test_name
    _test_name = {}
    for key in self.__data[constants.TEST_KEY_TESTCASES]:
      test_name = key[constants.TEST_KEY_TESTCASE][constants.TEST_KEY_TESTCASE_NAME]
      if test_name in _test_name:
        raise ValueError("TestName" + test_name + " already exists.")
      _test_name[test_name] = 1

  # initialize self variables
  def __initialize(self):
    self.__preload = None
    self.__preload_data_query = {}
    self.__testcase_input_query_data = {}
    self.__testcase_output_data = {}
    self.__schema_val = set()

    preload = constants.TEST_KEY_PRELOAD
    if preload in self.__data:
      self.__preload = self.__data[preload]
    
    self.__preload_query()

    self.__test_name = self.__data[constants.TEST_KEY_NAME]
    self.__tables_used = self.__data[constants.TEST_KEY_TABLES]

    _testcase_query_data = {}
    for testcase in self.__data[constants.TEST_KEY_TESTCASES]:
      testcase_object = TestCase(testcase)
      testcase_name = testcase_object.get_testcase_name()
      testcase_query = testcase_object.get_input_query_data()
      output_data = testcase_object.get_output_data()
      _testcase_query_data[testcase_name] = testcase_query
      self.__testcase_output_data[testcase_name] = output_data
      
      schema_val = testcase_object.get_schema_val()
      for data in schema_val:
        self.__schema_val.add(data)
      
      output_data_schema = list(output_data.keys())
      for data in output_data_schema:
        self.__schema_val.add(data)

    for key, value in _testcase_query_data.items():
      self.__insert_in_testcase_input_query_data(key, value)

    self.__sql = FileManager.get_instance().get_file_content(self.__data[constants.TEST_KEY_SQL])

  def __preload_query(self):
    if self.__preload is None:
      return
    for data_file in self.__preload:
      content = FileManager.get_instance().get_yaml_file_content(data_file)
      data_service = DataService(content)
      self.__insert_in_preload_data_query(data_service.get_name(), data_service.generate_query())
      
      schema_val = data_service.get_schema()
      for data in schema_val:
        self.__schema_val.add(data)

  def get_preload_data_query(self):
    return self.__preload_data_query

  def get_test_name(self):
    return self.__test_name

  def get_tables_used(self):
    return self.__tables_used

  def get_sql_query(self):
    return self.__sql

  def get_testcase_input_query_data(self):
    return self.__testcase_input_query_data

  def get_output_data(self):
    return self.__testcase_output_data

  def get_schema_val(self):
    return self.__schema_val

  def __insert_in_preload_data_query(self, key, value):
    if key not in self.__preload_data_query:
      self.__preload_data_query[key] = []
    self.__preload_data_query[key] = value

  def __insert_in_testcase_input_query_data(self, key, value):
    if key not in self.__testcase_input_query_data:
      self.__testcase_input_query_data[key] = []
    self.__testcase_input_query_data[key] = value
