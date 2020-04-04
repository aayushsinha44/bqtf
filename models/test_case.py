import common.constants as constants
from services.data_service import DataService
from core.file_manager import FileManager

class TestCase:

  def __init__(self, data):
    self.__data = data[constants.TEST_KEY_TESTCASE]
    self.__validate()
    self.__testcase_name = self.__data[constants.TEST_KEY_TESTCASE_NAME]
    self.__input_query_data = {}
    self.__output_data = {}
    self.__schema_val = set()

    self.__generate_input_query_data()
    self.__generate_output_data()

  def __validate(self):
    for key in constants.TEST_KEYS_TESTCASE_MUST:
      if key not in self.__data:
        raise ValueError(key+ " is required in testcase")

    for input_data in self.__data[constants.TEST_KEY_TESTCASE_INPUT]:
      if not (constants.TEST_KEY_TESTCASE_INPUT_DATA in input_data \
          or constants.TEST_KEY_TESTCASE_INPUT_DATA_PATH in input_data):
        raise ValueError(constants.TEST_KEY_TESTCASE_INPUT_DATA + 
                " or " + constants.TEST_KEY_TESTCASE_INPUT_DATA_PATH + " is required in testcase " + constants.TEST_KEY_TESTCASE_INPUT)

    # testcase output required key test
    for key in constants.TEST_KEYS_TESTCASE_OUTPUT_MUST:
      key_present = False
      for output_key in self.__data[constants.TEST_KEY_TESTCASE_OUTPUT]:
        if key == output_key:
          key_present = True
      if not key_present:
        raise ValueError(key + " is required in testcase " + constants.TEST_KEY_TESTCASE_OUTPUT)
    
    # output schema length matching
    output = self.__data[constants.TEST_KEY_TESTCASE_OUTPUT]
    schema_length = len(output[constants.TEST_KEY_TESTCASE_OUTPUT_SCHEMA])
    values = output[constants.TEST_KEY_TESTCASE_OUTPUT_VALUES]

    for value in values:
      if len(value[constants.DATA_KEY_VALUES_ROW]) != schema_length:
        raise ValueError("output schema and values length doesnot match.")

  def __generate_input_query_data(self):
    for input_data in self.__data[constants.TEST_KEY_TESTCASE_INPUT]:
      if constants.TEST_KEY_TESTCASE_INPUT_DATA in input_data:
        content = input_data[constants.TEST_KEY_TESTCASE_INPUT_DATA]
      else:
        content = FileManager.get_instance().get_yaml_file_content(input_data[constants.TEST_KEY_TESTCASE_INPUT_DATA_PATH])
      data_service = DataService(content, False)
      self.__insert_in_input_data_query(data_service.get_name(), data_service.generate_query())
      schema_val = data_service.get_schema()
      for data in schema_val:
        self.__schema_val.add(data)

  def __generate_output_data(self):
    output = self.__data[constants.TEST_KEY_TESTCASE_OUTPUT]
    schema = output[constants.TEST_KEY_TESTCASE_OUTPUT_SCHEMA]
    values = output[constants.TEST_KEY_TESTCASE_OUTPUT_VALUES]
    for schema_val in schema:
      _tmp = []
      for value in values:
        data = value[constants.DATA_KEY_VALUES_ROW]
        _tmp.append(data)
      self.__output_data[schema_val] = _tmp

  def get_input_query_data(self):
    return self.__input_query_data

  def get_testcase_name(self):
    return self.__testcase_name

  def get_output_data(self):
    return self.__output_data

  def get_schema_val(self):
    return self.__schema_val

  def __insert_in_input_data_query(self, key, value):
    if key not in self.__input_query_data:
      self.__input_query_data[key] = []
    self.__input_query_data[key] = value
