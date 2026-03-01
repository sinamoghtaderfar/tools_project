import os
import tempfile
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import io
from PIL import Image
from pdf2docx import Converter
from PyPDF2 import PdfMerger
import zipfile


def home(request):
    return render(request, 'home.html')


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

            response = HttpResponse(output_io.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
            return response

        # COMPRESS IMAGE
        elif tool_name == "compress-image":
            zip_io = io.BytesIO()

            with zipfile.ZipFile(zip_io, 'w') as zipf:
                for f in uploaded_files:
                    f.seek(0)

                    # Open image file
                    image = Image.open(f)
                    img_io = io.BytesIO()

                    # Save image with compression
                    image.save(img_io, format=image.format or 'JPEG', optimize=True, quality=70)
                    img_io.seek(0)

                    # Add compressed image to ZIP file
                    zipf.writestr(f"compressed_{f.name}", img_io.read())

            zip_io.seek(0)

            response = HttpResponse(zip_io.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="compressed_images.zip"'
            return response

        # CONVERT PDF TO DOCX
        elif tool_name == "convert-pdf":
            zip_io = io.BytesIO()

            with zipfile.ZipFile(zip_io, 'w') as zipf:
                for f in uploaded_files:
                    f.seek(0)

                    # Create temporary file for the uploaded PDF
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                        tmp_pdf.write(f.read())
                        tmp_pdf_path = tmp_pdf.name

                    # Create temporary file for the output DOCX
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
                        tmp_docx_path = tmp_docx.name

                    try:
                        # Convert PDF to DOCX using temporary files
                        cv = Converter(tmp_pdf_path)
                        cv.convert(tmp_docx_path, start=0, end=None)
                        cv.close()

                        # Read the converted DOCX file
                        with open(tmp_docx_path, 'rb') as docx_file:
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

            response = HttpResponse(zip_io.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="converted_files.zip"'
            return response

    # GET request
    return render(request, "tools/tool_page.html", {"tool_name": tool_name})