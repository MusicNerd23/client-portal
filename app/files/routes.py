import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import File
from ..extensions import db, limiter
from .forms import FileUploadForm, FileDeleteForm
from ..storage import get_storage
from ..tenancy import current_org_id

files = Blueprint('files', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
@login_required
def index():
    form = FileUploadForm()
    delete_form = FileDeleteForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            org_slug = current_user.organization.slug
            storage = get_storage()
            file_path, filename = storage.save(org_slug, file)

            new_file = File(
                org_id=current_org_id(),
                uploader_id=current_user.id,
                filename=filename,
                path=file_path,
                mime=file.mimetype,
                size=os.path.getsize(file_path)
            )
            db.session.add(new_file)
            db.session.flush()
            from ..models import record_activity
            record_activity('file.upload', 'File', new_file.id)
            db.session.commit()
            flash('File successfully uploaded')
            return redirect(url_for('files.index'))
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')

    all_files = File.query.filter_by(org_id=current_org_id()).order_by(File.created_at.desc()).all()
    return render_template('files/index.html', files=all_files, form=form, delete_form=delete_form)

@files.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file_record = File.query.get_or_404(file_id)
    # Ensure the user has access to this file (org_id check)
    if file_record.org_id != current_user.org_id and current_user.role != 'jusb_admin':
        flash('You do not have permission to download this file.')
        return redirect(url_for('files.index'))

    # Extract directory and filename from the full path
    directory = os.path.dirname(file_record.path)
    filename = os.path.basename(file_record.path)

    return send_from_directory(directory, filename, as_attachment=True)


@files.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    form = FileDeleteForm()
    file_record = File.query.get_or_404(file_id)
    if file_record.org_id != current_org_id() and current_user.role != 'jusb_admin':
        abort(403)
    if form.validate_on_submit():
        # Best effort remove from disk
        try:
            if os.path.exists(file_record.path):
                os.remove(file_record.path)
        except Exception:
            pass
        from ..models import record_activity
        db.session.delete(file_record)
        db.session.flush()
        record_activity('file.delete', 'File', file_id)
        db.session.commit()
        flash('File deleted')
    else:
        flash('Invalid delete request')
    return redirect(url_for('files.index'))
