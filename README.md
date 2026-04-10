# 健脑房 BrainGym

面向「开放式训练 + 体测」的认知能力练习 Web 应用：批判性思维、提问力、创造力等维度；支持 DeepSeek / OpenAI 兼容 API 的 AI 出题与点评。

## 评委 / 使用者如何运行

### 方式 A：本机 Python（最快）

1. Python **3.9+**（推荐 3.11）
2. 安装依赖并配置环境变量：

```bash
cd braingym
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入 LLM_API_KEY（无 key 时部分 AI 能力不可用，其余页面仍可浏览）
```

3. 启动服务：

```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. 浏览器打开：<http://127.0.0.1:8000>  
   首页输入昵称登录即可；健康检查：<http://127.0.0.1:8000/health>

### 方式 B：Docker（环境一致、适合提交物）

```bash
cp .env.example .env
# 按需编辑 .env
mkdir -p data
docker compose up --build
```

访问 <http://127.0.0.1:8000>。数据库文件在宿主机的 `./data/braingym.db`。

### 检查 LLM 是否可用

```bash
source .venv/bin/activate
python scripts/check_llm.py
```

## 公网部署（让别人打开链接就能用）

思路：**把代码放到 Git 仓库** → 在云平台用 **Docker** 构建并运行 → 绑定平台分配的 **HTTPS 域名** → 在控制台填入 **环境变量**（尤其 `LLM_API_KEY`）。本仓库的 `Dockerfile` 已监听 `0.0.0.0` 和 `PORT`，并暴露 `GET /health` 给健康检查。

### 方案一：Render（步骤最少，海外访问）

1. 把项目推到 **GitHub**（不要提交 `.env`、`braingym.db`）。
2. 打开 [Render Dashboard](https://dashboard.render.com/)，登录后 **New → Blueprint**，选中该仓库；若提示使用 `render.yaml`，按引导创建即可。
3. 在界面里为 **`LLM_API_KEY`** 填入你的 DeepSeek（或兼容 OpenAI）的 Key（Blueprint 里该项为 `sync: false`，需在 Dashboard 补全）。
4. 部署完成后，打开形如 `https://braingym.onrender.com` 的地址即可访问。

**持久化数据库（推荐正式演示用）**  
Render 的**持久盘仅支持付费 Web 实例**。本仓库的 `render.yaml` 已配置：磁盘挂到 `/app/data`，`DATABASE_URL=sqlite:////app/data/braingym.db`。若你只用**免费实例**，请删掉 `render.yaml` 里的 `disk` 段和 `DATABASE_URL` 环境变量，接受「重新部署后 SQLite 可能清空」；短期评委演示通常可接受。

**不用 Blueprint、纯手点创建**  

- **New → Web Service**，连接同一 GitHub 仓库。  
- **Runtime** 选 **Docker**（使用根目录 `Dockerfile`）。  
- **Environment**：添加 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`（与 `.env.example` 一致）。需要持久库时再加磁盘挂载 `/app/data`，并增加 `DATABASE_URL=sqlite:////app/data/braingym.db`。  
- **Health Check Path** 填 `/health`。

### 方案二：Fly.io / Railway / 其他

- **启动命令**：与 Dockerfile 默认一致即可（`uvicorn app.main:app --host 0.0.0.0 --port $PORT`）。  
- **环境变量**：同 `.env.example`。  
- **SQLite**：务必使用**持久卷**，并把 `DATABASE_URL` 指到卷内路径（例如 `sqlite:////data/braingym.db`），否则容器重建后数据会丢。

### 方案三：国内云服务器（轻量应用服务器 / ECS）

在机器上安装 Docker，复制项目后执行：

```bash
cp .env.example .env
# 编辑 .env
mkdir -p data
docker compose up -d --build
```

在安全组/防火墙放行 **8000**（或你映射的端口），用 `http://服务器公网IP:8000` 访问；若要 **HTTPS**，前面加一层 Nginx / 云平台 CLB 做证书。

---

**自检清单**

| 项 | 说明 |
|----|------|
| `PORT` | 平台一般会自动注入；本地 Docker 默认 8000 |
| `LLM_API_KEY` | 在平台「环境变量」里配置，不要写进仓库 |
| 数据库 | 正式环境务必持久卷 + `DATABASE_URL` 与挂载路径一致 |
| 健康检查 | `GET /health` 返回 `{"status":"ok"}` |

## 项目结构（方便你后续改）

| 路径 | 说明 |
|------|------|
| `app/main.py` | FastAPI 入口、静态资源、`/health` |
| `app/config.py` | 环境变量、维度/关卡/场景等配置 |
| `app/database.py` | SQLAlchemy、`init_db`、SQLite 迁移 |
| `app/models.py` | 数据模型 |
| `app/routers/` | 用户、引导、体测、训练路由 |
| `app/services/` | AI 调用、训练/体测业务逻辑 |
| `app/templates/` | Jinja2 页面 |
| `app/static/` | CSS 等静态文件 |
| `app/question_bank/` | 题库文本 |
| `scripts/check_llm.py` | 连通性自检 |

## 技术栈

FastAPI、Jinja2、SQLAlchemy、SQLite、httpx、python-dotenv。

## 许可

参赛或二次发布前请自行补充许可证文件（如 MIT），并按比赛要求标注原创与引用。
