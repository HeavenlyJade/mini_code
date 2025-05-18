class ShopUserMessage:
    USER_NOT_EXIST = '用户不存在'
    USER_PASSWORD_ERROR = '用户名不存在或密码错误'
    USER_EXISTED = '用户已存在'
    PHONE_EXISTED = '手机号已被使用'
    OPENID_EXISTED = 'OpenID已被使用'
    USER_DISABLED = '用户已被禁用'


class ShopAuthMessage:
    TOKEN_EXPIRES = '登录失效，请重新登录'


class ReturnStatusMapping:
    STATUS_CODE_TO_TEXT = {
        0: '待审核',
        1: '已同意',
        2: '已拒绝',
        3: '退款中',
        4: '已完成'
    }
    STATUS_DATA_TO_TEXT ={
        0: "退款/退货申请中",
    }

    # 状态文本与状态代码的映射
    STATUS_TEXT_TO_CODE = {
        '待审核': 0,
        '已同意': 1,
        '已拒绝': 2,
        '退款中': 3,
        '已完成': 4
    }
    STATUS_TO_OPERATION = {
        0: "等待审核",
        1: '审核通过',
        2: '审核拒绝',
        3: '退款处理中',
        4: '退款完成'
    }

    DEFAULT_OPERATION = '状态变更'

    @classmethod
    def get_status_text(cls, status_code):
        """
        根据状态代码获取状态文本

        Args:
            status_code: 状态代码(0-4)

        Returns:
            对应的状态文本
        """
        return cls.STATUS_CODE_TO_TEXT.get(status_code, '未知状态')
    @classmethod
    def get_status_data_text(cls, status_code):
        return cls.STATUS_DATA_TO_TEXT.get(status_code)

    @classmethod
    def get_operation_type(cls, status):
        """
        根据状态获取对应的操作类型

        Args:
            status: 订单退款状态

        Returns:
            对应的操作类型描述
        """
        return cls.STATUS_TO_OPERATION.get(status, cls.DEFAULT_OPERATION)

    @classmethod
    def get_operation_type(cls, status):
        """
        根据状态获取对应的操作类型

        Args:
            status: 可以是状态代码或状态文本

        Returns:
            对应的操作类型描述
        """
        # 如果输入的是状态代码，先转换为状态文本
        if isinstance(status, int):
            status_text = cls.get_status_text(status)
        else:
            status_text = status

        return cls.STATUS_TO_OPERATION.get(status_text, cls.DEFAULT_OPERATION)
