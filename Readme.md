# Semantic Search Using SBERT

This application uses [SBERT](https://arxiv.org/abs/1908.10084) to demonstrate semantic searching of a PDF document. The document is loaded and parsed by the [Docling](https://www.docling.ai/)-based [SpaCy Layout](https://github.com/explosion/spacy-layout) package, with parsed data saved in a [json](https://en.wikipedia.org/wiki/JSON) file.

The user enters a query into the text box. The query text is executed by SBERT, using the parsed contents of the json file as the document corpus, with results displayed in the Query Results table. When an item in the table is selected, the PDF file jumps to the appropriate page and the selected text is highlighted with a bounding box (Figure 1).



![Application Layout](screenshots/SSApp_Layout%20(72%20DPI).png "SSApp_Layout (72 DPI).png")

Figure 1. Application layout.

# JSON File

Each entry in the json file is dictionary composed of two elements (Table 1),

- **layout**: Includes bounding box coordinates for the associated text and the page on which the text is located. Bounding box coordinates obtained from SpaCy Layout are in points (1/72 inch) not pixels.
- **text**: The content of each labelled ‘text’ span in the PDF. The parsing of PDF files is notoriously difficult and, while Docling generally does an excellent job, note that it is unable to resolve the presence of ‘fi’ ligatures in the text.

Each entry is a document in the SBERT analysis

---

`{`

` "layout":{`

`"height":79.235,`

`"page_no":2,`

`"width":360.021,`

`"x":56.692, "y":236.524`

` },`

`"text":"An important distinction is the one between attempts to identify (and often also measure) fossil fuel subsidies that rely on an inventory approach and those that rely on a price-gap approach. These two approaches depend implicitly or explicitly on different de /uniFB01 nitions of fossil fuel subsidies, for example, the price-gap approach relies on de /uniFB01 nitions of fossil fuel subsidies that de /uniFB01 ne such subsidies in terms of prices being below a given benchmark."`

`}`

---

Table 1. Example entry in json file with layout information and associated text.

# Application Layout

The application has three parts (),

- **Query entry box**: Allows the user to enter an unstructured query string. Pressing *Enter* or clicking the *Search* button starts the SBERT analysis of the text.
- **Query Results table**: Each entry in the table is composed of the cosine similarity score for the document and the first seven (7) words of the document. The table is sorted by similarity score and scores less than zero (0.0) are not displayed.
- **PDF viewer**: A sub-classed [QPdfView](https://doc.qt.io/qtforpython-6/PySide6/QtPdfWidgets/QPdfView.html) which displays the PDF file and handles the display of the bounding box for the entry selected in the Query Results table.

# Menu and Bars

Structure of the File menu, toolbar and status bar.

## File menu

- Open PDF: Opens a [QFileDialog](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QFileDialog.html) that allows the user to select a PDF file. The selected file is processed by SpaCy Layout and a json file with the same file name as the PDF is created in the directory where the PDF is located.
- Recent Files: A list of recently opened files, displaying a maximum of ten (10) files. Selecting a file from the list displays the PDF file and opens the associated json file used for query processing.
- Close: Closes the application

## Toolbar

The toolbar contains two icons,

- : Open a PDF file. Same as selecting Open PDF from the menu.
- : Close. Same as selecting Close from the menu.

## Status Bar

Displays the file path and file name of the currently open PDF file.
