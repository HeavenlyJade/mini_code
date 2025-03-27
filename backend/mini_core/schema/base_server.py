from kit.schema.base import BaseSchema
from webargs import fields
class UploadResponseSchema(BaseSchema):
    url = fields.Str(description='文件访问URL')
    filename = fields.Str(description='原始文件名')
    mimetype = fields.Str(description='文件类型')
    size = fields.Int(description='文件大小')
