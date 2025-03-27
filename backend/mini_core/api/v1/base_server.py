

from flask.views import MethodView
from flask import request, current_app
from datetime import datetime
from pathlib import Path
import uuid
from backend.business.service.auth import auth_required
from backend.mini_core.schema.base_server import UploadResponseSchema
from kit.exceptions import ServiceBadRequest
from kit.util.blueprint import APIBlueprint
from werkzeug.utils import secure_filename


blp = APIBlueprint('base_server', 'base_server', url_prefix='/')


@blp.route('/upload_image')
class FileUploadAPI(MethodView):
    """文件上传API"""

    decorators = [auth_required()]

    @blp.response(UploadResponseSchema)
    def post(self):
        """处理文件上传请求"""
        if 'file' not in request.files:
            raise ServiceBadRequest('没有文件上传')

        file = request.files['file']
        if file.filename == '':
            raise ServiceBadRequest('未选择文件')

        # 验证文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'zip', 'mp4', 'webp', 'svg'}
        if not allowed_file(file.filename, allowed_extensions):
            raise ServiceBadRequest(f'不支持的文件类型，允许的类型: {", ".join(allowed_extensions)}')

        # 保存文件
        # try:
        filename = save_file(file)
        file_url = get_file_url(filename)

        return {
            'url': file_url,
            'filename': file.filename,
            'mimetype': file.mimetype,
        }
        # except Exception as e:
        #     current_app.logger.error(f"文件上传失败: {str(e)}")
        #     raise ServiceBadRequest(f'文件上传失败: {str(e)}')


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file) -> str:
    """保存上传的文件并返回生成的文件名"""
    # 生成唯一文件名
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    timestamp = datetime.now().strftime('%Y%m%d')
    unique_filename = f"{timestamp}_{uuid.uuid4().hex}.{extension}" if extension else f"{timestamp}_{uuid.uuid4().hex}"
    # 确保上传目录存在
    Image_Path = current_app.config.get('IMAGE_PATH')
    print("date_dir",Image_Path)

    upload_dir = Path(Image_Path)
    date_dir = upload_dir / timestamp
    if not date_dir.exists():
        date_dir.mkdir(parents=True, exist_ok=True)

    # 保存文件
    file_path = date_dir / unique_filename
    file.save(file_path)

    return str(Path(timestamp) / unique_filename)


def get_file_url(filename: str) -> str:
    """根据文件名生成访问URL"""
    base_url = current_app.config.get('UPLOADS_URL_PREFIX', '/files')
    return f"{base_url}/{filename}"


def get_file_size(filename: str) -> int:
    """获取文件大小"""
    file_path = Path(current_app.config['UPLOADS_FOLDER']) / filename
    return file_path.stat().st_size
