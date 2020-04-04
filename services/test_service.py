from models.test import Test
from copy import deepcopy
import secrets
import string

class TestService:

  def __init__(self, data):
    self.__test = Test(data)
    self.__input_query_load_data = None
    self.__schema_translation = {}
    self.__table_translation = {}

    self.__generate_translation()
    self.__generated_query = self.__get_wrapped_order_by_query()

  def __generate_translation(self):
    schema_val = self.__get_schema_val_to_be_replaced()
    table_used = self.__get_table_name_to_be_replaced()

    for val in schema_val:
      self.__schema_translation[val] = self.get_secret()
    
    for val in table_used:
      self.__table_translation[val] = self.get_secret()

  def __generate_wrapped_query(self):
    output_data = self.__test.get_output_data()
    sql_query = self.__test.get_sql_query()
    query_list = {}

    test_names = list(output_data.keys())
    input_query = self.__create_combined_input_query()
    for test_name in test_names:
      input_data = input_query[test_name]
      input_query_data = []
      for table_name, table_query in input_data.items():
        input_query_data.append(table_query)
      input_query = "WITH " + ", ".join(input_query_data)
      keys = ", ".join(list(output_data[test_name].keys()))
      query = "SELECT " + keys + " FROM ( " + sql_query + " )"
      query = input_query + query
      query_list[test_name] = query
    return query_list

  def __get_modified_table_final_query(self):
    query_list = self.__generate_wrapped_query()
    for test_name, query in query_list.items():
      for old_schema_value, updated_schema_value in self.__schema_translation.items():
        _query = deepcopy(query)
        query_list[test_name] = query_list[test_name].replace(old_schema_value, updated_schema_value)
      for old_table_name, updated_table_name in self.__table_translation.items():
        _query = deepcopy(query)
        query_list[test_name] = query_list[test_name].replace(old_table_name, updated_table_name)
    return query_list

  def __get_wrapped_order_by_query(self):
    query_list = self.__get_modified_table_final_query()
    for test_name, query in query_list.items():
      output_schema_len = len(list(self.__test.get_output_data()[test_name].keys()))
      val = [str(x+1) for x in range(output_schema_len)]
      order_by_val = ", ".join(val)
      query_list[test_name] += " ORDER BY " + order_by_val +  " DESC"
    return query_list

  def get_query(self):
    return self.__generated_query

  def __create_combined_input_query(self):
    preload_query = self.__test.get_preload_data_query()
    testcase_input_query = self.__test.get_testcase_input_query_data()
    for test_name, table_value in testcase_input_query.items():
      for table_name, query in table_value.items():
        if table_name in preload_query:
          continue
    
    table_query = deepcopy(testcase_input_query)
    for preload_table_name, preload_sql in preload_query.items():
      for test_name, table_values in testcase_input_query.items():
        is_preload_table_exists = False
        if preload_table_name in table_values:
          is_preload_table_exists = True
        if not is_preload_table_exists:
          table_query[test_name][preload_table_name] = preload_sql
    return table_query

  def __get_schema_val_to_be_replaced(self):
    schema_val = self.__test.get_schema_val()
    result = []
    for value in schema_val:
      if "." in value:
        result.append(value)
    return result

  def __get_table_name_to_be_replaced(self):
    table_used = self.__test.get_tables_used()
    result = []
    for value in table_used:
      if "." in value:
        result.append(value)
    return result

  def get_secret(self, length = 32):
    return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(length))

