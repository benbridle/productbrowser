import configparser
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ldproductbrowser import globals as ldglobal


class BottomBar(QHBoxLayout):
    def __init__(self, database):
        super().__init__()

        database_version, time_created = database.execute("SELECT version, time_created FROM metadata").fetchone()
        config = configparser.ConfigParser()
        config.read(ldglobal.app_context.get_resource("settings.cfg"))
        program_version = config["PROGRAM"]["version"]

        version_label = QLabel(
            f"Program version {program_version}  |  Database version {database_version}  (generated {time_created.split()[0]})"
        )
        version_label.setTextFormat(Qt.PlainText)
        version_label.setStyleSheet("QLabel { color : #444444;}")

        author_label = QLabel(
            '<a href="http://benbridle.com"><span style="color:#aaaaaa; text-decoration:none;">created by Ben Bridle</span></a>'
        )
        author_label.setAlignment(Qt.AlignRight)
        author_label.setOpenExternalLinks(True)
        self.addWidget(version_label)
        self.addWidget(author_label)
