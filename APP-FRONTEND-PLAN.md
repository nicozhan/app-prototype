# APP 端前端改造方案（jpgk-platform / mobile）

> 适用约束：只改 APP 端前端 UI，后端保持不动；提交只涉及 `mobile/` 前端内容。

## 一、结论（先给定位）

APP 端前端 = 仓库里的 **`mobile/`** 目录（工程名 `jpgk-mobile`，Uni-app 3 + Vue 3 + TypeScript + Pinia + Vite + Sass）。它与后端、Web 后台、小程序、设备终端**完全隔离**，你只需在 `mobile/src` 的 UI 层工作，其余一律不碰。

```
jpgk-platform/
├── backend/            ← 后端（微服务 ai / gateway / iothub / platform）★ 绝不改
├── frontend/           ← Web 管理后台前端（1299 文件，Vue+Vite）      ★ 不碰（不是 App）
├── mini/               ← C 端小程序（Taro + Vue3）                    ★ 不碰（另一产品）
├── device-terminal/    ← 设备终端                                     ★ 不碰
└── mobile/             ← ★★★ APP 端前端（你的工作区）★★★
    └── src/
        ├── main.ts / App.vue / pages.json / manifest.json / uni.scss   ← 入口与配置
        ├── pages/            ← 29 个 .vue（10 模块）★ UI 层
        ├── components/vs/    ← 12 个自研组件（Vs* 组件库）★ UI 层
        ├── styles/ static/ locale(s)/ custom-tab-bar/   ★ UI 层
        └── api/ stores/ composables/ utils/ analytics/ constants/ types/  ← 逻辑层（谨慎）
```

## 二、前后端边界（三层划分）

### 第 1 层：纯前端 UI（你负责改，改动安全）

| 目录 | 内容 | 规模 |
|---|---|---|
| `mobile/src/pages/` | 页面（10 模块 29 个 .vue） | 29 |
| `mobile/src/components/vs/` | 自研组件库（VsStatCard / VsReplenishConfirmSheet / VsSearchBar / VsStatusTag / VsTaskCard …） | 12 |
| `mobile/src/styles/` | 全局样式（skeleton.scss） | 1 |
| `mobile/src/static/` | 图片等静态资源 | 166 |
| `mobile/src/locale/` + `locales/` | 多语言（zh-CN 简 / zh-TW 繁 / en / vi-VN 越） | 10 |
| `mobile/src/custom-tab-bar/` | 自定义 tabbar | — |
| `mobile/src/main.ts / App.vue / pages.json / manifest.json / uni.scss` | 入口、路由注册、全局样式变量 | — |

### 第 2 层：前端仓库内的数据/逻辑层（尽量不改；若必须改需谨慎评估影响）

| 目录 | 内容 | 规模 |
|---|---|---|
| `mobile/src/api/` | API 调用（含 `mock/`，`VITE_USE_MOCK_API` 可脱离后端本地开发） | 27 |
| `mobile/src/stores/` | Pinia 状态（auth / replenishmentSession / tabBarLocale） | 3 |
| `mobile/src/composables/` | 组合式函数 | 1 |
| `mobile/src/utils/` | 工具函数 | 31 |
| `mobile/src/analytics/` | 埋点（Mixpanel） | 3 |
| `mobile/src/constants/`、`types/` | 常量、TS 类型 | — |

> 说明：这层虽在 `mobile/` 内，但承载「与后端交互 / 业务状态 / 埋点」，属于逻辑而非视觉。UI 重构原则上不动它；若新 UI 需要新字段/新接口，优先在 UI 层适配现有数据结构，确需改类型/接口时单独说明、单独评估。

### 第 3 层：绝不改

- `backend/`（ai / gateway / iothub / platform）—— 后端本体
- `frontend/` —— Web 后台前端
- `mini/` —— C 端小程序
- `device-terminal/` —— 设备终端

## 三、你的核心工作区（对应近期 UI 工作）

`pages.json` 共注册 26 个页面，底部 tab 3 个：`operations/index`（运营）、`replenishment/list`（补货）、`profile/index`（我的）。

与你近期「补货 / 机器详情 / 开门柜」工作直接对应的文件：

| 需求 | 文件 |
|---|---|
| 机器详情（Machine Details） | `mobile/src/pages/devices/detail.vue` |
| 设备参数 | `mobile/src/pages/devices/parameters.vue`、`DeviceParameterSettingTable.vue` |
| 补货清单（Restocking list） | `mobile/src/pages/replenishment/list.vue` |
| 补货详情 | `mobile/src/pages/replenishment/detail.vue` |
| 咖啡机料道补货 | `mobile/src/pages/replenishment/drink.vue`、`DrinkRestockLines.vue` |
| 开门柜补货执行 | `mobile/src/pages/replenishment/execute.vue` |
| 补货拍照 / 完成 | `photo.vue`、`complete.vue` |
| 补货变更弹窗 | `ReplenishmentChangeDialog.vue` |
| 补货确认 Bottom Sheet | `mobile/src/components/vs/VsReplenishConfirmSheet.vue` |
| 统计卡 / 状态标签 | `VsStatCard.vue`、`VsStatusTag.vue`、`VsStatusBar.vue` |

## 四、本地开发环境

- 依赖未装：需先 `cd mobile && npm install`。
- 预览（推荐，浏览器直接看，支持 mock 数据）：
  - `npm run dev:h5` —— H5 预览
  - `.env` 里 `VITE_USE_MOCK_API` 控制是否走 mock（可脱离后端）
- 真机/App 构建（需 HBuilderX 或对应环境）：
  - `npm run dev:app-android` / `dev:app-ios`
  - `npm run build:h5`（`build:test:h5` / `build:prod:h5`）
- 校验：
  - `npm run type-check` —— TS 类型检查（改 UI 后必跑）
  - `npm run test:unit` —— 单测（大量 `*.test.ts/mjs`，改逻辑才需关注）

## 五、分支策略（待你确认）

仓库默认分支 `master`，但**双门 / 开门柜功能不在 master 上**，而在分支 `20261113_doubleDoor`（`7f87eb14d`「机器模版，机器 开门柜 添加货柜切换」，相对 master 22 文件 +148/−874）。

建议流程：
1. 确认基线分支（`master` 还是 `20261113_doubleDoor`，或让我对比两者 mobile 差异后再定）。
2. 从基线拉一条独立 UI 分支，例如 `feature/ui-restock-redesign`。
3. 所有 UI 改动只落在该分支，只提交 `mobile/` 前端。

## 六、工作流（改 → 验证 → 提交）

1. **改**：只编辑第 1 层 UI 目录（pages / components / styles / static / locale）。
2. **验证**：`npm run type-check` + `npm run dev:h5` 目测（390×844 视口优先，对应手机）。
3. **提交**：commit 只包含 `mobile/` 下的前端文件，`message` 标注 UI 范围，例：
   `feat(mobile): 开门柜补货列表紧凑化（仅 UI）`
4. **推送**：推送到你的 UI 分支；合并走 MR/PR，不直接改 `master` / `backend`。

## 七、风险与注意事项

1. **生产证书/密钥已入库**（`mobile/572e…keystore`、`mobile/证书.p12`、`mobile/wangkang_prod.mobileprovision`）—— 安全债，建议后续从 git 历史清除并迁移到 CI 密钥管理，与本次 UI 工作无关，但需知悉。
2. **四语言同步**：UI 文案改动需同步 `zh-CN / zh-TW / en / vi-VN`（当前无泰语，与早前讨论的「泰语」不一致，需确认目标语种集合）。
3. **组件/逻辑耦合**：部分页面内嵌了 `.test.ts` 与业务 TS（如 `executeDraft.ts`、`liveChanges.ts`、`taskDetailView.ts`），改 UI 时注意别破坏这些配套逻辑，否则单测会红。
4. **`.env` 含 `VITE_MIXPANEL_TOKEN` / `VITE_API_BASE_URL`** —— 均为前端构建变量，非仓库外泄重点，但仍不建议在 commit 里改动。
5. **静态资源多**（166 个）—— UI 换图/换图标直接替换 `static/` 下对应文件即可。

## 八、下一步（待你拍板的两件事）

1. **基线分支**：`master` 还是 `20261113_doubleDoor`？
2. **目标语种**：维持现有「简/繁/英/越」四语，还是按早前说的改为「英/简/越/泰」？
