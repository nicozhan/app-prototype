# VendSolution · App Prototype

VendSolution（AIoT + SaaS 无人零售）手机运维 App 的 HTML 原型，共 **46 个页面**，统一 **390×844** 视口与一套共享设计系统 `app-ui.css`。

> 纯静态 HTML/CSS/JS，无构建步骤。打开 `index.html` 选择端；直接打开 `navigation.html` 即可当 App 用（可点击跳转）。

---

## 快速开始

```bash
npm start              # 本地起服务（默认 http://localhost:3000，入口选择页）
open index.html        # 入口选择页：App Demo / Web 后台
open navigation.html   # 直接进 Demo App（首页 / 消息 / 常用 / 全屏菜单）
open nav.html          # 全部页面索引
open style-guide.html  # 设计标准（C3 卡片规范）
open figma-pixel.html  # 改造前 Figma 1:1 对照稿（归档，不参与统一改造）
```

---

## 部署（Railway）

仓库根就是部署根，`npm start` 起一个无依赖的 Node 静态服务（`server.js`），端口读 `PORT`。

```
/            入口选择页 index.html  →  App Demo（/navigation.html）
                                   →  Web 后台 Demo（/vend-solution-reports.html#/devicecfg/brand，新标签打开）
```

线上示例（Railway）：`https://nicodemo.up.railway.app/` 为入口，`/navigation.html` 是 App，`/vend-solution-reports.html#/devicecfg/brand` 直接落在后台「品牌型号与组件 · 品牌」。

- **Railway 设置**：新建项目 → Deploy from GitHub repo → 选本仓库，其余保持默认。不需要环境变量、不需要构建命令，`railway.json` 已指定 `startCommand` 与健康检查 `/healthz`。
- **Web 后台是原型页**：`vend-solution-reports.html`（报表与分析，单文件自包含）从早期 Web 后台原型迁入，不连真实接口。要换成线上后台，改 `index.html` 里 Web 卡片的 `href` 与下方域名文本即可。
- **不想公开访问**：Railway 服务 → Settings → 生成域名后，可用 Variables 或 Railway 的 Access Control 限制；原型不含真实数据，但包含内部业务结构。
- `server.js` 已屏蔽 `.git` / `.workbuddy` / `shots` / `new` / `jpgk-platform` 等非页面目录，且防止路径穿越。

---

## 目录结构

```
├── index.html                # 入口选择页（App Demo / Web 后台）
├── vend-solution-reports.html # Web 后台原型（报表与分析，单文件）
├── server.js                 # Railway 静态服务（无依赖）
├── package.json              # 启动脚本
├── railway.json              # Railway 部署配置
├── app-ui.css                # 共享设计系统（令牌 + 组件）· 单一来源
├── app-ui.js                 # 共享行为（返回 / 回首页 / 退出登录 / 远程开锁 / 设备状态同步）
├── navigation.html           # Demo App 入口
├── nav.html                  # 页面导航（全部页面）
├── figma-pixel.html          # 改造前 1:1 对照稿（归档）
├── style-guide.html          # 设计标准说明
│
├── 主流程   login / my / scan / device-single-door / device-double-door / device-coffee / device-vending
│           cabinet-restock-c / vending-restock / restock-list / restock-form
│           restock-done / inventory
├── 补货方案 cabinet-restock-a / cabinet-restock-b / restock / restock-door
├── 告警通知 alerts / alert-detail / alert-detail-design / notifications / notification-detail
├── 商品经营 products / product-detail / rank-product / rank-site / site-product / material / stats
├── 系统     home / machines / nav / style-guide
└── app_workorder/            # 工单模块 A01–A09（引用 ../app-ui.css）
```

---

## 页面清单

| 模块 | 页面 |
|---|---|
| 登录 / 账户 | 登录（四语 · 免密码）、我的 |
| 首页 / 设备 | Demo 导航页（在线 / 离线 / 未知 / 全部筛选 · 右上扫码）、扫码识别设备（相机取景 → 单门柜设备页）、功能宫格、设备列表、单门开门柜（右上盘点）、双门开门柜、咖啡机、售卖机 |
| 补货 | 单门柜补货（方案 C，双门柜左右门复用；弹层内可选保质期：忽略 / 按生产日期 / 按到期时间）、售卖机货道补货（按货道 / 按商品切换）、咖啡机料仓列表、料仓补货表单、补货完成（拍照上传 + 补货详情）、库存盘点（记录可按近 7 天 / 近 1 个月 / 近 3 个月 / 自定义时间段筛选，差异增加标红、减少标绿） |
| 补货方案（历史） | 方案 A、方案 B、早期稿、开门柜中文版 |
| 经营统计 | 统计主页、商品销量排行、点位销量排行、点位原料统计、点位商品销售统计、商品列表、商品详情 |
| 告警 / 通知 | 告警列表、告警详情、卡片选型对比稿、通知列表、通知详情 |
| 工单 | 我的工单 A01、待认领 A02、详情 A03、记录进展 A04、完工提交 A05、等待反馈 A06、恢复处理 A07、转派 A08、退回返工 A09 |

---

## 设计系统 `app-ui.css`

所有页面在 `<head>` 引用同一份样式，页面级样式只写私有部分（类名加页面前缀），**不覆盖**组件类。

### 设计令牌

| 用途 | 变量 | 值 |
|---|---|---|
| 品牌主色 / 深色 | `--brand` / `--brand-deep` | `#2434C8` / `#1B299E` |
| 品牌浅底 / 描边 | `--brand-weak` / `--brand-line` | `#EDF0FF` / `#DCE2FF` |
| 正文 / 次要 / 辅助 | `--ink` / `--text-2` / `--text-3` | `#0B102F` / `#697095` / `#9AA1B7` |
| 页面底 / 卡片 / 次级面 | `--bg` / `--surface` / `--surface-2` | `#F5F6FA` / `#FFF` / `#F0F2F8` |
| 分隔线 | `--line` | `#E4E7EF` |
| 成功 | `--ok` / `--ok-bg` | `#008F63` / `#E8F7F1` |
| 警示（库存偏低 / 等待） | `--warn` / `--warn-bg` | `#9A5E2A` / `#FFF4E8` |
| 危险（缺货 / 失败 / 下架） | `--danger` / `--danger-bg` | `#D92D20` / `#FFF0EF` |
| 品牌点缀（仅装饰） | `--orange` | `#FF7A00` |

### 组件

`.app`（外壳）· `.status` · `.navbar` · `.body` · `.footer` · `.btn(-primary/-secondary/-ghost/-danger/-danger-weak/-sm/-xs/-block)` · `.card(-head/-title/-body/-foot)` · `.list` / `.item(-body/-name/-sub/-meta/-go/-icon)` · `.thumb` · `.badge(.brand/.ok/.warn/.danger)` · `.dot` · `.qty` · `.rows` / `.row` · `.stats` / `.stat` · `.segmented` · `.filter-select` · `.chips` / `.chip` · `.tabs` / `.tab` · `.field` / `.input` / `.textarea` / `.select` · `.search` · `.radio` · `.overlay` / `.sheet` / `.sheet-note` / `.sheet-btns` · `.ops`（远程操作按钮组） · `.empty` · `.steps` / `.step` · `.toast`

### 硬规则

1. **字数重**只用 400 / 600 / 700 / 800。
2. **圆角**：卡片 16、控件 12、小件 10。不使用重阴影（仅 `.app` 桌面外框例外）。
3. **留白**：页面左右 16px。
4. **橙色只作品牌点缀**，不承担警告含义；缺货用 `--danger`、库存偏低用 `--warn`、补齐用 `--ok`。
5. **禁止**用 `position:absolute` 还原整页或固定像素画布，一律流式布局；超一屏滚动 `.body`，主操作固定在 `.footer`。
6. 每屏只有一个主操作；双门柜「左门补货 / 右门补货」是唯一例外（两个对等主操作）。危险动作（下架、退出、删除）需二次确认。

### 底部导航显隐（对齐 Uber Eats / Shopify）

`navigation.html` 给每个页面标一个层级，存在 `PAGE_CHROME` 表里，未登记的页面默认 `focus`：

| 层级 | 底部 dock | 适用 | 页面 |
|---|---|---|---|
| `tab` | **显示** | 一级目的地、分区根，用户随时能回首页 | 首页 / 消息 / 常用（内置），`machines` `products` `stats`（从「全部」进入，汉堡入口高亮） |
| `focus` | **隐藏** | 对象详情、单任务，靠页面自己的返回 + 唯一主 CTA | 四类设备详情、告警与通知、工单全链路、商品详情、盘点、补货完成、`my` 等 |
| `immersive` | **隐藏** | 相机与执行中的任务，页面完全占满 | `scan` `cabinet-restock-c` `vending-restock` `restock-form` `inventory` |

规则：
- `focus` / `immersive` 页面**必须自带顶栏返回**（`onclick="appBack(event)"`），因为 dock 不再兜底。
- 页面内部跳转（分区页 → 详情页）时，外壳监听 `iframe` 的 `load` 重新判定层级，dock 会自动收起。
- 回到内置视图（或页面发 `app:home`）时 dock 自动恢复。

---

## 开发约定

1. **单一设计系统**：只改 `app-ui.css`，不在页面里重写组件规则。
2. **页面私有样式**加前缀（如 `.alert-xxx`、`.tk-xxx`），避免污染其他页面。
3. **子目录页面**（`app_workorder/`）引用 `../app-ui.css`。
4. **安全区**：`viewport-fit=cover` + `env(safe-area-inset-*)`。
5. **新页面**：复制 `my.html` 的骨架（`.app → .status → .navbar → .body → .footer`），完成后加入 `nav.html`。

> `vend.css` / `app_workorder/vend.css` 是改造前的旧令牌体系（Inter + 393 画布 + 重阴影），现已无页面引用，仅作历史归档保留，**不要在新页面中使用**。
> `index.html` 是入口选择页（App Demo / Web 后台）；改造前的 Figma 1:1 像素对照稿已改名为 `figma-pixel.html`，关闭导航显隐，仅用于比对视觉差异，不属于 App 页面。

---

## 已知限制

- 原型为静态 HTML，交互为前端模拟（免密码登录、开锁、补货、盘点均为本地状态），未接后端。
- 真实接入需转写为 Uni-app 3 + Vue 3 SFC（生产仓库 `jpgk-platform/mobile/`）。
