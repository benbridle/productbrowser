from PyQt5.QtWidgets import (
    QVBoxLayout,
    QScrollArea,
    QSizePolicy,
    QWidget,
    QPushButton,
)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from ldproductbrowser.models import Product
from ldproductbrowser.views import ImageWidget, BetterLabel, StockWidgetBrief
from ldproductbrowser import globals as ldglobal


class ProductPane(QScrollArea):
    """
    A vertical scrolling widget for displaying information about a single product.
    """

    returnPressed = pyqtSignal()

    def __init__(self, width):
        super().__init__()

        self.width = width
        self._hide_scrollbars()
        self._initialise_widgets()
        self.setWidgetResizable(True)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        product_layout = QVBoxLayout()

        product_layout.addWidget(self.image_widget)
        product_layout.addWidget(self.name_label)
        product_layout.addWidget(self.sku_label)
        product_layout.addSpacing(10)
        product_layout.addWidget(self.website_button)
        product_layout.addWidget(self.sdoc_button)
        product_layout.addWidget(self.info_button)
        product_layout.addSpacing(20)
        product_layout.addWidget(self.stock_widget_brief)
        product_layout.addWidget(self.eol_label)
        product_layout.addSpacing(10)
        product_layout.addWidget(self.description_label)
        product_layout.addSpacing(15)
        product_layout.addWidget(self.suggestion_button)
        product_layout.addStretch()

        with open(ldglobal.app_context.get_resource("images/blank_image.png"), "rb") as image_bytes:
            self.blank_image = image_bytes.read()
        self.setProduct(None)

        w = QWidget()
        w.setLayout(product_layout)
        self.setWidget(w)

        with open(ldglobal.app_context.get_resource("images/no_image.png"), "rb") as image_bytes:
            self.setFallbackImage(image_bytes.read())

    def _hide_scrollbars(self):
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")

    def _initialise_widgets(self):
        """
        self.image_widget
        self.name_label
        self.sku_label
        self.website_button
        self.sdoc_button
        self.info_button
        self.description_label
        self.suggestion_button
        self.stock_widget_brief
        """

        self.image_widget = ImageWidget(self.width, self.width)

        self.name_label = BetterLabel("").setBold(True).setFontSize(20)
        self.name_label.setFixedWidth(self.width)
        self.name_label.setMinimumHeight(50)
        self.name_label.setAlignment(Qt.AlignTop)

        self.sku_label = BetterLabel("").setBold(True).setFontSize(18)
        self.sku_label.setFixedWidth(self.width)

        self.website_button = UrlButton("View on website", "Not on website")
        self.sdoc_button = UrlButton("Open SDoC", "No SDoC found")
        self.info_button = UrlButton("View information PDF", "No information PDF")

        self.stock_widget_brief = StockWidgetBrief()
        self.stock_widget_brief.setFixedWidth(self.width)
        self.stock_widget_brief.setFixedHeight(60)

        self.eol_label = BetterLabel("END OF LINE").setBold(True).setFontSize(18)
        self.eol_label.setStyleSheet("QLabel {color: #ffffff; background-color: #ff9084; padding: 2px;}")
        self.eol_label.setFixedWidth(self.width)
        self.eol_label.setAlignment(Qt.AlignHCenter)
        sp = self.eol_label.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.eol_label.setSizePolicy(sp)

        self.description_label = BetterLabel("").setFontSize(14)
        self.description_label.setFixedWidth(self.width)
        self.description_label.setFixedWidth(self.width)
        self.description_label.setTextFormat(Qt.PlainText)

        self.suggestion_button = QPushButton("Suggest a correction...")
        self.suggestion_button.setDisabled(True)

    def updateText(self):
        self.name_label.setText(self.product.name)
        self.sku_label.setText(f"SKU #{self.product.sku}")
        long_text = ""
        try:
            long_text += "Description:\n" + self.product.description + "\n\n"
        except TypeError:
            pass
        try:
            long_text += "Specifications:\n" + self.product.specifications + "\n\n"
        except TypeError:
            pass
        try:
            long_text += "Features:\n" + self.product.features + "\n\n"
        except TypeError:
            pass
        try:
            long_text += "Applications:\n" + self.product.applications + "\n\n"
        except TypeError:
            pass
        while long_text.endswith("\n"):
            long_text = long_text[:-1]
        self.description_label.setText(long_text)
        if len(long_text) > 0:
            self.suggestion_button.show()
        else:
            self.suggestion_button.hide()

    def _hide_display(self):
        self.name_label.setText("")
        self.sku_label.setText("")
        self.description_label.setText("")
        self.info_button.hide()
        self.website_button.hide()
        self.sdoc_button.hide()
        self.image_widget.setImage(self.blank_image, alpha=True)
        self.suggestion_button.hide()
        self.stock_widget_brief.hide()
        self.eol_label.setVisible(False)

    def setProduct(self, product: Product):
        if product is None:
            self._hide_display()
            return
        self.info_button.show()
        self.website_button.show()
        self.sdoc_button.show()
        self.stock_widget_brief.show()

        self.product = product
        self.setImage(product.image)
        self.updateText()
        self._update_buttons()
        self.website_button.setUrl(product.website_url)
        self.info_button.setUrl(product.product_page_url)
        self.sdoc_button.setUrl("file:///" + str(product.sdoc_path))
        self.stock_widget_brief.set_product(product)
        self.updateEOL()
        product.stock_enquiry.updated.connect(self.updateEOL)
        product.stock_enquiry.soft_refresh()

    def updateEOL(self):
        self.setEOL(self.product.stock_enquiry.stock.eol)

    def setEOL(self, state):
        self.eol_label.setVisible(state)

    def setImage(self, image_bytes):
        self.image_widget.setImage(image_bytes)

    def setFallbackImage(self, image_bytes):
        self.image_widget.setFallbackImage(image_bytes)

    def _update_buttons(self):
        self.website_button.setDisabled(self.product.website_url is None)
        self.sdoc_button.setDisabled(self.product.sdoc_path is None)

    def keyPressEvent(self, e):
        if e.text() == "\r":
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)


def make_bg_visible(widget, colour=Qt.red):
    widget.setAutoFillBackground(True)
    p = widget.palette()
    p.setColor(widget.backgroundRole(), colour)
    widget.setPalette(p)


class GoToButton(QPushButton):
    def __init__(self, enabled_text, disabled_text):
        super().__init__(enabled_text)
        self.enabled_text = enabled_text
        self.disabled_text = disabled_text

    def setDisabled(self, state):
        super().setDisabled(state)
        if not state:
            self.setText(self.enabled_text)
        else:
            self.setText(self.disabled_text)


class UrlButton(GoToButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.clicked.connect(self._on_click)

    def setUrl(self, url):
        self.url = url

    def _on_click(self, *args):
        url = QUrl(self.url)
        QDesktopServices.openUrl(url)

