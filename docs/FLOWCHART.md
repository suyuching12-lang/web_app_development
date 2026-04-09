# 流程圖文件：食譜收藏夾

本文件描述了系統中的主要使用者操作路徑以及底層資料流的序列圖。

## 1. 使用者流程圖 (User Flow)

這個流程圖展示出家庭主婦從開啟網頁開始，可能會採取的各種操作路線。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
    
    Home --> Action{要執行什麼操作？}
    
    Action -->|尋找食譜| Search[在搜尋列輸入關鍵字]
    Search --> Home
    
    Action -->|瀏覽現有食譜| ClickRecipe[點擊特定食譜]
    ClickRecipe --> Detail[食譜詳細內容頁]
    
    Action -->|想記錄新菜色| ClickAdd[點擊「新增食譜」按鈕]
    ClickAdd --> AddForm[新增食譜表單頁]
    AddForm -->|填寫並送出| SubmitAdd(系統儲存資料)
    SubmitAdd --> Home
    
    Detail --> DetailAction{對這篇食譜的操作？}
    
    DetailAction -->|修改材料或步驟| Edit[點擊「編輯」按鈕]
    Edit --> EditForm[編輯食譜表單頁]
    EditForm -->|修改並送出| SubmitEdit(系統更新資料)
    SubmitEdit --> Detail
    
    DetailAction -->|不再需要| Delete[點擊「刪除」按鈕]
    Delete --> ConfirmDelete{確認刪除？}
    ConfirmDelete -->|是| DoDelete(系統刪除資料)
    DoDelete --> Home
    ConfirmDelete -->|否| Detail
```

## 2. 系統序列圖 (Sequence Diagram)

以下序列圖具體描述了使用者在「新增食譜」時，前端（瀏覽器）到後端（Flask、Model、SQLite）如何串聯處理並儲存資料的完整流程。

```mermaid
sequenceDiagram
    actor User as 家庭主婦
    participant Browser as 瀏覽器 (前端)
    participant Route as Flask 路由 (Controller)
    participant Model as Recipe 模型 (Model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 在首頁點擊「新增食譜」
    Browser->>Route: GET /recipe/add
    Route-->>Browser: 回傳 HTML 表單 (form.html)
    
    User->>Browser: 填寫料理名稱、材料、步驟後點擊「送出」
    Browser->>Route: POST /recipe/add (帶有表單資料)
    
    Route->>Route: 驗證資料格式 (如：名稱不可為空)
    Route->>Model: 呼叫建立食譜方法 (create_recipe)
    
    Model->>DB: 執行 SQL (INSERT INTO recipes ...)
    DB-->>Model: 回傳成功狀態與新產生的 ID
    
    Model-->>Route: 回傳新建立的 Recipe 物件或 ID
    
    Route-->>Browser: HTTP 302 重導向回首頁 (或食譜詳情頁)
    Browser->>Route: GET / (重新載入列表)
    Route-->>Browser: 回傳更新後的首頁 HTML
    Browser-->>User: 畫面顯示剛新增成功的食譜
```

## 3. 功能清單對照表

本表列出了所有主要操作功能以及對應的系統路由與 HTTP 動詞。

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| **瀏覽首頁 (列表)** | `/` | `GET` | 顯示所有食譜，支援關鍵字搜尋 (例如 `/?q=牛肉`) |
| **查看食譜詳情** | `/recipe/<id>` | `GET` | 顯示該食譜的詳細材料與完整步驟 |
| **顯示新增表單** | `/recipe/add` | `GET` | 顯示讓使用者填寫新食譜資訊的表單畫面 |
| **提交新增資料** | `/recipe/add` | `POST` | 接收表單內容，寫入資料庫並返回首頁 |
| **顯示編輯表單** | `/recipe/<id>/edit` | `GET` | 帶入既有資料，顯示編輯表單畫面 |
| **提交編輯資料** | `/recipe/<id>/edit` | `POST` | 接收修改後的內容，更新資料庫並返回詳情頁 |
| **刪除食譜** | `/recipe/<id>/delete` | `POST` | 接收刪除請求，移除資料並返回首頁 |
