# -*- encoding: utf-8 -*-

"""Implementation of the fundamental concepts of an IMO as database
tables.

This file implements the following classes, which are descendeants of
Django's `models.Model` class and are therefore used to set up tables
in the database:

- `Entity`: a feature of the instrument that is modelled in the
  IMO. Entities can form tree-like structures. Examples: a telescope,
  a cryostat, a focal plane, a beam, etc., where focal planes can be
  parents of several beams.

- `Quantity`: numerical information related to an entity, which must
  conform to some format specification (see below). Examples: a beam
  pattern saved as a Healpix map, a bandpass stored in an Excel file,
  etc.

- `FormatSpecification`: a document that presents the mathematical
  model, the units of measure used, the assumptions, and the file
  format used for files storing a "quantity" (see above)

- `DataFile`: a file containing numerical estimates of some
  "quantity" (see above).

"""

from collections import namedtuple
from pathlib import Path

import uuid
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

from instrumentdb.settings import STORAGE_PATH

FileType = namedtuple("ImageFileType", ["mime_type", "file_extension", "description",])

# List of supported document types (for specification documents).
# Please keep the most useful at the top of the list, then use
# alphabetic order!
DOCUMENT_FILE_TYPES = [
    FileType(mime_type="text/plain", file_extension="txt", description="Plain text"),
    FileType(mime_type="text/html", file_extension="html", description="HTML"),
    FileType(
        mime_type="application/pdf", file_extension="pdf", description="Adobe PDF"
    ),
    FileType(
        mime_type="text/rtf",
        file_extension="rtf",
        description="Rich-Text Format (.rtf)",
    ),
    FileType(mime_type="text/markdown", file_extension="md", description="Markdown"),
    FileType(
        mime_type="application/x-abiword",
        file_extension="abw",
        description="AbiWord document",
    ),
    FileType(
        mime_type="application/msword",
        file_extension="doc",
        description="Microsoft Word (.doc)",
    ),
    FileType(
        mime_type="application/vnd.openxmlformats-officedocument"
        ".wordprocessingml.document",
        file_extension="docx",
        description="Microsoft Word (.docx)",
    ),
    FileType(
        mime_type="application/vnd.amazon.ebook",
        file_extension="azw",
        description="Amazon Kindle eBook",
    ),
    FileType(
        mime_type="application/epub+zip",
        file_extension="epub",
        description="Electronic publication (EPUB)",
    ),
    FileType(
        mime_type="application/vnd.oasis.opendocument.text",
        file_extension="",
        description="OpenDocument text document (.odt)",
    ),
    FileType(
        mime_type="application/vnd.oasis.opendocument.presentation",
        file_extension="odp",
        description="OpenDocument presentation document (.odp)",
    ),
    FileType(
        mime_type="application/vnd.oasis.opendocument.spreadsheet",
        file_extension="ods",
        description="OpenDocument spreadsheet document (.ods)",
    ),
    FileType(
        mime_type="application/vnd.ms-powerpoint",
        file_extension="ppt",
        description="Microsoft PowerPoint (.ppt)",
    ),
    FileType(
        mime_type="application/vnd.openxmlformats-officedocument"
        ".presentationml.presentation",
        file_extension="docx",
        description="Microsoft PowerPoint (.pptx)",
    ),
    FileType(
        mime_type="application/vnd.ms-excel",
        file_extension="xls",
        description="Microsoft Excel (.xls)",
    ),
    FileType(
        mime_type="application/vnd.openxmlformats-officedocument"
        ".spreadsheetml.sheet",
        file_extension="xlsx",
        description="Microsoft Excel (.xlsx)",
    ),
    FileType(
        mime_type="application/octet-stream",
        file_extension="bin",
        description="Other (unknown)",
    ),
]

# List of supported image types (for plots associated with data files)
IMAGE_FILE_TYPES = [
    FileType(mime_type="image/png", file_extension="png", description="PNG image"),
    FileType(mime_type="image/jpeg", file_extension="jpg", description="Jpeg image"),
    FileType(mime_type="image/svg+xml", file_extension="svg", description="SVG image"),
    FileType(mime_type="image/apng", file_extension="apng", description="Animated PNG"),
    FileType(
        mime_type="image/bmp", file_extension="bmp", description="Windows bitmap image"
    ),
    FileType(mime_type="image/gif", file_extension="gif", description="GIF image"),
    FileType(mime_type="image/x-icon", file_extension="ico", description="ICO image"),
    FileType(mime_type="image/tiff", file_extension="tif", description="TIFF image"),
    FileType(mime_type="image/webp", file_extension="webp", description="WebP image"),
    FileType(
        mime_type="application/octet-stream",
        file_extension="bin",
        description="Other (unknown)",
    ),
]

# These dictionaries associate a MIME type with its extension:
# MIME_TO_IMAGE_EXTENSION["image/tiff"] == "tif"
MIME_TO_DOC_EXTENSION = {x.mime_type: x.file_extension for x in DOCUMENT_FILE_TYPES}
MIME_TO_IMAGE_EXTENSION = {x.mime_type: x.file_extension for x in IMAGE_FILE_TYPES}


class Entity(MPTTModel):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        max_length=256, help_text="Descriptive name for this entity"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    ordering = ("name",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "entities"


def format_spec_directory_path(instance, filename):
    # The ".split" trick enables proper treatment of MIME types like
    # "text/markdown; charset=UTF-8", because it removes what comes
    # after the ";"
    ext = MIME_TO_DOC_EXTENSION[instance.doc_mime_type.split(";")[0]]

    true_file_name = instance.doc_file_name
    if not true_file_name:
        true_file_name = ext
    return STORAGE_PATH / "format_spec" / f"{instance.uuid}_{true_file_name}"


class FormatSpecification(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    document_ref = models.CharField(
        "ID of the specification document",
        max_length=64,
        unique=True,
        help_text="ID of the technical document",
    )
    title = models.CharField(
        max_length=256,
        help_text="Title of the document containing the specification "
        + "for a file format",
    )
    doc_file = models.FileField(
        "file containing the specification document",
        null=True,
        blank=True,
        upload_to=format_spec_directory_path,
        help_text="Downloadable copy of the specification document (optional)",
    )
    doc_file_name = models.CharField(
        "name of the file containing the specification document",
        max_length=256,
        null=True,
        blank=True,
        help_text="Name of the file containing the specification document (optional)",
    )
    # Regarding the maximum length of a MIME type, see
    # https://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db
    doc_mime_type = models.CharField(
        "MIME type of the specification document",
        max_length=256,
        choices=[(x.mime_type, x.description) for x in DOCUMENT_FILE_TYPES],
        default=DOCUMENT_FILE_TYPES[0].mime_type,
        help_text="This specifies the MIME type of the downloadable copy "
        + "of the specification document",
    )
    file_mime_type = models.CharField(
        "MIME type of the file",
        max_length=256,
        help_text="This specifies the MIME type of the data file",
    )

    def __str__(self):
        if self.title:
            return f'{self.document_ref} ("{self.title}")'
        else:
            return f"{self.document_ref}"


class Quantity(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        max_length=256, help_text="Descriptive name for this quantity"
    )
    format_spec = models.ForeignKey(
        FormatSpecification,
        on_delete=models.CASCADE,
        related_name="quantities",
        help_text="Reference to the format specification used for data files "
        + "associated with this quantity",
    )
    parent_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="quantities",
        help_text="Entity to whom this quantity is related",
    )

    ordering = (
        "name",
        "uuid",
    )

    def __str__(self):
        return f"{self.name} ({str(self.uuid)[0:8]})"

    class Meta:
        verbose_name_plural = "quantities"


def data_file_directory_path(instance, filename):
    return STORAGE_PATH / "data_files" / f"{instance.uuid}_{instance.name}"


def plot_file_directory_path(instance, filename):
    ext = MIME_TO_IMAGE_EXTENSION[instance.plot_mime_type.split(";")[0]]
    return STORAGE_PATH / "plot_files" / f"{instance.uuid}_{instance.name}.{ext}"


class DataFile(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        "file name", max_length=1024, default="noname", help_text="Name of the file"
    )
    upload_date = models.DateTimeField(
        "date when the file was uploaded",
        default=timezone.now,
        editable=False,
        help_text="Date when the file was added to the database",
    )
    metadata = models.TextField(
        "JSON-formatted metadata",
        max_length=8192,
        blank=True,
        help_text="JSON record containing metadata for the file",
    )
    file_data = models.FileField(
        "File",
        blank=True,
        upload_to=data_file_directory_path,
        help_text="File contents (when present)",
    )
    quantity = models.ForeignKey(
        Quantity,
        on_delete=models.CASCADE,
        related_name="data_files",
        help_text="Quantity associated with the data in this file",
    )
    spec_version = models.CharField(
        "version of the specification document",
        max_length=32,
        help_text="Version number of the format specification document",
    )
    dependencies = models.ManyToManyField(
        "DataFile",
        blank=True,
        help_text="List of data files that have been used as inputs to "
        + "produce this data file",
    )
    plot_file = models.FileField(
        "Image file",
        blank=True,
        upload_to=plot_file_directory_path,
        help_text="Plot of the data in the file (optional)",
    )
    plot_mime_type = models.CharField(
        "MIME type of the image",
        max_length=256,
        blank=True,
        null=True,
        choices=[(x.mime_type, x.description) for x in IMAGE_FILE_TYPES],
        default=None,
        help_text="This specifies the MIME type of the image",
    )

    comment = models.TextField(max_length=4096, blank=True, help_text="Free-form notes")

    # When querying *all* the DataFile objects in a database, the
    # (inverse) order by upload date will not be very meaningful… But
    # usually we query only for DataFile objects related to some
    # specific quantity, and in this case the ordering is what we
    # would expect: the first object is the most recent one!
    ordering = (
        "-upload_date",
        "name",
        "uuid",
    )

    def __str__(self):
        return f"{self.name} ({str(self.uuid)[0:8]})"
