from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserFile
import os
from django.conf import settings

from docx import Document
from fpdf import FPDF
from PIL import Image
import pandas as pd
import zipfile
import uuid

from django.http import FileResponse, Http404
@login_required
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            UserFile.objects.create(
                user=request.user,
                original_name=uploaded_file.name,
                file=uploaded_file,
            )

    return redirect("dashboard")


@login_required
def dashboard(request):
    files = UserFile.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"files": files})


@login_required
def process_tool(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id, user=request.user)

    if request.method == "POST":
        tool_type = request.POST.get("tool_type")
        user_file.tool_type = tool_type

        input_path = user_file.file.path
        name, ext = os.path.splitext(user_file.file.name)
        ext = ext.lower()

        
        output_dir = os.path.join(settings.MEDIA_ROOT, 'outputs', f'user_{request.user.id}')
        os.makedirs(output_dir, exist_ok=True)

        output_name = str(uuid.uuid4())
        converted_path = ""

        # ---------------- Word ----------------
        if ext in [".doc", ".docx"]:
            doc = Document(input_path)
            if tool_type == "word_to_pdf":
                pdf = FPDF()
                pdf.add_page()
                for para in doc.paragraphs:
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 8, para.text)
                converted_path = os.path.join(output_dir, f"{output_name}.pdf")

            elif tool_type == "word_to_txt":
                converted_path = os.path.join(output_dir, f"{output_name}.txt")
                with open(converted_path, "w", encoding="utf-8") as f:
                    for para in doc.paragraphs:
                        f.write(para.text + "\n")

            elif tool_type == "compress_word":
                converted_path = os.path.join(output_dir, f"{output_name}.zip")
                with zipfile.ZipFile(converted_path, 'w') as zipf:
                    zipf.write(input_path, arcname=os.path.basename(input_path))

        # ---------------- PDF ----------------
        elif ext == ".pdf":
            if tool_type == "pdf_to_word":
                converted_path = os.path.join(output_dir, f"{output_name}.txt")
                with open(converted_path, "wb") as f:
                    f.write(b"PDF to Word placeholder")

            elif tool_type == "pdf_to_txt":
                converted_path = os.path.join(output_dir, f"{output_name}.txt")
                with open(converted_path, "wb") as f:
                    f.write(b"PDF to TXT placeholder")

            elif tool_type == "compress_pdf":
                converted_path = os.path.join(output_dir, f"{output_name}.zip")
                with zipfile.ZipFile(converted_path, 'w') as zipf:
                    zipf.write(input_path, arcname=os.path.basename(input_path))

        # ---------------- Image ----------------
        elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
            img = Image.open(input_path)

            if tool_type == "to_jpg":
                converted_path = os.path.join(output_dir, f"{output_name}.jpg")
                img.convert("RGB").save(converted_path, "JPEG")
            elif tool_type == "to_png":
                converted_path = os.path.join(output_dir, f"{output_name}.png")
                img.convert("RGB").save(converted_path, "PNG")
            elif tool_type == "to_gif":
                converted_path = os.path.join(output_dir, f"{output_name}.gif")
                img.convert("RGB").save(converted_path, "GIF")
            elif tool_type == "compress_image":
                converted_path = os.path.join(output_dir, f"{output_name}.zip")
                with zipfile.ZipFile(converted_path, 'w') as zipf:
                    zipf.write(input_path, arcname=os.path.basename(input_path))

        # ---------------- Archive ----------------
        elif ext in [".zip", ".rar", ".7z"]:
            if tool_type == "extract":
                extract_dir = os.path.join(output_dir, f"{output_name}_extracted")
                os.makedirs(extract_dir, exist_ok=True)
                with zipfile.ZipFile(input_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                converted_path = ""  # لینک دانلود برای فولدر فعلاً نمی‌دهیم

        # ---------------- CSV ----------------
        elif ext == ".csv":
            if tool_type == "to_excel":
                df = pd.read_csv(input_path)
                converted_path = os.path.join(output_dir, f"{output_name}.xlsx")
                df.to_excel(converted_path, index=False)

        # ---------------- Excel ----------------
        elif ext in [".xls", ".xlsx"]:
            if tool_type == "to_csv":
                df = pd.read_excel(input_path)
                converted_path = os.path.join(output_dir, f"{output_name}.csv")
                df.to_csv(converted_path, index=False, encoding="utf-8")

        # ---------------- Other ----------------
        else:
            pass

        # ---------------- Save converted file ----------------
        if converted_path and os.path.isfile(converted_path):
            relative_path = os.path.relpath(converted_path, settings.MEDIA_ROOT)
            user_file.converted_file.name = relative_path
            user_file.save()

    return redirect("dashboard")


@login_required
def download_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id, user=request.user)

    if not user_file.converted_file:
        raise Http404("File not found")

    file_path = user_file.converted_file.path
    if os.path.exists(file_path):
        # Force download
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        raise Http404("File not found")