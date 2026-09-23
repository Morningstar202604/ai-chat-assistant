# AI 对话助手

单文件纯前端 AI 对话助手，兼容 OpenAI 风格接口，无需后端、无需构建，数据仅存本地浏览器。

## 功能特性

### 对话核心
- 多轮流式对话，支持流式增量 Markdown 渲染
- 自研轻量 Markdown 解析（先转义防 XSS），代码块未闭合时安全降级
- 代码高亮（highlight.js）、数学公式（KaTeX）、流程图（Mermaid）按需懒加载
- HTML 代码沙箱预览（iframe sandbox）
- 消息编辑、删除、引用、重新生成、富文本复制（同时写入 HTML + 纯文本）
- 语音朗读（Web Speech Synthesis）
- 自动压缩长对话（超过 token 阈值时自动摘要较早历史）
- 自动生成会话标题（首轮回复后调用模型概括）

### 多模态
- 图片上传：支持按钮选择、粘贴、拖拽，自动压缩至合理尺寸（最多 4 张）
- 图片灯箱查看
- 图像生成：调用 `/images/generations` 端点，可配置独立图像模型

### 知识与记忆
- RAG 知识库：上传文档后自动分块，支持 BM25 关键词检索 + 向量嵌入混合检索
- 长期记忆：对话后自动提取用户事实，支持手动添加/删除/清空
- 提示词模板：7 个预设模板，输入 `/` 快速唤起，可应用到当前会话

### 工具与 Agent
- 内置工具：当前时间查询、安全数学计算器（白名单字符，不使用 eval）
- Agent 多轮推理循环：模型可连续调用工具多步推理，最多 5 轮，重复调用自动检测终止
- 联网搜索：按接口自动适配（智谱 GLM / 通义千问 / OpenAI / Kimi），不支持时自动降级
- 快捷工作流：多步链式提示词，3 个预设（总结→翻译→润色、代码审查→优化→解释、大纲→撰写→润色），支持自定义新建/编辑/删除

### 数据与存储
- IndexedDB 主存储（会话 + 记忆），隐私模式自动降级 localStorage
- API Key 可选加密存储（Web Crypto AES-GCM + PBKDF2，10 万次迭代）
- 全量数据导出/导入（JSON 备份）
- 会话管理：新建、搜索、重命名、删除、清空
- 输入草稿自动保存（切会话后恢复）

### 界面与体验
- 深色 / 浅色 / 跟随系统三种主题，首帧防闪烁（FOUC 脚本）
- 响应式布局：桌面 / 平板 / 手机 / 极窄屏（<360px）
- 移动端手势滑出侧边栏
- 命令面板（Ctrl/Cmd+K）：快速操作、会话搜索、消息全文搜索
- 多模型对比模式：2-3 列并发提问，逐列流式输出
- 快捷键：Ctrl/⌘+N 新建、Ctrl/⌘+S 设置、Ctrl/⌘+K 命令面板、Ctrl/⌘+B 侧边栏、Ctrl/⌘+L 清空输入、Alt+←/→ 切换会话
- 语音输入（Web Speech Recognition，Chrome/Edge 支持）
- 断网自动提示条，恢复后通知
- 运行时错误日志查看（最近 20 条，可复制/清空）
- 消息密度切换（舒适 / 紧凑）
- Token 实时估算（输入 + 会话）
- 文件上传解析：TXT / Markdown / CSV / JSON / PDF / DOCX / XLSX / 常见代码文件，单文件上限 5 万字符
- CSV 数据分析 + ECharts 图表生成

## 架构说明

- **单文件**：整个应用就是一个 `AI对话助手.html`，无外部 JS/CSS 依赖（除 CDN 懒加载）
- **无后端无构建**：双击打开即可使用，不需要 Node、不需要打包
- **接口**：只调 OpenAI 兼容的 `/chat/completions`、`/images/generations`、`/embeddings` 端点
- **Key 存储**：默认明文存 localStorage，可选开启密码加密（Web Crypto AES-GCM）
- **CDN**：所有第三方库通过 jsDelivr CDN 懒加载，加载失败自动降级（无高亮/无公式等）
- **隐私**：所有数据只在本地浏览器，不向任何服务器发送（除用户配置的 API 端点）

## 快速开始

### 使用
直接用浏览器打开 `AI对话助手.html` 即可。建议使用 Chrome / Edge 以获得最佳体验。

### 配置 API
1. 点击侧边栏底部「接口设置」（或顶栏齿轮图标，快捷键 Ctrl/⌘+S）
2. 在「接口与模型」标签页：
   - 选择接口预设（自动填入地址和模型列表）
   - 或手动填写接口地址（Base URL）和 API Key
   - 填写模型名称（如 `deepseek-chat`、`gpt-4o-mini` 等）
3. 点击「保存」
4. 在输入框输入消息，Enter 发送

### 支持的接口供应商
任何兼容 OpenAI 风格的接口均可使用，内置预设：
- **DeepSeek** — `api.deepseek.com`
- **OpenAI** — `api.openai.com`
- **Kimi (Moonshot)** — `api.moonshot.cn`
- **通义千问 (阿里)** — `dashscope.aliyuncs.com`
- **智谱 GLM** — `open.bigmodel.cn`
- **豆包 (火山方舟)** — `ark.cn-beijing.volces.com`
- **Agnes AI** — 免费额度
- **自定义** — 任意 OpenAI 兼容接口

## 技术栈与依赖

### 原生技术
- HTML5 / CSS3 / 原生 JavaScript（ES2020+，无框架无构建）
- CSS 变量设计系统（圆角 / 间距 / 字号 / 阴影 / 语义色）
- 响应式布局（Flexbox + Grid + 媒体查询）

### CDN 依赖（jsDelivr 懒加载，失败自动降级）
| 库 | 版本 | 用途 |
|---|---|---|
| highlight.js | 11.9.0 | 代码语法高亮 |
| KaTeX | 0.16.9 | LaTeX 数学公式渲染 |
| Mermaid | 10.9.0 | 流程图 / 时序图渲染 |
| PapaParse | 5.4.1 | CSV 文件解析 |
| pdf.js | 3.11.174 | PDF 文件文本提取 |
| mammoth | 1.6.0 | DOCX 文件文本提取 |
| SheetJS (xlsx) | 0.18.5 | XLSX 表格解析 |
| ECharts | 5.5.0 | CSV 数据可视化图表 |

### Web API 使用
- **IndexedDB** — 会话和知识库主存储，自动降级 localStorage
- **Web Crypto (SubtleCrypto)** — API Key 加密（PBKDF2 + AES-GCM）
- **Web Worker** — 余弦相似度计算、轻量 Markdown 渲染（Blob URL 自包含）
- **Web Speech API** — 语音输入（SpeechRecognition）和朗读（SpeechSynthesis）
- **Clipboard API** — 富文本复制（ClipboardItem，降级 execCommand）
- **AbortController** — 请求取消、超时控制
- **Fetch + ReadableStream** — SSE 流式输出解析
- **File API / Blob** — 文件上传、导出下载
- **matchMedia** — 主题跟随系统、减少动画偏好

## 项目结构

```
ai-chat/
├── AI对话助手.html          # 主程序（单文件，全部功能）
├── README.md                # 本文件
├── LICENSE                  # MIT 开源协议
└── _backup/                 # 历史版本备份（开发用，可删除）
    └── AI对话助手_v10_5001.html
```

## 限制与免责声明

### API Key 安全提醒
- API Key 默认明文存储在浏览器 localStorage 中，**请勿在公共设备上使用**
- 可在设置中开启「加密存储 API Key」，使用密码 + Web Crypto 加密，但：
  - 密码丢失后无法恢复
  - 无法防御恶意浏览器扩展读取内存中的 Key
- 应用本身不会向任何第三方服务器发送 Key

### 纯前端架构的能力边界
- 无代码沙箱：模型生成的代码仅在沙箱 iframe 中预览，不会在应用内执行
- 无实时语音通话：仅支持短语音输入转文字和文本朗读
- 无大规模向量检索：知识库为本地小型文档集合（建议 < 50 份文档），BM25 + 轻量嵌入混合检索
- 无服务端会话：所有对话历史只存本地，换浏览器/清缓存会丢失（建议定期导出备份）

### 其他
- CDN 依赖需要网络连接，首次使用代码高亮/公式/流程图时会加载对应库
- 应用不提供任何 API 服务，用户需自备 OpenAI 兼容接口的 API Key
- 流式输出效果取决于接口对 SSE 的支持程度

## 开源协议

MIT License — 详见 [LICENSE](LICENSE) 文件。
