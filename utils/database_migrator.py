"""
数据库迁移工具 - 用于升级数据库表结构
"""
import sqlite3
from app_config import DB_PATH


class DatabaseMigrator:
    """数据库迁移类"""

    def __init__(self):
        self.db_path = DB_PATH

    def migrate(self):
        """执行数据库迁移"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 检查 recipes 表的字段
            cursor.execute("PRAGMA table_info(recipes)")
            columns = [col[1] for col in cursor.fetchall()]

            print("📋 当前 recipes 表字段:", columns)

            needs_migration = False

            # 检查并添加缺失的字段
            missing_columns = []

            # 所有可能的字段
            all_columns = {
                'created_at': "ALTER TABLE recipes ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                'updated_at': "ALTER TABLE recipes ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                'image_path': "ALTER TABLE recipes ADD COLUMN image_path TEXT",
                'rating': "ALTER TABLE recipes ADD COLUMN rating REAL DEFAULT 0",
                'view_count': "ALTER TABLE recipes ADD COLUMN view_count INTEGER DEFAULT 0"
            }

            for col_name, sql in all_columns.items():
                if col_name not in columns:
                    missing_columns.append(col_name)
                    needs_migration = True
                    try:
                        cursor.execute(sql)
                        print(f"✅ 已添加 {col_name} 字段")
                    except sqlite3.OperationalError as e:
                        print(f"⚠️  添加 {col_name} 字段失败：{e}")

            if needs_migration:
                conn.commit()
                print("✅ 数据库升级完成！")
            else:
                print("✅ 数据库表结构已是最新版本")

            conn.close()
            return True

        except sqlite3.Error as e:
            print(f"❌ 数据库迁移失败：{e}")
            import traceback
            traceback.print_exc()
            return False
        except Exception as e:
            print(f"❌ 未知错误：{e}")
            import traceback
            traceback.print_exc()
            return False


    def check_table_structure(self):
        """检查表结构并打印信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            print("\n=== recipes 表结构 ===")
            cursor.execute("PRAGMA table_info(recipes)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]}: {col[2]} (默认值：{col[4]})")

            print("\n=== categories 表结构 ===")
            cursor.execute("PRAGMA table_info(categories)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]}: {col[2]} (默认值：{col[4]})")

            conn.close()
        except Exception as e:
            print(f"检查失败：{e}")


# 使用示例
if __name__ == "__main__":
    migrator = DatabaseMigrator()
    migrator.check_table_structure()
    print("\n")
    migrator.migrate()
    migrator.check_table_structure()
