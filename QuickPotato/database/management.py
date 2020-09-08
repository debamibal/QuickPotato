from QuickPotato.configuration.options import database_echo, database_connection_url
from QuickPotato.database.models import *
from QuickPotato.utilities.exceptions import *
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import database_exists, create_database, drop_database
import tempfile


class DatabaseManager(RawResultsModels, UnitPerformanceTestResultsModels):

    URL = database_connection_url

    def __init__(self):
        RawResultsModels.__init__(self)
        UnitPerformanceTestResultsModels.__init__(self)

    def validate_connection_url(self, database_name):
        """
        :return:
        """
        if self.URL is None:
            path_to_temp = tempfile.gettempdir() + "\\" if '\\' in tempfile.gettempdir() else "/"
            return "sqlite:///" + path_to_temp + database_name + ".db"

        elif database_connection_url.startswith('sqlite'):
            return self.URL + database_name + ".db"

        else:
            return f"{self.URL}/{database_name}"

    def spawn_engine(self, database_name):
        """
        :return:
        """
        try:
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            return engine

        except Exception:
            raise DatabaseConnectionCannotBeSpawned()

    def spawn_results_database(self, database_name):
        """
        :return:
        """
        try:
            # Add check for SQLite
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            if not database_exists(engine.url):
                create_database(engine.url)
            engine.dispose()
            return True

        except ProgrammingError:
            # Database exists no need to re-create it
            return True

        except Exception:
            raise DatabaseSchemaCannotBeSpawned()

    def delete_result_database(self, database_name):
        """

        Returns
        -------

        """
        url = self.validate_connection_url(database_name=database_name)
        engine = create_engine(url, echo=database_echo)
        if database_exists(engine.url):
            drop_database(engine.url)
        return True

    def spawn_time_spent_table(self, database_name):
        """
        :return:
        """
        try:
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            schema = self.time_spent_model()
            schema.metadata.create_all(engine)
            engine.dispose()

            return True

        except Exception:
            raise DatabaseTableCannotBeSpawned()

    def spawn_system_resources_table(self, database_name):
        """
        :return:
        """
        try:
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            schema = self.system_resources_model()
            schema.metadata.create_all(engine)
            engine.dispose()

            return True

        except Exception:
            raise DatabaseTableCannotBeSpawned()

    def spawn_boundaries_test_report_table(self, database_name):
        """
        :return:
        """
        try:
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            schema = self.boundaries_test_report_model()
            schema.metadata.create_all(engine)
            engine.dispose()

            return True

        except Exception:
            raise DatabaseTableCannotBeSpawned()

    def spawn_regression_test_report_table(self, database_name):
        """
        :return:
        """
        try:
            url = self.validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=database_echo)
            schema = self.regression_test_report_model()
            schema.metadata.create_all(engine)
            engine.dispose()

            return True

        except Exception:
            raise DatabaseTableCannotBeSpawned()
