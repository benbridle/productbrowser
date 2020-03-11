from PyQt5.QtWidgets import QDialog, QSizePolicy, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QCursor
from ldproductbrowser.views import BetterLabel, ImageWidget
from ldproductbrowser import globals as ldglobal


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        program_version = ldglobal.settings["PROGRAM"]["version"]

        expanding_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        icon_label = ImageWidget(100, 100)
        with open(ldglobal.app_context.get_resource("images/icon.png"), "rb") as image_bytes:
            icon_label.setImage(image_bytes.read())
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(icon_label)

        app_name_label = BetterLabel("Product Browser").setFontSize(30).setBold(True)
        app_name_label.setWordWrap(False)
        app_name_label.setAlignment(Qt.AlignHCenter)
        app_name_label.setSizePolicy(expanding_policy)
        version_label = BetterLabel(f"version {program_version}").setFontSize(20)
        version_label.setWordWrap(False)
        version_label.setAlignment(Qt.AlignHCenter)
        version_label.setSizePolicy(expanding_policy)
        description = "A product information browser that consolidates and displays diverse product data from a variety of sources."
        description_label = BetterLabel(description).setFontSize(14)
        description_label.setAlignment(Qt.AlignHCenter)
        description_label.setSizePolicy(expanding_policy)
        description_label.setFixedWidth(500)
        description_layout = QHBoxLayout()
        description_layout.addWidget(description_label)
        written_in_label = BetterLabel("Written in Python using Qt and SQLite3").setFontSize(14)
        written_in_label.setAlignment(Qt.AlignHCenter)
        written_in_label.setSizePolicy(expanding_policy)
        author_label = BetterLabel("Created by Ben Bridle, 2020").setFontSize(14)
        author_label.clicked.connect(self.open_author_website)
        author_label.setAlignment(Qt.AlignHCenter)
        author_label.setSizePolicy(expanding_policy)
        author_label.setCursor(QCursor(Qt.PointingHandCursor))
        # author_label.setMinimumWidth(200)
        author_label.setWordWrap(False)
        author_layout = QHBoxLayout()
        author_layout.addStretch()
        author_layout.addWidget(author_label)
        author_layout.addStretch()

        vbox = QVBoxLayout()
        vbox.addSpacing(20)
        vbox.addLayout(icon_layout)
        vbox.addWidget(app_name_label)
        vbox.addWidget(version_label)
        vbox.addSpacing(10)
        vbox.addLayout(description_layout)
        vbox.addSpacing(10)
        vbox.addWidget(written_in_label)
        vbox.addLayout(author_layout)
        vbox.addSpacing(10)
        vbox.setAlignment(Qt.AlignCenter)

        vbox.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(vbox)

    def open_author_website(self):
        QDesktopServices.openUrl(QUrl("http://benbridle.com"))
