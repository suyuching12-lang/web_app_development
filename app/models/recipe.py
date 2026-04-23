import sqlite3
from typing import Dict, List, Optional

# 將這段抽出至 app/__init__.py 或是 db.py 時，此處可以換成 import 以取得 connection
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("instance/database.db")
    conn.row_factory = sqlite3.Row
    return conn

class RecipeModel:
    @staticmethod
    def create(title: str, ingredients: str, steps: str, image_url: str = None, category: str = None, is_favorite: int = 0) -> int:
        """建立一筆新的食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, ingredients, steps, image_url, category, is_favorite)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, ingredients, steps, image_url, category, is_favorite))
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all() -> List[sqlite3.Row]:
        """取得所有食譜 (依建立時間由新到舊排序)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    @staticmethod
    def search_by_keyword(query: str) -> List[sqlite3.Row]:
        """透過關鍵字搜尋食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        search_query = f"%{query}%"
        cursor.execute('''
            SELECT * FROM recipes 
            WHERE title LIKE ? OR ingredients LIKE ? 
            ORDER BY created_at DESC
        ''', (search_query, search_query))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(recipe_id: int) -> Optional[sqlite3.Row]:
        """取得單一食譜的詳細資訊"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def update(recipe_id: int, title: str, ingredients: str, steps: str, image_url: str = None, category: str = None, is_favorite: int = 0) -> bool:
        """更新食譜資訊"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE recipes
            SET title = ?, ingredients = ?, steps = ?, image_url = ?, category = ?, is_favorite = ?
            WHERE id = ?
        ''', (title, ingredients, steps, image_url, category, is_favorite, recipe_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows > 0

    @staticmethod
    def delete(recipe_id: int) -> bool:
        """刪除食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows > 0
