from flask import Blueprint, render_template, request, redirect, url_for, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    """
    首頁: 顯示食譜列表。
    可接收 `?query=` 來做關鍵字搜尋。
    邏輯：調用 RecipeModel.get_all 或是 RecipeModel.search_by_keyword。
    輸出：渲染 index.html，傳遞 recipes 給前端
    """
    pass

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def detail(id):
    """
    詳情頁: 顯示特定食譜內容。
    邏輯：調用 RecipeModel.get_by_id(id) 並檢查是否存在。
    輸出：渲染 detail.html，傳遞 recipe 給前端
    """
    pass

@recipe_bp.route('/recipe/add', methods=['GET'])
def add_recipe_page():
    """
    新增食譜頁面: 顯示新增用表單。
    輸出：渲染 form.html
    """
    pass

@recipe_bp.route('/recipe/add', methods=['POST'])
def add_recipe_action():
    """
    新增食譜動作: 接收表單並儲存。
    邏輯：驗證後調用 RecipeModel.create，成功後重導向到首頁。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit_recipe_page(id):
    """
    編輯食譜頁面: 載入現有資料並顯示編輯表單。
    邏輯：調用 RecipeModel.get_by_id(id) 取得資料。
    輸出：渲染 form.html，傳遞 recipe 變數作為預填資料。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['POST'])
def edit_recipe_action(id):
    """
    編輯食譜動作: 接收修改內容並更新到資料庫。
    邏輯：調用 RecipeModel.update()，成功後重導向至與更新的 detail 頁面。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe_action(id):
    """
    刪除食譜動作: 移除特定紀錄。
    邏輯：調用 RecipeModel.delete(id)，接著重導向到首頁。
    """
    pass
