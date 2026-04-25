from collections import OrderedDict

from PySide6.QtCore import Qt, QSizeF, QRect, QPoint, QSize
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

PDF_POINT = 72  # PDF document measurements are in points (1/72 of an inch)

class MyPdfView(QPdfView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._highlight = {}
        # Calculate the ratio between screen resolution and PDF resolution
        self._logicalScale = QApplication.primaryScreen().logicalDotsPerInch() / PDF_POINT

        self.documentChanged.connect(self.updateDocumentLayout)

        self.doc = self.document()

        self.documentLayout = OrderedDict()

    # Clear the document layout information
    def clearLayout(self)->None:
        self._highlight.clear()
        self.documentLayout.clear()
    
    # Takes a dict of bounding box data, updates the document layout, and updates the viewport
    # in order to draw the bounding box.
    def setLayout(self, layout:dict)->None:
        self._highlight.clear()
        self._highlight.update(layout)
        self.updateDocumentLayout()
        self.viewport().update()

    # Returns the currently displayed PDF page.
    def CurrentPage(self)->int:
        return self._highlight["page_no"]-1
    
    # Updates the document layout if the status of the PDF file changes.
    def documentStatusChanged(self, status)->None:
        if status == QPdfDocument.Status.Ready:
            self.updateDocumentLayout()

    # updateDocumentLayout source - https://stackoverflow.com/a/79231842
    # See that link for an explanation of this method.
    def updateDocumentLayout(self):
        self.documentLayout.clear()
        self.doc = self.document()

        if self.doc is None:
            return
        elif self.doc.status() != QPdfDocument.Status.Ready:
            # the document may have just been changed, so we need to 
            # connect its statusChanged signal, but only once
            try:
                self.doc.statusChanged.connect(
                    self.documentStatusChanged, 
                    Qt.ConnectionType.UniqueConnection
                )
            except TypeError:
                # older PyQt/PySide versions may raise a TypeError whenever a
                # UniqueConnection fails
                pass

            # if a new document has been set but the previous one still 
            # exists and has a status change, it may still trigger this 
            # function, therefore we will try to disconnect it
            sender = self.sender()
            if self.doc != sender and isinstance(sender, QPdfDocument):
                try:
                    sender.statusChanged.disconnect(
                        self.documentStatusChanged)
                except TypeError:
                    pass
            return
        
        screenRes = QApplication.primaryScreen().logicalDotsPerInch() / 72
        viewSize = self.viewport().size()
        viewWidth = viewSize.width()
        spacing = self.pageSpacing()

        margins = self.documentMargins()
        left = margins.left()
        right = margins.right()
        pageY = margins.top()

        totalWidth = 0

        if self.pageMode() == self.PageMode.SinglePage:
            pageRange = range(
                self.pageNavigator.currentPage(), 
                self.pageNavigator.currentPage() + 1
            )
        else:
            pageRange = range(
                0, self.doc.pageCount()
            )

        zoomMode = self.zoomMode()
        zoomFactor = self.zoomFactor()
        sizeFunc = self.doc.pagePointSize

        for page in pageRange:
            origSize = sizeFunc(page)
            pageScale = zoomFactor
            if zoomMode == self.ZoomMode.Custom:
                pageSize = QSizeF(origSize * screenRes * zoomFactor).toSize()
            elif zoomMode == self.ZoomMode.FitToWidth:
                pageSize = QSizeF(origSize * screenRes).toSize()
                pageScale = (viewWidth - left - right) / pageSize.width()
                pageSize *= pageScale
            else:
                vsize = QSize(viewSize - QSize(left + right, spacing))
                pageSize = QSizeF(origSize * screenRes).toSize()
                scaledSize = pageSize.scaled(
                    vsize, Qt.AspectRatioMode.KeepAspectRatio)
                pageScale = scaledSize.width() / pageSize.width()
                pageSize = scaledSize

            if pageSize.width() > totalWidth:
                totalWidth = pageSize.width()

            self.documentLayout[page] = (
                QRect(QPoint(0, pageY), pageSize), 
                pageScale
            )
            pageY += pageSize.height() + spacing

        totalWidth += left + right

        # horizontally center each page based on the totalWidth
        for pageRect, _ in self.documentLayout.values():
            pageRect.moveLeft(
                (max(totalWidth, viewWidth) - pageRect.width()) // 2)
    
    # The paint event displays the bounding box around the PDF text.
    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.documentLayout:
            return

        # Get the parameters of the QPdfView viewport
        viewRect = QRect(
            self.horizontalScrollBar().value(), 
            self.verticalScrollBar().value(), 
            self.viewport().width(), 
            self.viewport().height()
        )

        bottom = viewRect.bottom()
        
        # Create a paint object to draw the bounding box
        painter = QPainter(self.viewport())
        painter.setPen(QColor(Qt.red))
        painter.setBrush(QColor(255, 0, 0, 25)) # Semi-transparent red fill
        painter.translate(-viewRect.x(), -viewRect.y())

        if self._highlight:
            pageRect, scale = self.documentLayout[self._highlight["page_no"]-1]
            if not pageRect.intersects(viewRect):
                if pageRect.y() > bottom:
                    # the page is beyond the viewport bottom, there is no 
                    # need to go further
                    return
            # Convert the information returned by SpaCy Layout (in points)
            # into pixels and draw the bounding box.
            painter.drawRect(pageRect.x() + (self._highlight["x"] * self._logicalScale) * scale,
                            pageRect.y() + (self._highlight["y"] * self._logicalScale) * scale,
                            (self._highlight["width"] * self._logicalScale) * scale,
                            (self._highlight["height"] * self._logicalScale) * scale)
        
        painter.end()
