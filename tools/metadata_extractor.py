import os
from datetime import datetime
from pathlib import Path

from services import Colors

# Imagens
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# PDF
from PyPDF2 import PdfReader

# DOCX
from docx import Document

# Mime detection
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


class FileMetadataExtractor:
    """
    HackTools -> File Metadata Extractor
    Extracts metadata from images (EXIF), PDF, DOCX, and other files.
    """

    @staticmethod
    def extract(file_path: str):
        if not os.path.exists(file_path):
            print(Colors.RED + "[!] File not found." + Colors.END)
            return None

        mime = FileMetadataExtractor.detect_file_type(file_path)

        print(Colors.BLUE + f"\n[+] File Detected: {mime}" + Colors.END)

        if mime.startswith("image"):
            return FileMetadataExtractor.extract_image_metadata(file_path)

        elif mime == "application/pdf":
            return FileMetadataExtractor.extract_pdf_metadata(file_path)

        elif mime in (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ):
            return FileMetadataExtractor.extract_docx_metadata(file_path)

        else:
            return FileMetadataExtractor.basic_file_info(file_path)

    @staticmethod
    def detect_file_type(path):
        if HAS_MAGIC:
            return magic.from_file(path, mime=True)
        # fallback: guess by extension
        ext = Path(path).suffix.lower()
        if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
            return "image"
        if ext == ".pdf":
            return "application/pdf"
        if ext == ".docx":
            return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        return "unknown"

    @staticmethod
    def extract_image_metadata(path):
        print(Colors.GREEN + "[+] Extracting EXIF metadata (image)..." + Colors.END)
        metadata = {}

        img = Image.open(path)
        exif = img.getexif()

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = value

            # GPS contains nested tags
            if tag == "GPSInfo":
                gps_data = {}
                for gps_id in value:
                    gps_tag = GPSTAGS.get(gps_id, gps_id)
                    gps_data[gps_tag] = value[gps_id]
                metadata["GPSInfo"] = gps_data

        FileMetadataExtractor.pretty_print(metadata)
        return metadata

    @staticmethod
    def extract_pdf_metadata(path):
        print(Colors.GREEN + "[+] Extracting PDF metadata..." + Colors.END)
        metadata = {}

        pdf = PdfReader(path)
        info = pdf.metadata
        #print(info)

        for key, val in info.items():
            metadata[key.replace("/", "")] = val

        FileMetadataExtractor.pretty_print(metadata)
        return metadata

    @staticmethod
    def extract_docx_metadata(path):
        print(Colors.GREEN + "[+] Extracting DOCX metadata..." + Colors.END)
        metadata = {}

        doc = Document(path)
        core = doc.core_properties

        doc_attrs = [
            "author", "title", "subject", "comments", "keywords",
            "last_modified_by", "created", "modified", "revision"
        ]

        for attr in doc_attrs:
            metadata[attr] = getattr(core, attr, None)

        FileMetadataExtractor.pretty_print(metadata)
        return metadata

    @staticmethod
    def basic_file_info(path):
        print(Colors.GREEN + "[+] Extracting basic file info..." + Colors.END)
        stat = os.stat(path)

        metadata = {
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
        }

        FileMetadataExtractor.pretty_print(metadata)
        return metadata

    @staticmethod
    def pretty_print(metadata: dict):
        print(Colors.CYAN + "\n=== METADATA ===" + Colors.END)
        if not metadata:
            print(Colors.RED + "No metadata found." + Colors.END)
            return
        for k, v in metadata.items():
            print(f"{Colors.GREEN}{k}{Colors.END}: {v}")
