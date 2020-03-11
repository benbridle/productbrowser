import sys
import configparser
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from ldproductbrowser.views import ProductBrowserWindow
from ldproductbrowser.models import ProductDatabase, BranchDatabase
from ldproductbrowser import globals as ldglobal


class AppContext(ApplicationContext):
    @cached_property
    def window(self):
        return ProductBrowserWindow()

    def run(self):
        self.window.show()
        return self.app.exec_()


if __name__ == "__main__":
    app_context = AppContext()
    ldglobal.app_context = app_context

    settings = configparser.ConfigParser()
    settings.read(app_context.get_resource("settings.cfg"))
    ldglobal.settings = settings

    ldglobal.productdb = ProductDatabase(app_context.get_resource("databases/ProductDatabase.db"))
    ldglobal.branchdb = BranchDatabase(app_context.get_resource("databases/BranchDatabase.db"))

    exit_code = app_context.run()
    sys.exit(exit_code)
