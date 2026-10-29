# VendSolution App 设计规范

> 适用对象：VendSolution 移动端（自动售货运营）HTML 原型全部页面
> 设计基准：iPhone 15（逻辑宽 **393** × 高 **852**）
> 样式来源：`vend.css`（根）与 `app_workorder/vend.css`（工单副本，需保持同步）
> 可视化参考：`style-guide.html`（卡片标准 C3）、`nav.html`（页面导航）
> 最后更新：2026-10-25

---

## 1. 设计原则

| 原则 | 说明 |
|---|---|
| **严重度优先** | 颜色只用于表达「严重度 / 优先级 / 状态」，不做装饰。用户第一眼应看到最紧急的事 |
| **一屏一事** | 852 首屏必须完整呈现当前页的主信息与主要操作，避免"翻页才知道有什么" |
| **密度克制** | 移动端优先压缩页头与内边距，一个卡片最多承载 4 类信息（严重度 / 标题 / 属性 / 操作） |
| **一致性 > 个性** | 新页面一律复用既有组件类，不新增卡片变体 |
| **安全区原生** | 所有固定头部/底部必须叠加 `env(safe-area-inset-*)` |

---

## 2. 设计令牌（Design Tokens）

### 2.1 品牌色

| 令牌 | 色值 | 用途 |
|---|---|---|
| `--blue` | `#2434C8` | 主色：页头渐变起点、主按钮、选中态、链接 |
| `--blue-deep` | `#1B299E` | 页头渐变终点 |
| `--ink` | `#0B102F` | 主文字 |
| `--gray` | `#697095` | 次要文字、占位、已关闭态 |
| `--orange` | `#FF7A00` | 运营告警、P1 警告、等待反馈 |
| `--green` | `#00A76F` | 成功、已完成、待认领 |
| `--red` | `#E5484D` | 严重（P0）、待处理、必填、错误 |

### 2.2 背景与描边

| 令牌 | 色值 | 用途 |
|---|---|---|
| `--bg` | `#EEF2FF` | 淡蓝底：图标块、选中胶囊底、Tag 底 |
| `--bg-soft` | `#F8F9FF` | 页面底色、输入框底、Chip 底 |
| `--line` | `#E3E7FF` | 默认描边、分隔线 |
| `#F0F3FC` | — | 卡片内部分隔线（比 `--line` 更浅） |
| `#C9D2F5` | — | P2 描边/光晕边框、虚线框、禁用图标 |
| `#9AA1BC` | — | 单号 / 时间戳等弱文本 |
| `--orange-bg` | `#FFF4EB` | 橙 Tag / 提示条底 |
| `--green-bg` | `#E6F9F1` | 绿 Tag 底 |
| `--red-bg` | `#FDEBEC` | 红 Tag / 错误提示条底 |

### 2.3 阴影与圆角

| 令牌 | 值 | 用途 |
|---|---|---|
| `--shadow` | `0 10px 28px rgba(36,52,200,.06)` | 所有卡片默认阴影 |
| 按钮阴影 | `0 12px 24px rgba(36,52,200,.25)` | `.btn-primary` |
| 下拉阴影 | `0 12px 28px rgba(36,52,200,.14)` | `.drop` |
| 浮层阴影 | `0 18px 40px rgba(11,16,47,.35)` | `.navmenu` |
| `--r` | `16px` | 列表行 `.row`、`.card` |
| 卡片 | `14px` | `.sect`、`.dcard`、`.tkcard`、主按钮 |
| 标准卡 | `14px` | **`.acard`（C3 标准）**、输入框、按钮、缩略图 |
| 小件 | `10–11px` | 下拉、图标块、Tab |
| 胶囊 | `999px` | Tag / Chip / Badge / 状态 |

> **圆角规则**：容器越大角越圆。卡片 12–14，内部控件 8–10，标签一律 999。

### 2.4 字体

```css
font-family:'Inter', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

- 数字/时间等需要对齐的文本：`ui-monospace, Menlo, monospace`
- 字重阶梯：`400 / 500 / 600 / 700 / 800`
- 开启 `-webkit-font-smoothing:antialiased`

### 2.5 字号阶梯

| 级别 | 字号 / 字重 | 应用 |
|---|---|---|
| H1 | 27 / 800 | `.hero .pagetitle` 首页大标题 |
| H2 | 19 / 800 | `.section h2` 板块标题 |
| 页标题 | 16.5–18 / 700–800 | `.dtop .title`、`.ttop .title` |
| 卡标题 | 16 / 800 | `.acard .atitle` |
| 卡标题（次） | 14.5–15 / 700 | `.tktitle`、`.row .name` |
| 区块标题 | 14–15 / 800 | `.sect h3`、`.dcard h3` |
| 正文 | 13–13.5 / 400–600 | 表单输入、正文段落 |
| 字段 | 12.5 / 400–700 | `.frow`、`.flabel` |
| 次要 | 11.5–12 / 500–600 | `.sub`、`.tkmeta`、时间戳 |
| 微标签 | 10–11 / 700–800 | `.alvl`、`.tkpri`、`.achip` |

---

## 3. 布局与适配

### 3.1 画布

```css
.screen{ width:393px; min-height:852px; margin:0 auto;
  background:var(--bg-soft); position:relative; overflow:hidden; }
```

- 逻辑宽固定 **393**，不做响应式断点（原型阶段）
- 桌面预览时 `body` 背景 `#c9cddb`，`.screen` 居中

### 3.2 安全区（必写）

```html
<meta name="viewport" content="width=device-width,initial-scale=1,
      viewport-fit=cover,maximum-scale=1">
```

| 位置 | 写法 |
|---|---|
| 顶部固定栏 | `padding-top: calc(12px + env(safe-area-inset-top))` |
| 底部固定栏 | `padding-bottom: calc(10px + env(safe-area-inset-bottom))` |
| 页面整体 | `min-height:100dvh` + `padding-bottom: calc(30px + env(safe-area-inset-bottom))` |

### 3.3 间距栅格

| 场景 | 值 |
|---|---|
| 页面左右边距（工单 / 统计） | `14px` |
| 页面左右边距（首页 / 商品 / 设备） | `20px` |
| 卡片纵向间距 | `9–12px` |
| 区块卡内边距 | `12–13px` |
| 卡片内元素间距 | `5–9px` |
| 图标与文字间距 | `4–7px` |

### 3.4 层级 z-index

| 层 | z-index |
|---|---|
| 下拉 / 导航菜单 / `.drop` | 30 |
| 固定底栏 `.dobot` | 40 |
| 弹窗遮罩 `.sheetmask` | 50 |
| 底部弹窗 `.sheet` | 60 |
| Toast | 80 |

---

## 4. 页面结构

### 4.1 四种页头（按页面类型选一，勿混用）

| 类型 | 类 | 适用 |
|---|---|---|
| 蓝色渐变页头 | `.hero` | 首页、一级业务页（含品牌行 + 大标题 + 操作按钮） |
| 白色顶栏 | `.topbar` | 简单一级页（返回 + 标题 + 图标按钮） |
| 列表页头 | `.ttop` | 工单 / 告警列表（标题 18/800 + 右侧「筛选」胶囊） |
| 详情/二级页头 | `.dtop` | 二级详情、统计页（三列 grid `62px 1fr 62px`） |

**`.dtop` 骨架**

```html
<div class="dtop">
  <a class="back" href="...">‹ 返回</a>
  <div class="title">页面标题</div>
  <span class="right"><!-- 右侧操作 --></span>
</div>
```

### 4.2 底部

| 组件 | 用途 |
|---|---|
| `.tabbar` | 底部 4 项主导航（工作台 / 工单 / 消息 / 我的），图标 21px、文字 10.5px，选中蓝色加粗 |
| `.dobot` | 详情页固定操作栏（`.row2` 横排 2–3 个按钮） |

```html
<div class="dobot">
  <div class="row2">
    <a class="abtn ghost" href="#">记录进展</a>
    <a class="abtn" href="#">提交完工</a>
  </div>
</div>
```

---

## 5. 卡片标准 · C3（全局强制）

> 这是**唯一的列表卡片标准**。所有自主设计页面的列表项一律使用 `.acard`，不得新增变体。
> 原型参考：`alert-detail-design.html`（C1–C4 对比，最终采用 **C3 · 描边 / 发光实心徽章**）

### 5.1 结构

```
┌────────────────────────────┐ ← 整圈描边 2px + 同色光晕（按严重度取色）
│ [P0 · 严重]      (待处理 ●) │ ← 实心等级徽章（左）| 软底状态胶囊（右）
│ 柜内温度过高                │ ← 标题 16/800
│ (设备告警) (SN0020301) (…)  │ ← 属性 chips（浅底细描边）
│ 2026/10/25 14:40    [查看→] │ ← 等宽时间 | 实心按钮
└────────────────────────────┘
```

### 5.2 骨架

```html
<a class="acard p0" href="alert-detail.html">
  <div class="ain">
    <div class="atop">
      <span class="alvl">P0 · 严重</span>
      <span class="ast2 s-todo"><span class="tdot"></span>待处理</span>
    </div>
    <div class="atitle">柜内温度过高</div>
    <div class="achips">
      <span class="achip dev">设备告警</span>
      <span class="achip">SN0020301</span>
    </div>
    <div class="afoot">
      <span class="atime">2026/10/25 14:40</span>
      <span class="abtn">查看 →</span>
    </div>
  </div>
</a>
```

双操作按钮场景（如「查看详情 / 认领工单」）用 `.aacts` + `.abt2` 替代 `.afoot`：

```html
<div class="aacts">
  <a class="abt2 ghost" href="#">查看详情</a>
  <a class="abt2" href="#">认领工单</a>
</div>
```

详情页状态头使用同款变体：`.sect.sev.p0` + `.sin`（描边 + 光晕，无顶部色条、无浅色底）。

### 5.3 严重度 / 优先级配色

| 档位 | 类名 | 描边 | 光晕（box-shadow） | 实心徽章 / 按钮 |
|---|---|---|---|---|
| 严重 | `.p0` | `#E5484D` 红 2px | `0 0 0 3px rgba(229,72,77,.10)` + `0 8px 20px rgba(229,72,77,.14)` | 红底白字 |
| 警告 | `.p1` | `#FF7A00` 橙 2px | `0 0 0 3px rgba(255,122,0,.08)` + `0 8px 18px rgba(255,122,0,.10)` | 橙底白字 |
| 提示 | `.p2` | `#C9D2F5` 浅蓝灰 2px | `0 0 0 3px rgba(122,132,168,.07)` + `0 6px 16px rgba(36,52,200,.06)` | `#7A84A8` 底白字 |

> 卡片底色统一**纯白**，严重度由「描边颜色 + 光晕强度」表达。光晕必须**逐档递减**：P0 最强、P1 约减半、P2 仅留极淡一圈，否则整页发光会失去分级意义。
> 操作按钮（`.abtn`）与徽章（`.alvl`）同为实心填充 + 白字，按钮取同档颜色。

**业务映射**

| 业务 | 映射 |
|---|---|
| 告警等级 | P0 → `.p0` ／ P1 → `.p1` ／ P2 → `.p2` |
| 工单优先级 | P1 → `.p0` ／ P2 → `.p1` |

### 5.4 状态配色

| 状态 | 类名 | 文字/色点 | 胶囊底色 | 语义 |
|---|---|---|---|---|
| 待处理 | `.s-todo` | `#E5484D` 红 | `--red-bg` | 未响应，需立即处理 |
| 处理中 | `.s-doing` | `#2434C8` 蓝 | `--bg` | 已接单处理中 |
| 等待反馈 | `.s-warn` | `#FF7A00` 橙 | `--orange-bg` | 挂起等待外部反馈 |
| 待认领 | `.s-claim` | `#00A76F` 绿 | `--green-bg` | 待分配 |
| 已完成 | `.s-done` | `#00A76F` 绿 | `--green-bg` | 终态成功 |
| 已关闭 / 待审核 | `.s-closed` | `#697095` 灰 | `#F1F3FA` | 终态 / 待审核 |

> 状态为「软底胶囊 + 色点 + 文字」三件套，禁止仅用颜色表达状态（无障碍要求）。胶囊与实心等级徽章形成「实心 / 空心」层次对比。

### 5.5 卡片内容规则

1. 严重度只取 `p0 / p1 / p2`，颜色与光晕由类决定，禁止内联写死
2. 空值（`—`）**不渲染**为 chip，直接省略
3. 列表排序：最高严重度置顶，同级按时间倒序
4. 标签最多 4 个 chip，超出折叠为 `+N`
5. 卡片整体可点击（`<a>` 包裹）；若卡内有独立按钮，卡体改为 `<div>`，按钮单独绑定
6. 同一列表中**光晕强度不可拉平**，必须保持 P0 > P1 > P2 的视觉落差

---

## 6. 组件库

### 6.1 按钮

| 类 | 规格 | 用途 |
|---|---|---|
| `.btn-primary` | 通栏（宽 `calc(100% - 40px)`）、16/700、padding 16、圆角 14、带蓝色投影 | 页面唯一主操作 |
| `.abtn` | `flex:1`、14/700、padding 13、圆角 12、蓝底白字 | 底栏 / 横排按钮 |
| `.abtn.ghost` | 白底蓝字 + 蓝边 | 次操作 |
| `.abtn.wide` | `flex:1 1 100%` | 整行独占 |
| `.abt2` | 12/700、padding 8×10、圆角 8 | 卡内小按钮 |
| `.tkview` / `.abtn`（卡内） | 11.5–12/700、`--bg` 底、圆角 8–999 | 卡片「查看 →」 |
| `.iconbtn` | 36×36、圆角 12、`--bg` 底、图标 18px | 页头图标按钮 |
| `.toolbtn` | 38×38、圆角 12、白底 + 描边 | 搜索行工具按钮 |

### 6.2 徽章 / 标签 / Chip

| 类 | 规格 | 场景 |
|---|---|---|
| `.badge` + `.b-blue/.b-green/.b-orange/.b-red/.b-gray` | 11/600、padding 4×10、圆角 999 | 状态徽章（通用） |
| `.alvl` + `.p0/.p1/.p2` | 10/800、圆角 6 | 告警等级（描边卡外使用） |
| `.tkpri` + `.pri-p1/.pri-p2/.pri-p3` | 10/800、圆角 6 | 工单优先级 |
| `.atag` + `.dev/.ops` | 10/700、圆角 6、带描边 | 告警类型（设备蓝 / 运营橙） |
| `.achip` | 11/600、padding 4×8、圆角 999、`--bg-soft` 底 + 细描边 | C3 卡内属性 |
| `.achip.dev` | 蓝 `#2434C8` + `--bg` 底 | 设备类属性 |
| `.achip.ops` | 橙 `#FF7A00` + `--orange-bg` 底 | 运营类属性 |

### 6.3 表单

```
.flabel      12.5/700 标签；必填加 <span class="req">*</span>（红）
             可选用 <span class="opt">（选填）</span>（灰）
.fsel        下拉选择：圆角 10、padding 10×11、13/600、--bg-soft 底、右侧 chevron
.finput      单行输入
.ftarea      多行输入：min-height 88、13.5/400、line-height 1.55
.fhint       11px 灰色辅助说明
.drop        下拉浮层：圆角 10、padding 5、阴影、选中项蓝底
```

- 聚焦态：`border-color:var(--blue)` + `background:#fff`
- `.field + .field{ margin-top:12px }`

### 6.4 单选组

```html
<div class="rgrp grid2">        <!-- 或 .rgrp（纵向）/ .rgrp.row（横向） -->
  <label class="radio on"><span class="dot"></span><span><b>选项</b></span></label>
</div>
```

- 选中态：蓝色描边 + 白底 + `0 0 0 3px rgba(36,52,200,.06)`；圆点变为 4.5px 蓝边

### 6.5 筛选与 Tab

| 类 | 用途 |
|---|---|
| `.tmain` / `.mt` | 主 Tab（我的工单 / 待认领），等宽，选中蓝底 + 计数胶囊 `<small>` |
| `.tchips` / `.tchip` | 次级状态 chips，横向滚动，隐藏滚动条 |
| `.tfilter` / `.fg` / `.fl` / `.opt` | 折叠筛选面板：分组卡 + 标签 + 多选胶囊（选中蓝） |
| `.tabs2` / `.tab2` | 统计页指标切换（销量 / 销售额 / 毛利） |
| `.tabs` / `.tab` | 首页横向 Tab（选中为蓝色胶囊） |
| `.sel` | 统计页筛选下拉（标签 + 下拉同一行） |
| `.searchrow` / `.search` | 搜索行：`.search` 圆角 12、`#F1F3FA` 底、14px |

**筛选面板规则**

1. 必须提供「清除过滤条件」，一键重置全部维度（含分段切换与自定义时间区间）。
2. 时间维度固定提供 **全部 / 今天 / 近 7 天 / 近 30 天 / 自定义**；选「自定义」就地展开起止时间（两个原生 `datetime-local` + `step="1"`，**精确到年月日时分秒**，纵向全宽排列），留空表示该端不限。
3. 起止时间颠倒时**自动交换**，不弹错打断用户；两端都清空则回到「全部」。
4. 自定义区必须回显「已选区间（含秒）+ 命中条数」，让用户确认筛选已生效。
5. 时间筛选的时间基准必须与列表展示的时间一致（不应使用与展示脱节的相对时间），否则会出现"选了区间却筛空"。

### 6.6 数据展示

| 类 | 规格 | 用途 |
|---|---|---|
| `.tbl` | grid `30px 1fr 62px 74px` | 排行榜（名次 / 名称 / 数量 / 金额） |
| `.tbl .rk.top` | 前三名蓝底白字 | 名次标记 |
| `.bars` / `.bar` | 轨道高 9、圆角 999、渐变 `blue → #5B6BF0` | 占比分布 |
| `.kpi`（3 列）/ `.kpi2`（2 列） | 12/400 名称 + 18/800 数值 | 概览指标 |
| `.drow` | 14/700 主 + 11.5 次 + 右侧 chevron | 明细列表行 |
| `.pcard` | 44×44 图标块 + 名称 + 说明 | 商品明细卡 |
| `.tl` | 8px 圆点 + 1.5px 竖线 | 处理记录时间线 |
| `.loadmore` | 13/600 蓝色居中 | 加载更多 |
| `.tkempty` | 12px 灰、padding 24 | 空态 |

### 6.7 反馈组件

| 类 | 用途 |
|---|---|
| `.notice`（红）/ `.notice.warn`（橙）/ `.notice.blue`（蓝） | 顶部提示条，`.notice .q` 可放引用原文 |
| `.toast` | 居中底部胶囊提示，`bottom:96px`，`.on` 显示 |
| `.sheetmask` + `.sheet` | 底部弹窗：圆角 20 顶部、`.grab` 拖拽条、`.sh` 头部、`.body` 内容 |
| `.photo` / `.photo.add` | 74×74 照片位，虚线描边为「添加」 |

---

## 7. 图标规范

- 统一 `viewBox="0 0 24 24"`，`fill="none"`，`stroke="currentColor"`
- 线宽：常规 **1.8–2**，强调/返回 **2.2**
- 端点：`stroke-linecap="round"` + `stroke-linejoin="round"`
- 颜色继承 `currentColor`，不写死色值
- 尺寸按场景：卡内 chip 11px、字段行 13–14px、按钮内 16–18px、底栏 21px、缩略图容器 22–26px

---

## 8. 交互与动效

| 场景 | 规则 |
|---|---|
| 列表 → 详情 | 整卡点击跳转 |
| 认领工单 | **无需二次确认**，点击后直接进详情（PRD 约定） |
| 记录进展 | 保存只追加记录，**不改变工单状态** |
| 提交完工 | 必填项未填 → 拦截并高亮 + Toast；不静默失败 |
| 等待反馈 | 明确提示 SLA **继续计时** |
| 恢复处理 | 选择「否」则保持等待状态 |
| 退回返工 | 保留审核意见，生成新版本（V1 / V2） |
| 弹窗 | 底部升起，遮罩点击可关闭；截图/自动化需等待动画结束 |
| 主操作 | 提交类操作需有 Loading / 禁用态，防重复提交 |

---

## 9. 文案规范

| 项 | 规则 |
|---|---|
| 语言 | 简体中文，术语统一（点位 / 设备 / 工单 / 告警 / 租户 / SLA） |
| 空值 | 统一显示 `—`（长破折号），不写「无」「N/A」 |
| 时间 | 列表 `MM/DD HH:mm`，详情 `YYYY/MM/DD HH:mm` |
| 单号 | 长 ID 截断为前 8 位 + `…`（如 `60e340a2…`），详情页展示完整 |
| 金额 | `¥` 前缀，千分位分隔 |
| 等级 | 大写 + 中文后缀：`P0 · 严重` / `P1 · 警告` / `P2 · 提示` |
| 按钮 | 动词短语：「提交完工」「认领工单」「记录进展」，不用「确定」「OK」 |

---

## 10. 代码约定

### 10.1 CSS 铁律

1. **只追加，不改动**：`vend.css` 已有规则一律不改，新需求以新类追加到文件末尾
2. **双份同步**：根目录 `vend.css` 与 `app_workorder/vend.css` 需保持一致，改一个必须同步另一个
3. **禁止内联写死颜色**：颜色一律走 CSS 变量或语义类
4. **覆盖需带作用域**：若与既有类重名（如 `.abtn`、`.alvl`），必须在父作用域内覆盖（`.acard .abtn{...}`），不得改基础类
5. **保留基础属性**：写覆盖样式时必须连同 `display:flex/grid` 等基础属性一起保留，否则布局会退化

### 10.2 文件与命名

| 项 | 规则 |
|---|---|
| 文件命名 | 小写 kebab-case：`ticket-detail.html`、`alert-detail.html` |
| 模块目录 | 同一业务模块放独立目录（如 `app_workorder/`），并复制一份 `vend.css` |
| 跨目录引用 | 子目录页面引用上级页面用 `../home.html`；上级引用子页用 `app_workorder/tickets.html` |
| 新增页面 | 必须同步更新 `nav.html`（分组 + 计数） |
| 类名语义 | 按「模块前缀 + 元素」命名（`.acard` 卡、`.atitle` 标题、`.achip` 标签） |

### 10.3 新页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1">
<title>页面名称 · VendSolution</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="vend.css">
</head>
<body>
<div class="screen">
  <div class="dtop">
    <a class="back" href="nav.html">‹ 返回</a>
    <div class="title">页面名称</div>
    <span class="right"></span>
  </div>
  <!-- 内容：区块卡 .sect / 列表卡 .acard -->
</div>
</body>
</html>
```

---

## 11. 页面清单（29 页）

| 模块 | 页面 | 文件 |
|---|---|---|
| 总览 | App 总览画廊 | `index.html` |
| | 工单总览 | `app_workorder/index.html` |
| | 页面导航 | `nav.html` |
| | **设计标准（C3）** | `style-guide.html` |
| 登录 / 账户 | 登录、我的 | `login.html`、`my.html` |
| 首页 | 首页（含告警入口） | `home.html` |
| 商品 / 设备 / 补货 | 商品列表、商品详情、设备、补货、补货完成 | `products.html`、`product-detail.html`、`machines.html`、`restock.html`、`restock-done.html` |
| 经营统计 | 经营统计、商品销量排行、点位销量排行、点位原料统计、点位商品销售统计 | `stats.html`、`rank-product.html`、`rank-site.html`、`material.html`、`site-product.html` |
| 告警 | 告警列表、告警详情、卡片设计对比 | `alerts.html`、`alert-detail.html`、`alert-detail-design.html` |
| 工单 | 我的工单 A01、待认领 A02、详情 A03、记录进展 A04、完工提交 A05、等待反馈 A06、恢复处理 A07、转派 A08、退回返工 A09 | `app_workorder/tickets.html`、`app_workorder/ticket-claim.html`、`app_workorder/ticket-detail.html`、`app_workorder/ticket-progress.html`、`app_workorder/ticket-complete.html`、`app_workorder/ticket-wait.html`、`app_workorder/ticket-resume.html`、`app_workorder/ticket-transfer.html`、`app_workorder/ticket-rework.html` |

> 导航页 `nav.html` 收录其中 28 页（不含自身）；`alert-detail-design.html` 为 C1–C4 选型对比稿，同样纳入导航便于回看。

### 例外说明

`login / my / home / products / product-detail / machines / restock / restock-done` 为 **Figma 1:1 像素复刻**页，其卡片沿用 Figma 原结构（`.row` 等），**不套用 C3**，以免破坏与设计稿的一致性。

---

## 12. 验收清单

新页面交付前逐项自检：

- [ ] 逻辑宽 393，首屏 852 内可看到主信息与主操作
- [ ] 顶部/底部固定栏已加 `env(safe-area-inset-*)`，`viewport-fit=cover` 已写
- [ ] 列表卡片使用 `.acard`，严重度 `p0/p1/p2`、状态 `s-*` 类名正确
- [ ] 空值显示 `—` 且不渲染为 chip
- [ ] 颜色全部走变量/语义类，无内联硬编码色值
- [ ] 未改动 `vend.css` 既有规则；若改了 CSS，根与 `app_workorder` 两份已同步
- [ ] 所有 `href` 指向真实存在的文件（跨目录路径已修正）
- [ ] 新页面已加入 `nav.html`，计数已更新
- [ ] 无头 Chrome 截图核对：无错位、重叠、溢出
- [ ] 主操作有校验 / Loading / 防重复提交

---

## 附：快速决策表

| 我要做… | 用什么 |
|---|---|
| 一个列表项 | `.acard` + `.ain` |
| 一个详情信息块 | `.sect` + `.hd` / `.frow` |
| 详情页状态头 | `.sect.sev.p0` + `.sin` |
| 一个表单 | `.field` + `.flabel` + `.fsel/.finput/.ftarea` |
| 一个筛选面板 | `.tfilter` + `.fg` + `.fl` + `.opt` |
| 底部主操作 | `.dobot` + `.row2` + `.abtn` |
| 一个弹窗 | `.sheetmask` + `.sheet` + `.grab` + `.sh` + `.body` |
| 一个提示 | `.notice` / `.toast` |
| 一个排行榜 | `.dcard` + `.tbl` |
| 一组指标 | `.kpi`（3 列）/ `.kpi2`（2 列） |
