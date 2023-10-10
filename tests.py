import unittest

import mysql.connector
import openpyxl

from ASpace_Data_Audit import *
from secrets import *


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
        pass

    def test_write_headers(self):
        pass


class SQLTests(unittest.TestCase):

    def test_db_connection(self):
        self.db_connect, self.db_cursor = connect_db()
        self.assertIsNotNone(self.db_connect)
        self.assertIsNotNone(self.db_cursor)
        pass

    def test_query_db(self):
        pass

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
        pass

    def test_update_booleans(self):
        pass

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
        pass

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


if __name__ == '__main__':
    unittest.main()
