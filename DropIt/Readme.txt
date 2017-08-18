
  DropIt (v8.4)
-----------------------------

Personal Assistant to Automatically Manage Your Files

Website: http://www.dropitproject.com/
Contact: http://www.lupopensuite.com/contact.htm

Software realized by Lupo PenSuite Team.
Released under Open Source GPL.




  Introduction
-----------------------------

DropIt is a simple floating target image that you can drop files onto
to quickly process them with the action of your choice.

DropIt allows to define a destination for each rule created
and group several associations in different profiles.

Read the official "Guide.pdf" for more information.




  Acknowledgements
-----------------------------

These are the developers that collaborate to create DropIt:
- Lupo73 (author and main developer)
- divinity666 (developer)
- tproli (website and html features designer)
- guinness (developer)

These are the included components and related authors:
- 7-Zip archiver by Igor Pavlov
- Copy library by Yashied
- Crystal Clear icons by Everaldo
- Crystal Project icons by Everaldo
- Gallery Lightbox by fancyBox
- Gallery Themes by tpr
- HTML Lightbox by Transcendent Design
- HTML Sortable Table by webtoolkit.info
- HTML Themes by tpr
- Nuove XT icons by Saki
- Oxygen icons by Oxygen Team
- PDFToText tool by Xpdf Team
- PSFTP tool by PuTTY Team
- Sounds by SoundJay.com
- USB icon by webdesignerdepot.com
- Vista Inspirate icons by Saki

And a big thanks to all translators!




  ChangeLog
-----------------------------

Version 8.4 [23-07-2017]
- added "Print" action (using default system applications based on file formats)
- added %Pages% abbreviation to read the number of pages of a document
- added %YearWeekCreated%, %YearWeekModified%, %YearWeekOpened%, %YearWeekTaken% abbreviations
- added option to configure FirstFileContentDate abbreviations for different languages (read 5.6 of the Guide)
- updated the internal tool to manage archives (7z v16.04)
- fixed ++ and -- modifiers to work properly with all Unicode characters
- fixed some abbreviations that use Windows Explorer information to work on Windows Vista/8.1/10
- fixed support to use pipe symbol in regular expressions in Additional Filters
- fixed some minor bugs

Previous Versions:
http://www.dropitproject.com/changelog.txt

Known Limits:
- "Create Gallery" action does not keep Exif data of resized images
- "Encrypt" action does not rename processed files after the first duplicate
- "Send by Mail" action fails if the file exceed the server size limit or the format is not authorized
- DropIt may fail to search strings in PDF files generated with OCR
- DropIt may stop working after 24-48 hours of folder monitoring




-----------------------------