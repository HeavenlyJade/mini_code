# 起源小程序后端系统

![License](https://img.shields.io/badge/license-IKAS-blue.svg)
![Python](https://img.shields.io/badge/python-3.9-green.svg)
![Flask](https://img.shields.io/badge/flask-2.1.2-red.svg)

## 项目简介

起源小程序后端系统是一个基于Flask框架的综合性电商小程序后端服务，主要面向微信小程序提供完整的电商业务支持。系统采用现代化的微服务架构设计，支持商品管理、订单处理、用户管理、分销系统、支付集成等核心功能。

### 主要特性

- 🛒 **完整电商功能** - 商品管理、购物车、订单处理、库存管理
- 📱 **微信小程序集成** - 微信登录、微信支付、小程序授权
- 💰 **分销系统** - 多级分销、佣金结算、等级管理
- 🏪 **多门店支持** - 门店管理、配送设置、营业时间配置
- 📊 **数据分析** - 仪表盘统计、销售分析、用户行为分析
- 🔐 **权限管理** - 基于RBAC的角色权限控制
- 📦 **物流管理** - 订单跟踪、物流信息、配送状态
- 🎫 **会员系统** - 等级管理、积分体系、优惠券

## 技术栈

### 后端框架
- **Flask** - 轻量级Web框架
- **Flask-SQLAlchemy** - ORM数据库操作
- **Flask-Migrate** - 数据库迁移工具
- **Flask-JWT-Extended** - JWT身份认证
- **Flask-Smorest** - RESTful API文档生成

### 数据库
- **MySQL** - 主数据库
- **Redis** - 缓存和会话存储
- **Oracle** - 企业数据库支持（可选）

### 异步任务
- **Celery** - 分布式任务队列
- **RabbitMQ** - 消息队列中间件

### 第三方集成
- **微信支付** - 支付接口集成
- **顺丰速运** - 物流API集成
- **Apache SkyWalking** - 应用性能监控

### 部署工具
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Gunicorn** - WSGI HTTP服务器

## 项目结构

```
mini_code/
├── backend/                    # 主要业务模块
│   ├── alarm/                 # 报警服务
│   ├── business/              # 业务服务
│   ├── license_management/    # 许可证管理
│   ├── log/                   # 日志服务
│   ├── mini_core/             # 小程序核心功能
│   │   ├── api/              # API接口层
│   │   ├── domain/           # 领域模型
│   │   ├── repository/       # 数据访问层
│   │   ├── service/          # 业务逻辑层
│   │   └── schema/           # 数据验证模式
│   ├── role/                  # 角色权限管理
│   └── user/                  # 用户管理
├── kit/                       # 工具库
│   ├── domain/               # 领域基础组件
│   ├── repository/           # 仓储模式基类
│   ├── service/              # 服务基类
│   ├── util/                 # 工具函数
│   └── wechatpayv3/          # 微信支付v3 SDK
├── task/                      # 异步任务
├── conf/                      # 配置文件
├── migrations/                # 数据库迁移文件
├── tests/                     # 测试文件
└── requirements/              # 依赖管理
```

## 核心功能模块

### 1. 用户管理系统
- 微信小程序用户授权登录
- 用户信息管理和更新
- 收货地址管理
- 会员等级体系

### 2. 商品管理系统
- 商品信息管理（CRUD）
- 商品分类管理
- 规格属性管理
- 库存管理和预警
- 商品图片和视频管理

### 3. 订单管理系统
- 订单创建和状态管理
- 订单详情和日志记录
- 订单退货退款处理
- 订单配置和设置

### 4. 支付系统
- 微信支付集成（JSAPI、小程序支付）
- 支付回调处理
- 支付状态同步
- 退款处理

### 5. 分销系统
- 多级分销管理
- 分销商等级配置
- 佣金计算和结算
- 提现申请处理

### 6. 门店管理
- 门店信息管理
- 营业时间配置
- 配送范围设置
- 门店服务模式（外卖/自取/堂食）

### 7. 物流管理
- 订单发货管理
- 物流信息跟踪
- 配送状态更新
- 物流公司对接

### 8. 权限管理
- 基于RBAC的权限控制
- 角色和权限管理
- 菜单权限配置
- API接口权限验证

## 安装部署

### 环境要求

- Python 3.9+
- MySQL 5.8+
- Redis 5.0+
- Docker & Docker Compose（推荐）

### 开发环境安装

#### 1. 使用Poetry（推荐）

```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

#### 2. 使用pip

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置文件

复制环境配置文件并修改相关配置：

```bash
.env
```

配置数据库连接、Redis连接、微信小程序配置等：

```env
# 数据库配置
DEV_DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 微信小程序配置
WECHAT_MULTIPLATFORM_APPID=your_wechat_appid
WECHAT_MULTIPLATFORM_SECRET=your_wechat_secret

# JWT配置
JWT_SECRET_KEY=your_jwt_secret_key
```

### 数据库初始化

```bash
# 初始化数据库迁移
flask db init

# 生成迁移文件
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

### 运行应用

#### 开发环境

```bash
# 直接运行
python run.py

# 或使用Flask命令
flask run --host=127.0.0.1 --port=5555 --debug
```

#### 生产环境

```bash
# 使用Gunicorn
gunicorn autoapp:app \
    --bind 0.0.0.0:5000 \
    -w 8 \
    -k eventlet \
    --access-logfile - \
    --error-logfile -
```

### Docker部署

#### 构建镜像

```bash
# 开发环境
docker build -f Dockerfile.dev -t mini_app_bac:dev .

# 生产环境
docker build -f Dockerfile -t mini_app_bac:latest .
```

#### 使用Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web
```

### Celery异步任务

启动Celery Worker：

```bash
# 开发环境
celery -A celery_worker.celery worker -l info

# 生产环境（使用eventlet）
celery -A celery_worker.celery worker -l info -P eventlet
```

启动Flower监控（可选）：

```bash
celery -A celery_worker.celery flower
```

## API文档

应用启动后，可以通过以下地址访问API文档：

- **Swagger UI**: http://localhost:5000/swagger-ui
- **ReDoc**: http://localhost:5000/redoc
- **RapiDoc**: http://localhost:5000/rapidoc

## 配置说明

### 微信小程序配置

1. 在微信公众平台配置小程序信息
2. 获取AppID和AppSecret
3. 配置服务器域名和业务域名
4. 设置支付商户号和API密钥

### 支付配置

1. 申请微信支付商户号
2. 下载API证书文件到 `wxcert/` 目录
3. 配置支付回调URL
4. 设置支付密钥

### 物流配置

1. 申请顺丰速运API权限
2. 配置物流公司信息
3. 设置物流回调接口

## 开发指南

### 代码规范

项目使用以下代码规范工具：

- **Black** - 代码格式化
- **isort** - 导入排序
- **MyPy** - 类型检查

运行代码检查：

```bash
# 格式化代码
black .

# 排序导入
isort .

# 类型检查
mypy .
```

### 测试

运行测试用例：

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=backend --cov-report=html
```

### 数据库迁移

```bash
# 生成迁移文件
flask db migrate -m "描述信息"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

## 监控与日志

### 日志配置

系统使用Loguru进行日志管理，日志文件位于 `logs/` 目录：

- 应用日志：`logs/app.log`
- 微信支付日志：`wechatpay.log`
- 错误日志：`logs/error.log`

### 性能监控

集成Apache SkyWalking进行应用性能监控：

1. 配置SkyWalking Agent
2. 设置监控指标
3. 查看性能报告

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库配置
   - 确认数据库服务是否启动

2. **微信支付失败**
   - 检查证书文件路径
   - 验证商户号配置
   - 确认回调URL设置

3. **Celery任务失败**
   - 检查Redis连接
   - 查看Celery Worker日志
   - 确认任务队列配置

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看Docker容器日志
docker-compose logs -f web

# 查看Celery日志
docker-compose logs -f celery_worker
```

## 贡献指南

1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request



## 更新日志

### v1.0.0 (当前版本)
- 初始版本发布
- 基础电商功能实现
- 微信小程序集成
- 分销系统上线
- Docker部署支持

---

**注意**: 本项目正在积极开发中，功能和API可能会发生变化。生产环境使用前请进行充分测试。

