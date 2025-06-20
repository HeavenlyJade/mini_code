from marshmallow import Schema, fields, validate

class PSDProcessRequestSchema(Schema):
    """PSD处理请求模式"""
    psd_path = fields.Str(missing="jinjiang2.psd", description="PSD文件路径")
    new_text = fields.Str(required=True, description="要替换的文本内容", validate=validate.Length(min=1, max=100))
    output_format = fields.Str(missing="png", description="输出格式", validate=validate.OneOf(["png", "jpg", "jpeg"]))
    quality = fields.Int(missing=95, description="输出质量", validate=validate.Range(min=1, max=100))

class PSDProcessResponseSchema(Schema):
    """PSD处理响应模式"""
    code = fields.Int(required=True, description="响应状态码")
    message = fields.Str(required=True, description="响应消息")
    data = fields.Dict(description="响应数据")
