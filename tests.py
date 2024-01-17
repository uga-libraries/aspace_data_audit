import unittest

import mysql.connector
import openpyxl
import subprocess  # TODO: build out running report through subprocess and testing excel output

from ASpace_Data_Audit import *
from secrets import *

AUDIT_FILE = ""  # Global variable for storing the filepath of the audit spreadsheet generated


class TestASpaceFunctions(unittest.TestCase):

    def test_connect_aspace_api(self):
        self.local_aspace = connect_aspace_api()
        self.assertIsInstance(self.local_aspace, ASnakeClient)

    def test_check_creators(self):
        # use https://stackoverflow.com/a/34738440 to capture stdout print statements for checking
        pass

    def test_check_child_levels(self):
        pass

    def test_check_res_levels(self):
        # use https://stackoverflow.com/a/34738440 to capture stdout print statements for checking
        pass

    def test_export_eads(self):
        # could test this by checking if exported files are in export_folder, but that would require dependency on
        # test_create_export_folder
        pass


class SpreadsheetTests(unittest.TestCase):

    def test_generate_spreadsheet(self):
        self.test_workbook, self.test_spreadsheet_filepath = generate_spreadsheet()
        self.assertIsInstance(self.test_workbook, openpyxl.Workbook)
        self.assertIsInstance(self.test_spreadsheet_filepath, str)
        self.assertEqual(os.path.exists(self.test_spreadsheet_filepath), True)

    def test_write_headers(self):
        test_headers = ["test_header_1", "test_header_2", "test_header_3"]
        self.sample_workbook, self.test_spreadsheet_filepath = generate_spreadsheet()
        write_headers(self.sample_workbook, "test", test_headers)
        self.sample_workbook.save(self.test_spreadsheet_filepath)

        test_workbook = openpyxl.load_workbook(self.test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        self.assertIn("test", test_sheetnames)

        if "test" in test_sheetnames:
            test_sheet = test_workbook["test"]
            for row in test_sheet.iter_rows(max_row=1, max_col=3):
                for cell in row:
                    self.assertIn(cell.value, test_headers)


class SQLTests(unittest.TestCase):

    def test_db_connection(self):
        self.db_connect, self.db_cursor = connect_db()
        self.assertIsNotNone(self.db_connect)
        self.assertIsNotNone(self.db_cursor)

    def test_query_db(self):
        test_statement = ('SELECT name, username FROM user')
        self.db_connect, self.db_cursor = connect_db()
        results = query_database(self.db_connect, self.db_cursor, test_statement)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_run_query(self):
        # use https://stackoverflow.com/a/34738440 to capture stdout print statements for checking
        pass

    def test_check_controlled_vocabs(self):
        # use https://stackoverflow.com/a/34738440 to capture stdout print statements for checking
        pass

    def test_check_duplicates(self):
        # not sure how to test this, since there's no print outputs
        pass


class AuditFunctionsTests(unittest.TestCase):

    def test_email_users(self):
        pass

    def test_standardize_resids(self):
        test_statement = ('SELECT repo.name AS Repository, resource.identifier AS Resource_ID  '
                          'FROM repository AS repo '
                          'JOIN resource ON repo.id = resource.repo_id ')
        self.db_connect, self.db_cursor = connect_db()
        results = query_database(self.db_connect, self.db_cursor, test_statement)
        updated_resids = standardize_resids(results)
        # print(results[1][1])
        # print(updated_resids[1][1])
        self.assertNotEqual(results[1][1], updated_resids[1][1])
        self.assertIsInstance(updated_resids[1][1], str)
        self.assertNotIn("Null", updated_resids[1][1])

    def test_update_booleans(self):
        test_statement = ('SELECT name, username, is_system_user AS System_Administrator '
                          'FROM user')
        self.db_connect, self.db_cursor = connect_db()
        results = query_database(self.db_connect, self.db_cursor, test_statement)
        updated_booleans = update_booleans(results)
        # print(results[1][2])
        # print(updated_booleans[1][2])
        self.assertIsNot(results[1][2], updated_booleans[1][2])
        self.assertIsInstance(updated_booleans[1][2], bool)

    def test_get_top_containers(self):
        pass

    def test_duplicate_subjects(self):
        # this function passes info to check_duplicates - consider removing from test or having test pass info to
        # check_duplicates
        pass

    def test_duplicate_agent_persons(self):
        # this function passes info to check_duplicates - consider removing from test or having test pass info to
        # check_duplicates
        pass

    def test_check_export_folder(self):
        pass

    def test_delete_export_folder(self):
        pass

    def test_check_urls(self):
        # again not sure how to test this function, no stdout
        pass

    def test_check_url(self):
        test_good_url = 'https://www.libs.uga.edu/'
        test_bad_url = 'http://www.cviog.uga.edu/about/chapel/history.php'
        good_response_code = check_url(test_good_url)
        bad_response_code = check_url(test_bad_url)
        self.assertIsNone(good_response_code)
        self.assertIsNotNone(bad_response_code)

    def test_run_audit(self):
        # no idea how to test this, it runs the whole suit of checks on our data, but no stdout - just writing to
        # workbook
        pass

    def test_email_error(self):
        # not sure how to test this, it refers to email_users
        pass

    def test_run_script(self):
        # this kicks off the whole script, would be difficult to test
        pass


class AuditOutputTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
