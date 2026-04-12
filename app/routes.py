import os
import uuid
from flask import Blueprint, request, render_template, send_file, flash, redirect, url_for

from app.parser.docx_parser import parse_docx
from app.generator.html_generator import generate_html
from app.generator.manifest_generator import generate_manifest
from app.packager.scorm_packager import pack_scorm
from app.database import db, Conversion          # ← новый импорт

bp = Blueprint("main", __name__)

UPLOAD_FOLDER = "/tmp/scorm_uploads"
OUTPUT_FOLDER = "/tmp/scorm_output"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@bp.route("/", methods=["GET"])
def index():
    return render_template("upload.html")


@bp.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        flash("Файл не выбран")
        return redirect(url_for("main.index"))

    file = request.files["file"]

    if not file.filename.endswith(".docx"):
        flash("Пожалуйста, загрузите файл формата .docx")
        return redirect(url_for("main.index"))

    session_id = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.docx")
    output_path = os.path.join(OUTPUT_FOLDER, f"{session_id}.zip")
    file.save(input_path)

    try:
        # Конвейер конвертации
        parsed = parse_docx(input_path)
        html = generate_html(parsed, TEMPLATES_DIR)
        manifest = generate_manifest(parsed.title, list(parsed.images.keys()), TEMPLATES_DIR)
        pack_scorm(html, manifest, parsed.images, output_path)

        # ← Записываем успешную конвертацию в БД
        record = Conversion(
            original_filename=file.filename,
            document_title=parsed.title,
            status="success",
        )
        db.session.add(record)
        db.session.commit()

    except Exception as e:
        # ← Записываем ошибку в БД
        record = Conversion(
            original_filename=file.filename,
            document_title=None,
            status="error",
            error_message=str(e),
        )
        db.session.add(record)
        db.session.commit()

        flash(f"Ошибка при конвертации: {e}")
        return redirect(url_for("main.index"))

    return send_file(
        output_path,
        as_attachment=True,
        download_name="scorm_package.zip",
        mimetype="application/zip",
    )


@bp.route("/history", methods=["GET"])
def history():
    """Страница с историей всех конвертаций."""
    conversions = Conversion.query.order_by(Conversion.created_at.desc()).all()
    return render_template("history.html", conversions=conversions)