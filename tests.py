import ast
import time
import unittest

import openpyxl
import pathlib
import subprocess

from ASpace_Data_Audit import *
from secrets import *

AUDIT_FILE = ""  # Global variable for storing the filepath of the audit spreadsheet generated


class AuditOutputTests(unittest.TestCase):

    def test_run_report(self):
        test = pathlib.Path(os.getcwd(), 'venv/Scripts/activate')
        print(test)
        subprocess.run(['source', 'venv/Scripts/activate'])
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.call(["python", "ASpace_Data_Audit.py", "--test"])
        testing_spreadsheet = pathlib.Path(os.getcwd(), f'data_audit_{str(date.today())}.xlsx')
        report_generated = self.assertIsFile(testing_spreadsheet)
        if report_generated is True:
            global AUDIT_FILE
            AUDIT_FILE = report_generated

    def test_audit_file(self):
        print(AUDIT_FILE)
        self.assertIsFile(AUDIT_FILE)

    @staticmethod
    def assertIsFile(path):
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError(f'File does not exist: {str(path)}')


    @staticmethod
    def assertIsFolder(path):
        if not pathlib.Path(path).resolve().is_dir():
            raise AssertionError(f'Folder does not exist: {str(path)}')


    @staticmethod
    def assertHasFiles(path):
        if not os.listdir(path):
            raise AssertionError(f'Files do not exist in {path}')


class TestASpaceFunctions(AuditOutputTests):

    def test_connect_aspace_api(self):
        self.local_aspace = connect_aspace_api()
        self.assertIsInstance(self.local_aspace, ASnakeClient)

    def test_check_creators(self):
        self.sample_workbook, self.test_spreadsheet_filepath = generate_spreadsheet()
        self.local_aspace = connect_aspace_api()
        check_creators(self.sample_workbook, self.local_aspace)
        self.sample_workbook.save(self.test_spreadsheet_filepath)

        test_workbook = openpyxl.load_workbook(self.test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        self.assertIn("Resources without Creators", test_sheetnames)

        if "Resources without Creators" in test_sheetnames:
            test_sheet = test_workbook["Resources without Creators"]
            for row in test_sheet.iter_rows(min_row=2, max_row=2, min_col=4, max_col=4):
                for cell in row:
                    if cell.value:
                        self.assertEqual(cell.value, "None")
        os.remove(self.test_spreadsheet_filepath)

    def test_check_child_levels(self):
        pass

    def test_check_res_levels(self):
        self.sample_workbook, self.test_spreadsheet_filepath = generate_spreadsheet()
        self.local_aspace = connect_aspace_api()
        check_res_levels(self.sample_workbook, self.local_aspace, test=True)
        self.sample_workbook.save(self.test_spreadsheet_filepath)

        test_workbook = openpyxl.load_workbook(self.test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        self.assertIn("Collection Level Checks", test_sheetnames)

        if "Collection Level Checks" in test_sheetnames:
            test_sheet = test_workbook["Collection Level Checks"]
            for row in test_sheet.iter_rows(min_row=2, max_row=2, min_col=5, max_col=5):
                for cell in row:
                    if cell.value:
                        test_value = ast.literal_eval(cell.value)
                        self.assertIsInstance(test_value, list)
                        self.assertTrue(len(cell.value) >= 2)
        os.remove(self.test_spreadsheet_filepath)

    def test_export_eads(self):
        test_workbook, test_spreadsheet_filepath = generate_spreadsheet()
        export_folder = str(pathlib.Path(os.getcwd(), "source_eads"))
        if not os.path.exists(export_folder):
            os.mkdir(export_folder)
        local_aspace = connect_aspace_api()
        export_eads(test_workbook, export_folder, local_aspace)
        self.assertHasFiles(export_folder)
        for root, directories, files in os.walk(export_folder):
            for filename in files:
                self.assertEqual(str(Path(filename).suffix), '.xml')


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
        test_workbook, test_spreadsheet_filepath = generate_spreadsheet()
        test_headers = ["Name", "Username", "System Administrator?", "Hidden User?"]
        self.db_connect, self.db_cursor = connect_db()
        self.test_statement = ('SELECT name, username, is_system_user AS System_Administrator, '
                               'is_hidden_user AS Hidden_User FROM user')
        run_query(test_workbook, 'Users', test_headers, self.test_statement, booleans=True)
        test_workbook.save(test_spreadsheet_filepath)
        test_workbook = openpyxl.load_workbook(test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        if "Users" in test_sheetnames:
            user_sheet = test_workbook["Users"]
            potential_users = []
            for row in user_sheet.iter_rows(min_row=2, max_col=1):
                for cell in row:
                    potential_users.append(cell.value)
            self.assertIn('Administrator', potential_users)
        os.remove(test_spreadsheet_filepath)

    def test_check_controlled_vocabs(self):
        test_workbook, test_spreadsheet_filepath = generate_spreadsheet()
        test_vocab = 'Name_Sources'
        test_terms = ["local", "naf", "ingest", "snac", "lcnaf"]
        test_term_num = 4
        check_controlled_vocabs(test_workbook, test_vocab, test_terms, test_term_num)

        test_workbook.save(test_spreadsheet_filepath)
        test_workbook = openpyxl.load_workbook(test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        if "Name_Sources" in test_sheetnames:
            user_sheet = test_workbook["Name_Sources"]
            potential_vocab = []
            for row in user_sheet.iter_rows(min_row=2, max_col=1):
                for cell in row:
                    potential_vocab.append(cell.value)
                    if cell.value not in test_terms:
                        self.assertTrue(cell.font.color)
            self.assertIn('lcnaf', potential_vocab)
        os.remove(test_spreadsheet_filepath)

    def test_check_duplicates(self):
        test_workbook, test_spreadsheet_filepath = generate_spreadsheet()
        test_headers = ["Original Subject", "Original Subject ID", "Duplicate Subject", "Duplicate Subject ID"]
        test_statement = f'SELECT title, id FROM subject'
        test_sheetname = 'Duplicate Subjects'
        test_uri_string = '/subjects/'
        check_duplicates(test_workbook, test_headers, test_statement, test_sheetname, test_uri_string)

        test_workbook.save(test_spreadsheet_filepath)
        test_workbook = openpyxl.load_workbook(test_spreadsheet_filepath)
        test_sheetnames = test_workbook.sheetnames
        if 'Duplicate Subjects' in test_sheetnames:
            user_sheet = test_workbook["Duplicate Subjects"]
            potential_duplicates = {}
            duplicate_count = 0
            for row in user_sheet.iter_rows(min_row=2, max_col=4):
                potential_duplicates[duplicate_count] = []
                for cell in row:
                    if cell.value:
                        self.assertIsInstance(cell.value, str)
                        potential_duplicates[duplicate_count].append(cell.value)
                duplicate_count += 1
            for result_index, results in potential_duplicates.items():
                if results:  # if results not an empty list
                    original_name = results[0]
                    duplicate_name = results[2]
                    self.assertEqual(original_name, duplicate_name)

                    original_uri = results[1]
                    duplicate_uri = results[3]
                    self.assertNotEqual(original_uri, duplicate_uri)
        os.remove(test_spreadsheet_filepath)


class AuditFunctionsTests(AuditOutputTests):

    def test_email_users(self):
        send_from = input(f'Enter the email to send from: ')
        send_to = [f'{input("Enter the email to send to: ")}']
        email_subject = f'Test email_users for ASpace_Data_Audit'
        email_message = ("This is a test of the email_users function. If you received this, you can type 'Yes' in the "
                         "console response.")
        test_server = input(f'Enter the email server: ')
        try:
            email_users(send_from, send_to, email_subject, email_message, server=test_server)
        except Exception as error:
            self.fail(error)
        email_response = input(f'Did you receive an email from the above source? It may take a minute or two. '
                               f'Type Yes or No: ').lower()
        self.assertEqual(email_response, 'yes')

    def test_standardize_resids(self):
        test_statement = ('SELECT repo.name AS Repository, resource.identifier AS Resource_ID  '
                          'FROM repository AS repo '
                          'JOIN resource ON repo.id = resource.repo_id ')
        self.db_connect, self.db_cursor = connect_db()
        results = query_database(self.db_connect, self.db_cursor, test_statement)
        updated_resids = standardize_resids(results)
        self.assertNotEqual(results[1][1], updated_resids[1][1])
        self.assertIsInstance(updated_resids[1][1], str)
        self.assertNotIn("Null", updated_resids[1][1])

    def test_update_booleans(self):
        test_statement = ('SELECT name, username, is_system_user AS System_Administrator '
                          'FROM user')
        self.db_connect, self.db_cursor = connect_db()
        results = query_database(self.db_connect, self.db_cursor, test_statement)
        updated_booleans = update_booleans(results)
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
        export_folder = pathlib.Path(os.getcwd(), "source_eads")
        self.assertIsFolder(export_folder)

    def test_delete_export_folder(self):
        source_eads_path = str(Path.joinpath(Path.cwd(), "test_source_eads"))
        os.mkdir(source_eads_path)
        time.sleep(5)
        delete_export_folder(source_eads_path)
        if not os.path.exists(source_eads_path):
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
        send_from = input(f'Enter the email to send from: ')
        send_to = [f'{input("Enter the email to send to: ")}']
        test_server = input(f'Enter the email server: ')
        try:
            email_error(send_from, send_to, f'TEST ERROR for ASpace_Data_Audit - not real error',
                        server=test_server)
        except Exception as error:
            self.fail(error)
        email_response = input(f'Did you receive an email from the above source? It may take a minute or two. '
                               f'Type Yes or No: ').lower()
        self.assertEqual(email_response, 'yes')
        pass

    def test_run_script(self):
        run_script(False)
        generated_report = pathlib.Path(os.getcwd(), f'data_audit_{str(date.today())}.xlsx')
        self.assertIsFile(generated_report)
        pass


if __name__ == '__main__':
    unittest.main()
