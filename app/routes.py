import os
import uuid
import json
from flask import Blueprint, request, render_template, send_file, flash, redirect, url_for, session
from flask_login import login_required, current_user

from app.parser.docx_parser import parse_docx
from app.generator.html_generator import generate_html
from app.generator.manifest_generator import generate_manifest
from app.packager.scorm_packager import pack_scorm
from app.database import db, Conversion, CourseMetadata

bp = Blueprint("main", __name__)

UPLOAD_FOLDER = "/tmp/scorm_uploads"
OUTPUT_FOLDER = "/tmp/scorm_output"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
XSD_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "xsd")
JS_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "js")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@bp.route("/", methods=["GET"])
@login_required
def index():
    return render_template("upload.html")


@bp.route("/convert", methods=["POST"])
@login_required
def convert():
    if "file" not in request.files:
        flash("Файл не выбран")
        return redirect(url_for("main.index"))

    file = request.files["file"]

    if not file.filename.endswith(".docx"):
        flash("Пожалуйста, загрузите файл формата .docx")
        return redirect(url_for("main.index"))

    # Сохраняем файл
    session_id = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.docx")
    file.save(input_path)

    try:
        parsed = parse_docx(input_path)
    except Exception as e:
        flash(f"Ошибка при чтении файла: {e}")
        return redirect(url_for("main.index"))

    # Сохраняем промежуточные данные в сессию
    # (parsed нельзя положить в сессию напрямую — сериализуем нужное)
    session["session_id"] = session_id
    session["original_filename"] = file.filename
    session["document_title"] = parsed.title

    # Генерируем HTML и сохраняем на диск — он понадобится на следующем шаге
    html = generate_html(parsed, TEMPLATES_DIR)
    html_path = os.path.join(OUTPUT_FOLDER, f"{session_id}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Сохраняем список изображений и сами байты
    images_meta = {}
    for filename, data in parsed.images.items():
        img_path = os.path.join(OUTPUT_FOLDER, f"{session_id}_{filename}")
        with open(img_path, "wb") as f:
            f.write(data)
        images_meta[filename] = img_path
    session["images_meta"] = images_meta

    # Показываем форму метаданных, подставив title как подсказку
    return render_template("metadata.html", suggested_title=parsed.title)


@bp.route("/finalize", methods=["POST"])
@login_required
def finalize():
    session_id = session.get("session_id")
    if not session_id:
        flash("Сессия истекла, загрузите файл заново")
        return redirect(url_for("main.index"))

    # Читаем метаданные из формы — всё необязательно
    title = request.form.get("title", "").strip() or session.get("document_title", "Без названия")
    description = request.form.get("description", "").strip() or None
    author = request.form.get("author", "").strip() or None
    organization = request.form.get("organization", "").strip() or None
    language = request.form.get("language", "ru").strip() or "ru"
    version = request.form.get("version", "1.0").strip() or "1.0"
    keywords = request.form.get("keywords", "").strip() or None

    # Читаем сохранённые данные
    html_path = os.path.join(OUTPUT_FOLDER, f"{session_id}.html")
    images_meta = session.get("images_meta", {})

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Восстанавливаем изображения
    images = {}
    for filename, img_path in images_meta.items():
        with open(img_path, "rb") as f:
            images[filename] = f.read()

    output_path = os.path.join(OUTPUT_FOLDER, f"{session_id}.zip")

    try:
        manifest = generate_manifest(
            title=title,
            images=list(images.keys()),
            templates_dir=TEMPLATES_DIR,
            description=description,
            author=author,
            organization=organization,
            language=language,
            version=version,
            keywords=keywords,
        )
        pack_scorm(html, manifest, images, output_path, xsd_dir=XSD_DIR, js_dir=JS_DIR)

        # Сохраняем конвертацию в БД
        conversion = Conversion(
            original_filename=session.get("original_filename", ""),
            document_title=title,
            status="success",
            user_id=current_user.id,
        )
        db.session.add(conversion)
        db.session.flush()  # чтобы получить conversion.id до commit

        # Сохраняем метаданные в БД
        meta = CourseMetadata(
            user_id=current_user.id,
            conversion_id=conversion.id,
            title=title,
            description=description,
            author=author,
            organization=organization,
            language=language,
            version=version,
            keywords=keywords,
        )
        db.session.add(meta)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при конвертации: {e}")
        return redirect(url_for("main.index"))

    # Чистим сессию
    session.pop("session_id", None)
    session.pop("document_title", None)
    session.pop("original_filename", None)
    session.pop("images_meta", None)

    return send_file(
        output_path,
        as_attachment=True,
        download_name="scorm_package.zip",
        mimetype="application/zip",
    )


@bp.route("/history", methods=["GET"])
@login_required
def history():
    conversions = Conversion.query.filter_by(user_id=current_user.id)\
        .order_by(Conversion.created_at.desc()).all()
    return render_template("history.html", conversions=conversions)