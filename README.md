# SoftMatterGPT

面向软物质课程与实验教学的 AI 教学工作台。

**在线体验**：https://softmatter.streamlit.app/ （无需安装，直接使用）

## 项目简介

SoftMatterGPT 是一个面向软物质科学课程的智能教学辅助系统。系统基于公开大语言模型（Ollama），结合检索增强生成（RAG）技术，为师生提供课程知识问答、文献检索、实验配方查询、实验方案生成、表征结果辅助分析、材料体系对比以及教学数据分析等功能。

系统提供两套前端界面：
- **杂志风格前端**（推荐）：基于 Next.js + Tailwind CSS 构建的现代化杂志风格界面，具有精致的排版、视觉冲击力和优秀的阅读体验
- **经典前端**：基于 Streamlit 构建的传统多页面应用

后端采用 FastAPI 提供统一 API 服务，支持离线环境下优雅降级，在 Ollama 服务不可用时仍可使用知识检索和规则分析功能。

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| 前端（杂志风格） | Next.js 15 + React 19 + Tailwind CSS 4 |
| 前端（经典） | Streamlit 多页面应用 |
| 后端 | FastAPI RESTful API |
| 数据校验 | Pydantic v2 |
| 大语言模型 | Ollama（支持 Qwen、DeepSeek、Gemma、Llama 等开源模型） |
| 数据处理 | Pandas、NumPy |
| 文本检索 | scikit-learn（TF-IDF 向量化） |
| 可视化 | Plotly、Matplotlib |
| 运行环境 | Python >= 3.9 |

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/songhong/softmatter-app.git
cd softmatter-app
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 Ollama（可选）

如需使用大语言模型功能，请安装 Ollama 并拉取模型：

```bash
# 安装 Ollama（参考 https://ollama.com）
curl -fsSL https://ollama.com/install.sh | sh

# 拉取推荐模型
ollama pull qwen3.5:9b
```

未安装 Ollama 时，系统仍可正常运行，但涉及 LLM 生成的功能（智能问答、实验方案、材料对比）将返回提示信息。

### 4. 配置环境变量（可选）

**大多数情况下不需要手动配置**，所有参数都有默认值，直接启动即可。

只有在以下场景才需要修改：

| 场景 | 需要修改的变量 |
|------|--------------|
| Ollama 部署在其他机器或端口 | `OLLAMA_BASE_URL` |
| 想使用其他模型（如 deepseek:7b） | `DEFAULT_MODEL` |
| 需要固定的 API 密钥（多人共用） | `SOFTMATTER_API_KEY` |

**配置方法**：在项目根目录创建 `.env` 文件：

```bash
# 复制示例文件（如果存在）
cp .env.example .env

# 或手动创建
cat > .env << 'EOF'
# Ollama 服务地址（默认 http://localhost:11434）
OLLAMA_BASE_URL=http://localhost:11434

# 默认模型（默认 qwen3.5:9b）
DEFAULT_MODEL=qwen3.5:9b

# API 认证密钥（不设置会自动生成，但每次启动不同）
SOFTMATTER_API_KEY=your-secret-key-here
EOF
```

**所有可配置参数一览**：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 服务地址 |
| `DEFAULT_MODEL` | `qwen3.5:9b` | 默认模型名称 |
| `TOP_K` | `5` | RAG 检索返回条数 |
| `SIMILARITY_THRESHOLD` | `0.3` | 检索相似度阈值 |
| `API_HOST` | `127.0.0.1` | 后端监听地址 |
| `API_PORT` | `8000` | 后端监听端口 |
| `SOFTMATTER_API_KEY` | 自动生成 | API 认证密钥 |

> **注意**：`.env` 文件包含敏感信息，已在 `.gitignore` 中排除，不会被提交到 Git 仓库。

## 启动方法

> **注意**：需要同时运行后端和前端两个服务，请打开两个终端窗口。

### 终端 1：启动后端服务

```bash
cd softmatter-app
python api_server.py
```

后端默认运行在 `http://127.0.0.1:8000`，提供 13 个业务 API 端点（15 个独立路径）。

### 终端 2：启动前端页面

```bash
cd softmatter-app
streamlit run app.py
```

前端默认运行在 `http://localhost:8501`，在浏览器中打开即可使用。

### 快速验证

启动后，访问 `http://localhost:8501`，如果看到 SoftMatterGPT 界面，说明安装成功。

---

## 部署方式与局域网访问

### 方式一：本地部署（自己用）

最简单的方式，只在自己电脑上运行：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动后端（终端 1）
python api_server.py

# 3. 启动前端（终端 2）
streamlit run app.py

# 4. 浏览器打开 http://localhost:8501
```

Ollama 地址保持默认 `http://localhost:11434`。如果 Ollama 装在 Windows 而 Streamlit 在 WSL2 中运行，参考下方「常见问题 - 问题 2」的解决方法。

---

### 方式二：局域网访问（让同网络的其他人也能用）

如果你希望实验室或教室里其他人也能通过浏览器访问你的 SoftMatterGPT，需要做以下配置：

#### 第一步：确认你的局域网 IP

```bash
# Linux / WSL2：
hostname -I
# 或
ip addr show | grep "inet " | grep -v 127.0.0.1

# Windows（PowerShell）：
ipconfig | findstr "IPv4"
```

记下你的 IP 地址，例如 `192.168.1.100`。

#### 第二步：确保 Ollama 允许外部访问

Ollama 默认只监听 `127.0.0.1`（本机），其他电脑无法连接。需要让 Ollama 监听所有地址：

**Windows 用户**：
1. 搜索「环境变量」，打开「编辑系统环境变量」
2. 点击「环境变量」→「系统变量」→「新建」
3. 变量名：`OLLAMA_HOST`，变量值：`0.0.0.0`
4. 确定保存，重启 Ollama（任务管理器结束 ollama.exe 后重新打开）

**Linux / WSL2 用户**：
```bash
# 启动 Ollama 时指定监听地址
OLLAMA_HOST=0.0.0.0 ollama serve &

# 或设置环境变量后启动
export OLLAMA_HOST=0.0.0.0
ollama serve &
```

**macOS 用户**：
```bash
OLLAMA_HOST=0.0.0.0 ollama serve &
```

#### 第三步：确认 Streamlit 配置允许外部访问

项目已内置 `.streamlit/config.toml`，默认配置为：

```toml
[server]
address = "0.0.0.0"    # 允许外部访问
port = 8501
```

如果你修改过这个文件，确保 `address = "0.0.0.0"`（不是 `localhost` 或 `127.0.0.1`）。

#### 第四步：修改 Ollama 地址配置

在系统设置页面，将 Ollama 地址改为你的局域网 IP：

```
http://192.168.1.100:11434    # 替换为你的实际 IP
```

或者在 `.env` 文件中设置：

```bash
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

#### 第五步：防火墙放行

**Windows 防火墙**：
1. 搜索「Windows Defender 防火墙」→「高级设置」
2. 左侧点击「入站规则」→ 右侧点击「新建规则」
3. 选择「端口」→ TCP → 特定端口：`8501,8000,11434`
4. 选择「允许连接」→ 完成

**Linux 防火墙**（如果启用了 ufw）：
```bash
sudo ufw allow 8501/tcp   # Streamlit 前端
sudo ufw allow 8000/tcp   # FastAPI 后端
sudo ufw allow 11434/tcp  # Ollama
```

#### 第六步：其他电脑访问

在同一局域网的其他电脑浏览器中输入：

```
http://192.168.1.100:8501    # 替换为你的实际 IP
```

#### 局域网访问常见问题

**Q：其他电脑打不开页面？**

```bash
# 在其他电脑上测试连通性
ping 192.168.1.100           # 替换为你的 IP
curl http://192.168.1.100:8501  # 测试 Streamlit
curl http://192.168.1.100:11434/api/tags  # 测试 Ollama
```

如果 ping 不通，检查两台电脑是否在同一子网（IP 前三段相同）。如果 ping 通但端口不通，检查防火墙设置。

**Q：能打开页面但显示「无法连接 Ollama」？**

确保 Ollama 已设置 `OLLAMA_HOST=0.0.0.0` 并重启。然后在系统设置页面确认 Ollama 地址是局域网 IP 而不是 `localhost`。

**Q：学校/公司网络有 VLAN 隔离？**

部分校园网或企业网会隔离不同 VLAN 的设备，即使在同一局域网也无法互访。这种情况需要联系网管，或者使用方式三（线上部署）。

---

### 方式三：线上部署（任何人都能访问）

#### 3.1 Streamlit Cloud（推荐，免费）

已部署的在线版本：**https://softmatter.streamlit.app/**

直接在浏览器中打开即可使用，无需安装任何软件。

**自己部署步骤**：

1. **登录 Streamlit Cloud**
   - 打开 https://share.streamlit.io
   - 用 GitHub 账号登录
   - 国内用户可能需要 VPN 才能访问（见下方「国内用户特别说明」）

2. **选择仓库部署**
   - 点击「New app」
   - Repository：选择你的仓库（如 `songhong/softmatter-app`）
   - Branch：`main`
   - Main file path：`app.py`
   - 点击「Deploy!」

3. **配置环境变量（可选）**
   - 部署后点击右上角「⋮」→「Settings」
   - 在「Secrets」中添加环境变量：
     ```toml
     OLLAMA_BASE_URL = "http://your-ollama-server:11434"
     DEFAULT_MODEL = "qwen3.5:9b"
     ```

4. **访问地址**
   - 部署成功后会生成类似 `https://your-app-name.streamlit.app` 的链接
   - 分享这个链接给任何人即可使用

**Streamlit Cloud 限制**：
- Ollama 无法连接（云端服务器无法访问你本地的 Ollama）
- LLM 生成功能不可用，但知识检索、文献搜索、配方查询等基于规则的功能正常
- 免费版有资源限制，高并发时可能变慢
- 国内访问可能较慢或需要 VPN

---

#### 3.2 Hugging Face Spaces（免费，国内可访问）

Hugging Face Spaces 支持部署 Streamlit 应用，且国内可以直接访问：

1. 注册 Hugging Face 账号：https://huggingface.co/join
2. 创建新的 Space：https://huggingface.co/new-space
3. 选择 SDK 为 **Streamlit**
4. 上传项目文件（或连接 GitHub 仓库）
5. 部署后获得类似 `https://<用户名>-<空间名>.hf.space` 的链接

**优点**：国内可直接访问，无需 VPN
**缺点**：免费版有资源限制，冷启动较慢

---

#### 3.3 Render（免费版可用）

Render 支持部署 Web 服务，免费版足够个人使用：

1. 注册 Render 账号：https://render.com
2. 创建 Web Service
3. 连接 GitHub 仓库
4. 配置：
   - Build Command：`pip install -r requirements.txt`
   - Start Command：`streamlit run app.py --server.port $PORT`
5. 部署后获得类似 `https://<服务名>.onrender.com` 的链接

**优点**：自动部署，支持自定义域名
**缺点**：免费版 15 分钟无访问会休眠，首次访问需要等待唤醒

---

#### 3.4 Railway（有免费额度）

Railway 提供免费额度，部署简单：

1. 注册 Railway 账号：https://railway.app
2. 从 GitHub 仓库部署
3. 自动检测 Streamlit 应用并配置
4. 部署后获得类似 `https://<项目名>.up.railway.app` 的链接

**优点**：部署简单，支持自定义域名
**缺点**：免费额度有限，超出后收费

---

#### 3.5 Vercel / Netlify

这两个平台主要用于静态网站，但也可以通过 Serverless Functions 部署 Streamlit 应用（需要额外配置）。不推荐新手使用，建议优先选择上面的方式。

---

#### 线上部署平台对比

| 平台 | 免费 | 国内可访问 | 部署难度 | 冷启动 | 推荐场景 |
|------|------|-----------|---------|--------|---------|
| Streamlit Cloud | 是 | 需VPN | 简单 | 无 | 教学演示、快速分享 |
| Hugging Face Spaces | 是 | 是 | 简单 | 较慢 | 国内用户、学术分享 |
| Render | 是 | 是 | 中等 | 15分钟休眠 | 个人项目 |
| Railway | 有额度 | 是 | 简单 | 无 | 长期运行 |
| 自建服务器 | 看服务器 | 看服务器 | 较复杂 | 无 | 生产环境、完全控制 |

---

### 方式四：自建服务器部署（推荐用于长期使用）

如果你有一台 Linux 服务器（云服务器或实验室服务器），可以部署为长期服务：

```bash
# 1. SSH 登录服务器
ssh user@your-server-ip

# 2. 安装 Python 和依赖
sudo apt update && sudo apt install -y python3 python3-pip git
pip3 install -r requirements.txt

# 3. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3.5:9b

# 4. 克隆代码
git clone https://github.com/songhong/softmatter-app.git
cd softmatter-app

# 5. 配置 Ollama 监听外部访问
export OLLAMA_HOST=0.0.0.0
ollama serve &

# 6. 启动后端
nohup python3 api_server.py &

# 7. 启动前端
nohup streamlit run app.py --server.headless true &

# 8. 访问
# 浏览器打开 http://your-server-ip:8501
```

**使用 systemd 管理服务（推荐）**：

创建 `/etc/systemd/system/softmatter.service`：

```ini
[Unit]
Description=SoftMatterGPT Streamlit App
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/softmatter-app
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.headless true
Restart=always
RestartSec=5
Environment=OLLAMA_HOST=0.0.0.0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable softmatter
sudo systemctl start softmatter
sudo systemctl status softmatter
```

**使用 Nginx 反向代理（可选，支持域名和 HTTPS）**：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 国内用户特别说明

### 1. pip 安装加速

国内访问 PyPI 较慢，使用清华镜像源：

```bash
# 临时使用
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久设置（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

其他可用镜像源：

| 镜像源 | 地址 |
|--------|------|
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple |
| 豆瓣 | https://pypi.douban.com/simple |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple |

### 2. Ollama 下载

Ollama 官网（ollama.com）在部分地区可能访问较慢：

- **Windows / macOS**：从 https://ollama.com 下载安装包，如果下载慢可以找国内镜像或使用代理
- **Linux**：`curl -fsSL https://ollama.com/install.sh | sh`，如果超时可以多试几次或使用代理
- **拉取模型**：`ollama pull qwen3.5:9b`，模型下载可能较慢，建议使用代理或耐心等待

### 3. GitHub 访问

`git clone` 可能很慢或失败：

```bash
# 方法一：使用代理
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

# 方法二：直接在 GitHub 页面下载 ZIP
# 打开 https://github.com/songhong/softmatter-app
# 点击绿色「Code」按钮 → 「Download ZIP」

# 方法三：使用 GitHub 镜像站加速
```

### 4. Streamlit Cloud 访问

- `share.streamlit.io` 和 `*.streamlit.app` 在国内可能无法直接访问
- 解决方案：使用 VPN，或部署在国内云服务器上（见「方式四」）

### 5. 代理软件配置

如果你使用 Clash、V2Ray 等代理软件，建议将以下地址加入**直连规则**（不走代理）：

```
localhost, 127.0.0.1, 192.168.*, 10.*
```

否则本地服务之间的通信可能被代理拦截导致失败。

---

## 常见问题与故障排查

> 如果你是第一次使用，建议通读本节。大部分问题都在这里能找到答案。

### 问题 1：浏览器打不开 `http://localhost:8501`

**原因**：Streamlit 默认监听 IPv6，在部分系统上浏览器无法访问。

**解决方法**：项目已内置 `.streamlit/config.toml` 配置文件，默认监听 `0.0.0.0:8501`。如果仍然打不开：

```bash
# 1. 确认 Streamlit 是否在运行
ps aux | grep streamlit

# 2. 确认端口是否被占用
# Linux / WSL2：
ss -tlnp | grep 8501
# Windows（PowerShell）：
netstat -ano | findstr :8501

# 3. 如果端口被占用，杀掉旧进程
# Linux / WSL2：
kill -9 $(pgrep -f "streamlit run")
# Windows（PowerShell）：
taskkill /PID <进程ID> /F
```

---

### 问题 2：「无法连接 Ollama 服务，请确认 Ollama 已启动」

这是最常见的问题。**根本原因是 Streamlit 和 Ollama 不在同一个网络里**。

#### 情况 A：Ollama 装在 Windows，Streamlit 在 WSL2 中运行

这是最常见的情况。WSL2 有自己独立的网络，`localhost` 在 WSL2 里指的是 WSL2 自己，不是 Windows。

**解决方法**：在系统设置页面，将 Ollama 地址改为 Windows 宿主机 IP：

```bash
# 第一步：在 WSL2 终端中获取 Windows 宿主机 IP
cat /etc/resolv.conf | grep nameserver
# 输出类似：nameserver 10.255.255.254
# 这个 10.255.255.254 就是 Windows 的 IP

# 第二步：确认 Ollama 可从 WSL2 访问
curl http://10.255.255.254:11434/api/tags
# 如果返回 JSON 数据，说明可以连通
```

然后在浏览器中打开系统设置页面，将 Ollama 地址从 `http://localhost:11434` 改为 `http://10.255.255.254:11434`（以你实际获取到的 IP 为准），点击「保存地址」。

**重要**：Ollama 默认只允许本机访问。如果 WSL2 无法连通 Windows 的 Ollama，需要在 Windows 上设置环境变量让 Ollama 监听所有地址：

1. 打开 Windows「系统环境变量」（搜索"环境变量"）
2. 新建系统变量：`OLLAMA_HOST` = `0.0.0.0`
3. 重启 Ollama 服务（在任务管理器中结束 ollama.exe 后重新启动）

#### 情况 B：Ollama 装在 WSL2，Streamlit 在 Windows 中运行

这种情况较少见。Windows 访问 WSL2 的服务需要知道 WSL2 的 IP：

```bash
# 在 WSL2 终端中查看自己的 IP
hostname -I
# 输出类似：172.21.123.45

# 确认 Ollama 在 WSL2 中正常运行
curl http://localhost:11434/api/tags
```

然后在 Windows 浏览器的系统设置页面中，将 Ollama 地址改为 `http://172.21.123.45:11434`。

#### 情况 C：Ollama 和 Streamlit 都在 Windows 上

直接在命令提示符或 PowerShell 中运行：

```cmd
cd softmatter-gpt
pip install -r requirements.txt
streamlit run app.py
```

Ollama 地址保持默认的 `http://localhost:11434` 即可。

#### 情况 D：Ollama 和 Streamlit 都在 WSL2 / Linux 上

直接运行即可，地址保持默认 `http://localhost:11434`。

```bash
# 确认 Ollama 已启动
ollama list
# 如果没有输出，先启动 Ollama
ollama serve &
```

---

### 问题 3：「模型 XXX 未找到」

**原因**：`settings.json` 中记录的模型名与你实际安装的模型名不一致。

**解决方法**：

```bash
# 第一步：查看你实际安装了哪些模型
ollama list

# 第二步：在系统设置页面，点击「刷新本地模型列表」
# 第三步：从列表中选择一个已安装的模型，点击「设为当前模型」
```

或者直接编辑 `data/settings.json`，将 `current_model` 改为你实际安装的模型名。

---

### 问题 4：代理（VPN / Clash / V2Ray）导致连接失败

如果你使用了代理软件，`localhost` 请求可能被代理拦截。

**解决方法**：在终端中临时关闭代理：

```bash
# 方法一：临时取消代理环境变量
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

# 方法二：将 localhost 加入代理白名单
export no_proxy="localhost,127.0.0.1"

# 然后再启动 Streamlit
streamlit run app.py
```

如果是 Windows，可以在「系统环境变量」中删除或修改 `HTTP_PROXY` 和 `HTTPS_PROXY`。

---

### 问题 5：端口冲突（8501 或 8000 被占用）

```bash
# 查看哪个进程占用了端口
# Linux / WSL2：
lsof -i :8501
lsof -i :8000

# Windows（PowerShell）：
netstat -ano | findstr :8501
netstat -ano | findstr :8000

# 杀掉占用进程后重新启动
```

或者修改端口：

```bash
# 修改 Streamlit 端口
# 编辑 .streamlit/config.toml，将 port = 8501 改为其他值
streamlit run app.py --server.port 8502

# 修改后端端口：设置环境变量
export API_PORT=8001
```

---

### 问题 6：`pip install` 安装依赖失败

```bash
# 使用国内镜像源加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果仍然失败，尝试逐个安装
pip install streamlit fastapi uvicorn pandas numpy scikit-learn plotly requests pydantic -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 问题 7：Python 版本不兼容

本项目需要 Python >= 3.9。检查你的版本：

```bash
python --version
# 如果低于 3.9，需要升级 Python

# 推荐使用 conda 管理环境
conda create -n softmatter python=3.11
conda activate softmatter
pip install -r requirements.txt
```

---

### 问题 8：后端 API 连接失败（前端显示网络错误）

前端页面需要后端 API 服务才能正常工作。

```bash
# 1. 确认后端是否在运行
curl http://127.0.0.1:8000/api/system/status

# 2. 如果没有运行，启动后端
python api_server.py

# 3. 如果后端启动失败，检查端口是否被占用
lsof -i :8000
```

---

### 快速诊断脚本

如果遇到问题，运行以下命令快速定位：

```bash
# 在项目根目录运行
python -c "
import sys
print(f'Python: {sys.version}')

# 检查依赖
try:
    import streamlit; print(f'Streamlit: {streamlit.__version__}')
except: print('Streamlit: 未安装')

try:
    import fastapi; print(f'FastAPI: {fastapi.__version__}')
except: print('FastAPI: 未安装')

# 检查 Ollama 连接
import requests
try:
    r = requests.get('http://localhost:11434/api/tags', timeout=3)
    models = [m['name'] for m in r.json().get('models', [])]
    print(f'Ollama: 在线 ({len(models)} 个模型: {models})')
except:
    print('Ollama: 无法连接 localhost:11434')
    try:
        import subprocess
        ip = subprocess.check_output(['cat', '/etc/resolv.conf']).decode()
        for line in ip.split('\n'):
            if 'nameserver' in line:
                wsl_ip = line.split()[-1]
                r = requests.get(f'http://{wsl_ip}:11434/api/tags', timeout=3)
                models = [m['name'] for m in r.json().get('models', [])]
                print(f'Ollama: 通过 Windows IP {wsl_ip} 可达 ({len(models)} 个模型)')
                break
    except:
        print('Ollama: Windows IP 也无法连接，请检查 Ollama 是否启动')
"
```

---

### 问题 9：Ollama 模型下载失败或中断

```bash
# 重新下载模型（支持断点续传）
ollama pull qwen3.5:9b

# 查看下载进度
ollama list

# 如果一直失败，可以手动下载模型文件
# 1. 访问 https://ollama.com/library/qwen3.5
# 2. 找到对应版本的 GGUF 文件
# 3. 用浏览器或下载工具下载
# 4. 放到 Ollama 的模型目录中
```

**Ollama 模型目录位置**：
- Windows：`C:\Users\<用户名>\.ollama\models`
- Linux / WSL2：`~/.ollama/models`
- macOS：`~/.ollama/models`

---

### 问题 10：内存不足（RAM）

Ollama 模型需要较多内存。不同模型的内存需求：

| 模型大小 | 最低内存 | 推荐内存 |
|----------|---------|---------|
| 7B（如 qwen3.5:9b） | 8 GB | 16 GB |
| 13B | 16 GB | 32 GB |
| 70B | 64 GB | 128 GB |

如果内存不足，Ollama 会变慢或崩溃。解决方法：

```bash
# 使用更小的量化模型
ollama pull qwen3.5:9b-q4_K_M    # 4-bit 量化，内存占用更小

# 或使用更小的模型
ollama pull qwen3:1.8b            # 1.8B 参数，适合低内存
```

**WSL2 用户注意**：WSL2 默认会占用最多 50% 的系统内存。如果内存紧张，可以限制 WSL2 内存使用：

创建或编辑 Windows 用户目录下的 `.wslconfig` 文件（`C:\Users\<用户名>\.wslconfig`）：

```ini
[wsl2]
memory=8GB
swap=4GB
```

保存后在 PowerShell 中运行 `wsl --shutdown` 重启 WSL2。

---

### 问题 11：磁盘空间不足

Ollama 模型文件较大，确保有足够的磁盘空间：

| 模型 | 大约大小 |
|------|---------|
| qwen3.5:9b | ~6 GB |
| llama3.1:8b | ~5 GB |
| deepseek-coder:6.7b | ~4 GB |

```bash
# 查看磁盘空间
df -h                    # Linux / WSL2
# Windows：打开「此电脑」查看磁盘

# 删除不需要的模型释放空间
ollama rm <模型名>
```

---

### 问题 12：Ollama 首次响应很慢

第一次使用某个模型时，Ollama 需要将模型加载到内存中，可能需要 30 秒到几分钟。后续请求会快很多（几秒内）。

如果每次都慢，可能是内存不足导致模型被反复卸载。参考「问题 10」增加内存或使用更小的模型。

---

### 问题 13：GPU 加速（NVIDIA / AMD）

如果有独立显卡，可以让 Ollama 使用 GPU 加速，大幅提升响应速度：

**NVIDIA 显卡**：
1. 安装 NVIDIA 驱动和 CUDA
2. Ollama 会自动检测并使用 GPU
3. 验证：`ollama ps` 查看是否显示 GPU 信息

**AMD 显卡**（Linux）：
1. 安装 ROCm 驱动
2. Ollama 支持 ROCm，会自动检测

**macOS（Apple Silicon）**：
- Ollama 原生支持 Metal GPU 加速，无需额外配置

---

### 问题 14：浏览器兼容性

推荐使用以下浏览器访问：
- Google Chrome（推荐）
- Microsoft Edge
- Firefox
- Safari

**不推荐**：IE 浏览器（不支持）

如果页面显示异常，尝试：
1. 清除浏览器缓存（Ctrl+Shift+Delete）
2. 使用无痕/隐私模式打开
3. 禁用浏览器扩展（某些广告拦截器可能影响页面加载）

---

### 问题 15：Windows Defender / 杀毒软件拦截

部分杀毒软件可能误报 Python 或 Ollama 为威胁：

1. 打开 Windows Defender（或其他杀毒软件）
2. 将以下目录加入白名单/排除列表：
   - 项目目录（如 `C:\Users\zhuyu\Desktop\softmatter-gpt`）
   - Python 安装目录
   - Ollama 目录（`C:\Users\<用户名>\AppData\Local\Programs\Ollama`）
   - `.venv` 虚拟环境目录

---

### 问题 16：公司 / 学校网络限制

部分企业或校园网络会：
- 封锁非标准端口（如 8501、8000、11434）
- 使用 HTTPS 代理拦截 SSL 连接
- 隔离不同 VLAN

**解决方法**：

```bash
# 方法一：使用标准端口（80/443）
streamlit run app.py --server.port 80

# 方法二：通过 SSH 隧道访问（如果你有跳板机）
ssh -L 8501:localhost:8501 user@your-server

# 方法三：联系网管开放端口
```

如果公司网络有 SSL 代理，pip 可能报证书错误：

```bash
# 临时跳过证书验证（不推荐用于生产环境）
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

### 问题 17：macOS 特别说明

**Apple Silicon（M1/M2/M3）**：
- Ollama 原生支持，性能优秀
- Python 需要 ARM64 版本（推荐使用 Homebrew 或 Miniforge）

**Intel Mac**：
- 完全兼容，无需特殊配置

```bash
# 安装 Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.11

# 安装 Ollama
brew install ollama
```

---

### 问题 18：更新项目到最新版本

```bash
# 进入项目目录
cd softmatter-app

# 拉取最新代码
git pull origin main

# 更新依赖（如果有新增）
pip install -r requirements.txt

# 重启服务
# 先杀掉旧进程，再重新启动
```

**注意**：`git pull` 会覆盖你对代码的修改。如果你修改过代码，先备份：

```bash
# 查看你修改了哪些文件
git status

# 备份修改
cp -r data/ data_backup/
git stash    # 暂存修改
git pull     # 拉取更新
git stash pop  # 恢复修改（可能需要手动合并冲突）
```

---

### 问题 19：备份与恢复

**需要备份的文件**：

| 文件 | 说明 |
|------|------|
| `data/settings.json` | 你的设置（模型选择、Ollama 地址等） |
| `data/*.csv` | 知识库、文献、配方数据 |
| `logs/` | 问答历史记录 |
| `.env` | 环境变量配置 |

```bash
# 备份
tar -czf softmatter-backup.tar.gz data/ logs/ .env

# 恢复
tar -xzf softmatter-backup.tar.gz
```

---

### 问题 20：查看日志排查问题

如果遇到不明错误，查看日志：

```bash
# Streamlit 日志
# 如果用 nohup 启动的：
cat /tmp/streamlit-server.log

# 如果用 systemd 启动的：
sudo journalctl -u softmatter -f

# Ollama 日志
# Linux：
journalctl -u ollama -f
# Windows：查看 Ollama 安装目录下的日志文件

# Python 错误日志
# 直接在终端启动 Streamlit（不用 nohup），错误会直接显示在终端
streamlit run app.py
```

---

### 问题 21：数据文件损坏或丢失

如果页面显示「数据加载失败」或空白：

```bash
# 检查数据文件是否存在
ls -la data/

# 应该看到这些文件：
# softmatter_knowledge.csv    (课程知识库)
# literature_records.csv      (文献记录)
# experiment_recipes.csv      (实验配方)
# sample_questions.csv        (测试问题)
# feedback.csv                (反馈记录)
# settings.json               (设置文件)

# 如果文件丢失，从 Git 恢复
git checkout -- data/
```

---

### 问题 22：多人同时使用

Streamlit 默认支持多人同时访问，但有以下注意事项：

- **Ollama 并发**：Ollama 默认只支持有限的并发请求。多人同时提问时，后面的请求会排队等待
- **设置冲突**：多人共用时，一个人修改模型设置会影响所有人
- **建议**：如果是教学场景，建议教师统一设置模型，学生只使用问答功能

如果需要更好的多用户支持，可以考虑：
- 部署多个 Ollama 实例
- 使用 Ollama 的负载均衡功能
- 或使用方式四（自建服务器）部署，通过 Nginx 做反向代理

---

### 问题 23：Ollama 安全注意事项

- Ollama 默认没有认证机制，任何能访问 11434 端口的人都能使用你的模型
- 如果在公网部署，务必通过防火墙限制访问，或使用 Nginx 添加认证
- 不要在公共网络上暴露 Ollama 端口

```bash
# 只允许本机访问（默认，最安全）
# 不设置 OLLAMA_HOST，或设置为：
export OLLAMA_HOST=127.0.0.1

# 只允许局域网访问
export OLLAMA_HOST=0.0.0.0
# 但配合防火墙只允许特定 IP 访问 11434 端口
```

---

## 功能概述

| 功能模块 | 页面 | 说明 |
|----------|------|------|
| 系统总览 | 首页 | 模型状态、数据统计卡片、系统架构图、安全声明 |
| 智能问答 | 软物质智能问答 | 基于 RAG 的课程问答，展示证据来源与置信度 |
| 文献检索 | 文献知识检索 | 结构化文献记录搜索，支持 CSV/TXT/Markdown 导入 |
| 配方查询 | 实验配方库 | 实验配方检索、安全等级标注、教师复核提示 |
| 方案生成 | 实验方案助手 | 输入研究目标，生成教学版实验方案框架 |
| 表征分析 | 表征结果分析 | 文字描述分析，基于规则匹配给出结构解释建议 |
| 材料对比 | 材料体系对比 | 预设主题与自定义材料对比，输出对比表格 |
| 教师面板 | 教师分析面板 | 高频关键词、反馈统计、弱点总结、复习建议 |
| 系统设置 | 系统设置 | Ollama 连接检测、模型管理、服务地址配置 |

## 目录结构

```
softmatter-gpt/
├── app.py                  # Streamlit 前端入口
├── api_server.py           # FastAPI 后端入口
├── config.py               # 全局配置
├── requirements.txt        # Python 依赖清单
├── core/                   # 核心业务模块
│   ├── data_loader.py      # 数据加载
│   ├── retriever.py        # 课程知识库检索
│   ├── literature_processor.py  # 文献记录解析与检索
│   ├── recipe_extractor.py # 实验配方抽取与检索
│   ├── characterization.py # 表征结果辅助分析
│   ├── llm_client.py       # Ollama / LLM 调用
│   ├── prompt_templates.py # Prompt 模板管理
│   ├── safety_checker.py   # 实验安全审核
│   ├── qa_logger.py        # 问答日志与反馈
│   └── analytics.py        # 教师统计分析
├── pages/                  # Streamlit 多页面
│   ├── 1_首页.py
│   ├── 2_软物质智能问答.py
│   ├── 3_文献知识检索.py
│   ├── 4_实验配方库.py
│   ├── 5_实验方案助手.py
│   ├── 6_表征结果分析.py
│   ├── 7_材料体系对比.py
│   ├── 8_教师分析面板.py
│   └── 9_系统设置.py
├── data/                   # 数据文件
│   ├── softmatter_knowledge.csv
│   ├── literature_records.csv
│   ├── experiment_recipes.csv
│   ├── sample_questions.csv
│   ├── feedback.csv
│   └── settings.json
├── logs/                   # 运行日志
│   └── qa_history.csv
├── assets/                 # 静态资源
│   ├── architecture.png    # 系统架构图
│   └── rag_flow.png        # RAG 流程图
└── docs/                   # 项目文档
    ├── 软件说明书.md
    ├── 演示流程.md
    └── 答辩讲稿.md
```

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/system/status` | GET | 系统状态信息 |
| `/api/models` | GET | 获取 Ollama 模型列表 |
| `/api/model/current` | GET/POST | 获取或设置当前模型 |
| `/api/model/test` | POST | 测试当前模型 |
| `/api/ollama/status` | GET | Ollama 服务连接状态 |
| `/api/ollama/url` | POST | 设置 Ollama 服务地址 |
| `/api/ask` | POST | 软物质智能问答 |
| `/api/search` | POST | 课程知识库检索 |
| `/api/literature/search` | POST | 文献记录检索 |
| `/api/recipe/search` | POST | 实验配方检索 |
| `/api/experiment-plan` | POST | 实验方案生成 |
| `/api/characterization/analyze` | POST | 表征结果辅助分析 |
| `/api/compare` | POST | 材料体系对比 |
| `/api/feedback` | POST | 保存用户反馈 |
| `/api/teacher/analysis` | GET | 教师分析数据 |

所有 API 端点均需 `X-API-Key` 请求头认证。

## 数据说明

| 数据源 | 当前条数 | 说明 |
|--------|----------|------|
| 课程知识库 | 60 条 | 人工编写的软物质教学知识条目 |
| 文献记录 | 27 条 | 教学示例数据，标注为 curated_example |
| 实验配方 | 30 条 | 教学示例数据，标记 is_example=true |
| 测试问题 | 25 条 | 覆盖流变学、胶体、高分子、乳液等方向 |
| 反馈记录 | 6 条 | 包含 5 条演示反馈和 1 条测试记录 |

文献记录和实验配方当前为教学示例数据，非真实文献解析结果。系统支持后续导入真实数据以扩充知识库。

## 安全声明

- 本系统输出的实验方案仅为教学参考框架，不构成可直接执行的实验操作 SOP。
- 涉及高风险试剂（强酸、强碱、液氮等）、高温高压等实验条件时，系统会自动标记需教师复核。
- 所有基于 LLM 生成的回答均附带证据来源和置信度标注，证据不足时系统会明确提示。
- API 端点采用密钥认证，Ollama 地址设置包含 SSRF 防护。
- 输入参数经 Pydantic 校验，防止非法数据注入。

## 已知限制

1. Ollama 需要在本地安装并启动后才能使用 LLM 生成功能，离线状态下仅可使用检索和规则分析功能。
2. 当前数据为教学示例规模（共 122 条），系统已预留批量导入接口，支持后续扩展至数百条规模。
3. 表征结果分析基于规则匹配实现，未接入多模态视觉模型，暂不支持直接分析图片文件。
4. PDF 批量解析脚本已预留接口，当前未执行大规模 PDF 解析任务。

## 致谢

- 课程知识库内容参考了软物质科学领域经典教材与公开文献。
- 大语言模型能力由 Ollama 项目提供，支持 Qwen、DeepSeek、Gemma、Llama 等开源模型。
- 前端界面基于 Streamlit 框架构建，数据可视化使用 Plotly 和 Matplotlib。
- 项目开发过程中得到了课程教师的指导和建议。

## 许可证

本项目仅用于教学目的。项目代码、文档和数据集均以教学示例形式提供，不对外发布为正式软件产品。如需二次开发或引用，请注明出处并遵守相关开源组件的许可协议。
