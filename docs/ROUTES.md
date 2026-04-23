# 路由與頁面設計文件：食譜收藏夾

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 (食譜列表) | GET | `/` | `templates/index.html` | 顯示所有食譜，處理搜尋 `?query=` 的呈現 |
| 檢視食譜詳情 | GET | `/recipe/<int:id>` | `templates/detail.html` | 顯示單筆食譜詳細材料與步驟 |
| 新增食譜頁面 | GET | `/recipe/add` | `templates/form.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipe/add` | (無) | 接收表單資料，寫入資料庫後重導向至首頁 |
| 編輯食譜頁面 | GET | `/recipe/<int:id>/edit` | `templates/form.html` | 取出原始資料預填表單以供編輯 |
| 更新食譜 | POST | `/recipe/<int:id>/edit` | (無) | 接收表單變更，更新資料庫後重導向至詳情頁 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete` | (無) | 刪除資料庫紀錄，完成後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (`GET /`)
- **輸入**：URL Query String `?query=` (可選)。
- **處理邏輯**：如果沒有 `query`，呼叫 `RecipeModel.get_all()`；若有 `query`，則呼叫 `RecipeModel.search_by_keyword(query)`。
- **輸出**：渲染 `index.html`，傳遞 `recipes` 變數與搜尋關鍵字 `query`。

### 新增食譜頁面 (`GET /recipe/add`)
- **處理邏輯**：靜態頁面渲染與傳遞表單標題以供 UI 重用。
- **輸出**：渲染 `form.html`。

### 建立食譜 (`POST /recipe/add`)
- **輸入**：表單欄位 `title`、`ingredients`、`steps` 等 (Form Data)。
- **處理邏輯**：驗證必填欄位。成功則呼叫 `RecipeModel.create`。
- **輸出**：`redirect('/')` 重導向至首頁。若驗證失敗可以 `flash` 錯誤訊息並重新渲染 `form.html`。

### 檢視食譜詳情 (`GET /recipe/<id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：從資料庫透過 `RecipeModel.get_by_id(id)` 撈取食譜。若不到資料則拋出 `404 Not Found` 例外。
- **輸出**：渲染 `detail.html` 並傳遞 `recipe` 物件。

### 編輯食譜頁面 (`GET /recipe/<id>/edit`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：透過 `RecipeModel.get_by_id(id)` 取出原資料。
- **輸出**：渲染共用表單 `form.html` 並傳遞 `recipe` 以利預填。

### 更新食譜 (`POST /recipe/<id>/edit`)
- **輸入**：URL 參數 `id`，以及表單欄位。
- **處理邏輯**：驗證資料後呼叫 `RecipeModel.update`。
- **輸出**：`redirect(url_for('detail', id=id))`。

### 刪除食譜 (`POST /recipe/<id>/delete`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `RecipeModel.delete(id)` 從資料庫刪除紀錄。
- **輸出**：`redirect('/')`。

## 3. Jinja2 模板清單

所有的視圖需放在 `app/templates/` 內，主要規劃如下：

1. `base.html`：**全域共用主板**
   包含共用的 Header (導覽列與搜尋框)、Footer、以及 CSS 與 JavaScript 的預先載入，定義 `{% block content %}` 供子模板填入。

2. `index.html`：**首頁模版**，繼承自 `base.html`
   負責負責以卡片清單的形式呈現資料。

3. `detail.html`：**詳情頁模版**，繼承自 `base.html`
   負責顯示豐富的食譜細節與排版，包含返回與操作（編輯/刪除）按鈕。

4. `form.html`：**共用表單模版**，繼承自 `base.html`
   採用同一個表單來處裡「新增」或「編輯」，可透過傳入的 `recipe` 變數來判斷是編輯模式還是新增模式。
