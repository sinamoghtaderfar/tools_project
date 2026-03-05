import os
import tempfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import io
from PIL import Image
from pdf2docx import Converter
from PyPDF2 import PdfMerger
import zipfile
from django.urls import reverse


def home(request):
    return render(request, "home.html")


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def guest_tool(request, tool_name):
    allowed_tools = ["merge-pdf", "compress-image", "convert-pdf"]

    # If tool_name is not valid
    if tool_name not in allowed_tools:
        tool_name = "merge-pdf"

    if request.method == "POST":
        uploaded_files = request.FILES.getlist("file")

        if not uploaded_files:
            messages.error(request, "Please select at least one file.")
            return render(request, "tools/tool_page.html", {"tool_name": tool_name})

        # Check file sizes
        for f in uploaded_files:
            if f.size > MAX_FILE_SIZE:
                messages.error(request, f"File {f.name} is too large! Max size 5 MB.")
                return render(request, "tools/tool_page.html", {"tool_name": tool_name})

        # MERGE PDF
        if tool_name == "merge-pdf":
            merger = PdfMerger()
            for f in uploaded_files:
                f.seek(0)
                merger.append(f)

            output_io = io.BytesIO()
            merger.write(output_io)
            merger.close()
            output_io.seek(0)

            response = HttpResponse(output_io.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="merged.pdf"'
            return response

        # COMPRESS IMAGE
        elif tool_name == "compress-image":
            zip_io = io.BytesIO()

            with zipfile.ZipFile(zip_io, "w") as zipf:
                for f in uploaded_files:
                    f.seek(0)

                    # Open image file
                    image = Image.open(f)
                    img_io = io.BytesIO()

                    # Save image with compression
                    image.save(
                        img_io, format=image.format or "JPEG", optimize=True, quality=70
                    )
                    img_io.seek(0)

                    # Add compressed image to ZIP file
                    zipf.writestr(f"compressed_{f.name}", img_io.read())

            zip_io.seek(0)

            response = HttpResponse(zip_io.read(), content_type="application/zip")
            response["Content-Disposition"] = (
                'attachment; filename="compressed_images.zip"'
            )
            return response

        # CONVERT PDF TO DOCX
        elif tool_name == "convert-pdf":
            zip_io = io.BytesIO()

            with zipfile.ZipFile(zip_io, "w") as zipf:
                for f in uploaded_files:
                    f.seek(0)

                    # Create temporary file for the uploaded PDF
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp_pdf:
                        tmp_pdf.write(f.read())
                        tmp_pdf_path = tmp_pdf.name

                    # Create temporary file for the output DOCX
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".docx"
                    ) as tmp_docx:
                        tmp_docx_path = tmp_docx.name

                    try:
                        # Convert PDF to DOCX using temporary files
                        cv = Converter(tmp_pdf_path)
                        cv.convert(tmp_docx_path, start=0, end=None)
                        cv.close()

                        # Read the converted DOCX file
                        with open(tmp_docx_path, "rb") as docx_file:
                            docx_content = docx_file.read()

                        # Add DOCX file to ZIP archive
                        docx_name = f"{f.name.rsplit('.',1)[0]}.docx"
                        zipf.writestr(docx_name, docx_content)

                    finally:
                        # Remove temporary files
                        try:
                            os.unlink(tmp_pdf_path)
                            os.unlink(tmp_docx_path)
                        except:
                            pass

            zip_io.seek(0)

            response = HttpResponse(zip_io.read(), content_type="application/zip")
            response["Content-Disposition"] = (
                'attachment; filename="converted_files.zip"'
            )
            return response

    # GET request
    return render(request, "tools/tool_page.html", {"tool_name": tool_name})


TOOLS = {
    "word": {
        "title": "Word Tools",
        "icon": "📝",
        "tools": [
            {
                "name": "word_to_pdf",
                "display": "Word to PDF",
                "url": "word_to_pdf",
                "requires_login": True,
            },
            {
                "name": "word_to_txt",
                "display": "Word to TXT",
                "url": "word_to_txt",
                "requires_login": True,
            },
            {
                "name": "compress_word",
                "display": "Compress Word",
                "url": "compress_word",
                "requires_login": True,
            },
        ],
    },
    "pdf": {
        "title": "PDF Tools",
        "icon": "📄",
        "tools": [
            {
                "name": "convert-pdf",
                "display": "Convert PDF",
                "url": "convert-pdf",
                "requires_login": False,
            },
            {
                "name": "merge-pdf",
                "display": "Merge PDF",
                "url": "merge-pdf",
                "requires_login": False,
            },
            {
                "name": "pdf_to_word",
                "display": "PDF to Word",
                "url": "pdf_to_word",
                "requires_login": True,
            },
            {
                "name": "pdf_to_txt",
                "display": "PDF to TXT",
                "url": "pdf_to_txt",
                "requires_login": True,
            },
            {
                "name": "compress_pdf",
                "display": "Compress PDF",
                "url": "compress_pdf",
                "requires_login": True,
            },
        ],
    },
    "image": {
        "title": "Image Tools",
        "icon": "🖼️",
        "tools": [
            {
                "name": "compress-image",
                "display": "Compress Image",
                "url": "compress-image",
                "requires_login": False,
            },
            {
                "name": "to_jpg",
                "display": "Convert to JPG",
                "url": "to_jpg",
                "requires_login": True,
            },
            {
                "name": "to_png",
                "display": "Convert to PNG",
                "url": "to_png",
                "requires_login": True,
            },
            {
                "name": "to_gif",
                "display": "Convert to GIF",
                "url": "to_gif",
                "requires_login": True,
            },
            {
                "name": "compress_image",
                "display": "Compress Image",
                "url": "compress_image",
                "requires_login": True,
            },
        ],
    },
    "archive": {
        "title": "Archive Tools",
        "icon": "📦",
        "tools": [
            {
                "name": "extract",
                "display": "Extract Archive",
                "url": "extract",
                "requires_login": True,
            },
        ],
    },
    "excel": {
        "title": "Excel Tools",
        "icon": "📊",
        "tools": [
            {
                "name": "to_excel",
                "display": "CSV to Excel",
                "url": "to_excel",
                "requires_login": True,
            },
            {
                "name": "to_csv",
                "display": "Excel to CSV",
                "url": "to_csv",
                "requires_login": True,
            },
        ],
    },
}


def tools_list(request):
    """show tools list with dynamic login labels"""
    tools_categories = TOOLS.copy()
    user_logged_in = request.user.is_authenticated

    for category in tools_categories.values():
        for tool in category["tools"]:
            if tool["requires_login"]:
                if user_logged_in:
                    tool["status_text"] = "Available for you"
                    tool["border_color"] = "border-green-400"
                else:
                    tool["status_text"] = "Login Required"
                    tool["border_color"] = "border-yellow-400"
            else:
                tool["status_text"] = "Free"
                tool["border_color"] = "border-green-400"

    context = {"tools_categories": tools_categories}
    return render(request, "tools/tools_list.html", context)


def tool_page(request, tool_slug):
    tool_data = next(
        (t for c in TOOLS.values() for t in c["tools"] if t["url"] == tool_slug), None
    )
    if not tool_data:
        messages.error(request, "Tool not found.")
        return redirect("tools_list")

    requires_login = tool_data["requires_login"]
    tool_display_name = tool_data["display"]

    if requires_login:
        if not request.user.is_authenticated:
            login_url = f"{reverse('login')}?next={request.path}"
            messages.warning(
                request, f"Please log in to use '{tool_display_name}' tool."
            )
            return redirect(login_url)
        if requires_login and request.user.is_authenticated:
            messages.info(
                request,
                f"'{tool_display_name}' is available for you! Redirecting to dashboard...",
            )
            return redirect("dashboard")

    return guest_tool(request, tool_slug)
