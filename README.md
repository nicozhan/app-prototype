# VendSolution · App Prototype

VendSolution（AIoT + SaaS 无人零售）移动端 App 的 HTML 原语原型，共 **29 个页面**，统一 393×852（iPhone 15）画布与设计令牌，可直接在浏览器查看与点击跳转。

> 纯静态 HTML/CSS/JS，无构建步骤。打开 `nav.html` 即可浏览全部页面。

---

## 快速开始

```bash
open nav.html          # 页面导航（推荐入口）
open index.html        # Figma 1:1 复刻总览
open style-guide.html  # 设计标准 C3 卡片规范
```

---

## 目录结构

```
├── nav.html                  # 页面导航（全部页面入口）
├── index.html                # 1:1 复刻总览（iframe 画廊）
├── style-guide.html          # 设计标准 · C3 卡片
├── DESIGN-SPEC.md            # 设计规范文档（12 章）
├── vend.css                  # 共享设计系统（令牌 + 组件）
│
├── login.html  my.html  home.html
├── products.html  product-detail.html  machines.html
├── restock.html  restock-done.html
├── stats.html  rank-product.html  rank-site.html
├── material.html  site-product.html
├── alerts.html  alert-detail.html  alert-detail-design.html
│
└── app_workorder/            # 工单模块 A01–A09
    ├── vend.css              # 该模块的样式副本（需与根 vend.css 同步）
    ├── index.html
    └── tickets / ticket-claim / ticket-detail / ticket-progress
        ticket-complete / ticket-wait / ticket-resume / ticket-transfer / ticket-rework
```

---

## 页面清单

| 模块 | 页面 |
|---|---|
| 登录 / 账户 | 登录、我的 |
| 首页 | 欢迎页（含告警、工单入口） |
| 商品 / 设备 / 补货 | 商品列表、商品详情、设备、补货、补货完成 |
| 经营统计 | 统计主页、商品销量排行、点位销量排行、点位原料统计、点位商品销售统计 |
| 告警 | 告警列表（分段 + 4 维筛选 + 秒级自定义时段）、告警详情、卡片选型对比稿 |
| 工单 | 我的工单 A01、待认领 A02、详情 A03、记录进展 A04、完工提交 A05、等待反馈 A06、恢复处理 A07、转派 A08、退回返工 A09 |

---

## 设计标准 · C3

所有**自主设计**的列表卡片统一使用 `.acard`：

- **2px 整圈描边** + **同色扩散光晕**，严重度逐档递减：`p0` 红 → `p1` 橙 → `p2` 浅蓝灰
- **实心等级徽章**（`.alvl`）+ **软底状态胶囊**（`.ast2.s-*`）
- 属性 chips（`.achip`）+ 等宽时间（`.atime`）+ **实心操作按钮**（`.abtn`）
- 详情页状态头用 `.sect.sev.p0 / p1 / p2`

完整规范见 [`DESIGN-SPEC.md`](DESIGN-SPEC.md) 第 5 章，可视化版本见 [`style-guide.html`](style-guide.html)。

**例外**：`login / my / home / products / product-detail / machines / restock / restock-done` 为 Figma 1:1 像素复刻页，不套用 C3，以保持与设计稿一致。

---

## 开发约定

1. **CSS 只追加**：往 `vend.css` 新增类，不改既有规则，避免牵连其他模块。
2. **双份同步**：`app_workorder/` 有独立 `vend.css` 副本，改组件需两处同步。
3. **设计令牌**：`--blue #2434C8` / `--orange #FF7A00` / `--ink #0B102F` / `--gray #697095` / `--red #E5484D`。
4. **安全区**：`viewport-fit=cover` + `env(safe-area-inset-*)` + `min-height:100dvh`。
5. **新页面**：按 `DESIGN-SPEC.md` 第 10.3 节骨架模板创建，并加入 `nav.html`。
