from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from ldproductbrowser.tools import image_tools


class ImageWidget(QLabel):
    """
    Custom widget that provides a simple interface for displaying images at a
    specified size.
    """

    def __init__(self, width, height):
        super().__init__()
        self.setSize(width, height)
        self.fallback_image = None
        self.image = None

    def setSize(self, width, height):
        self.setFixedSize(QSize(width, height))

    def setImage(self, image_bytes, alpha=False):
        """
        Process the given image and use it as the main image for the widget,
        and then update the image display.
        """
        if image_bytes is None:
            self.image = None
        else:
            if alpha:
                value = 0
            else:
                value = 255
            self.image = self._scale_image_over_colour(image_bytes, (255, 255, 255, value))
        self._update_display()

    def setFallbackImage(self, image_bytes):
        """
        Set and process a fallback image that will be displayed if the given image is invalid
        """
        self.fallback_image = self._scale_image_over_colour(image_bytes, (255, 255, 255, 0))

    def _update_display(self):
        """
        Set the Pixmap of this widget to display the most appropriate image.
        """
        product_pixmap = QPixmap()
        if self.image:
            product_pixmap.loadFromData(self.image)
        else:
            product_pixmap.loadFromData(self.fallback_image)
        self.setPixmap(product_pixmap)

    def getSize(self):
        """
        Return the size of the widget in pixels as an (x,y) tuple
        """
        width = self.size().width()
        height = self.size().height()
        return width, height

    def get_fallback_image(self):
        """
        Validate and return fallback image.
        """
        if self.fallback_image is None:
            raise ValueError("A fallback image has not been set")
        return self.fallback_image

    def _scale_image_over_colour(self, image_bytes, colour=(255, 255, 255, 0)):
        image = image_tools.convert_bytes_to_pil_image(image_bytes)
        width, height = self.getSize()
        image = image_tools.superimpose_image_on_background(image, width, height, colour)
        image_bytes = image_tools.convert_pil_image_to_bytes(image)
        return image_bytes
