


if __name__ == '__main__':
    from backend.app import create_app
    app = create_app()
    app.app_context().push()
    from backend.mini_core.service.shop_app.wx_server_new import init_wechat_pay

    wxpay = init_wechat_pay()

