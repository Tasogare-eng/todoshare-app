# 004: カテゴリ管理機能

## 概要
Todoを整理・分類するためのカテゴリ機能の実装

## 目的
- Todoのカテゴリ分けを実現
- 色分けによる視覚的な区別
- 柔軟なカテゴリ管理

## タスク

### データベース設計
- [ ] Categoriesテーブルの作成
- [ ] TodoCategoriesテーブルの作成（多対多関係）
- [ ] RLSポリシーの設定
- [ ] デフォルトカテゴリのシードデータ作成

### バックエンド実装
- [ ] Categoryモデルの作成（SQLAlchemy）
- [ ] TodoCategoryリレーションモデルの作成
- [ ] Pydanticスキーマの作成（CategoryCreate, CategoryUpdate, CategoryResponse）
- [ ] カテゴリ作成API（POST /api/categories）
- [ ] カテゴリ一覧取得API（GET /api/categories）
- [ ] カテゴリ更新API（PUT /api/categories/{id}）
- [ ] カテゴリ削除API（DELETE /api/categories/{id}）
- [ ] Todoにカテゴリを追加API（POST /api/todos/{id}/categories）
- [ ] Todoからカテゴリを削除API（DELETE /api/todos/{id}/categories/{category_id}）
- [ ] カテゴリ別Todo一覧API（GET /api/categories/{id}/todos）

### フロントエンド実装
- [ ] カテゴリストア（Pinia）の作成
- [ ] カテゴリ管理ページコンポーネント
- [ ] カテゴリ作成/編集モーダル
- [ ] カテゴリバッジコンポーネント
- [ ] カラーピッカーコンポーネント
- [ ] Todo作成/編集フォームへのカテゴリ選択追加
- [ ] カテゴリフィルター機能
- [ ] カテゴリ別色分け表示

### UI/UX
- [ ] カテゴリチップのデザイン
- [ ] カラーパレットの定義（12色程度）
- [ ] ドラッグ&ドロップでカテゴリ追加（オプション）
- [ ] カテゴリアイコンの追加（オプション）

### バリデーション
- [ ] カテゴリ名必須チェック
- [ ] カテゴリ名最大文字数（30文字）チェック
- [ ] カテゴリ名重複チェック（ユーザー内）
- [ ] カラーコードの形式チェック（#RRGGBB）
- [ ] カテゴリ削除時の関連Todo確認

### テスト
- [ ] カテゴリCRUD APIテスト
- [ ] Todo-カテゴリ関連APIテスト
- [ ] カテゴリストアテスト
- [ ] コンポーネントテスト

## 完了条件
- [ ] カテゴリの作成・編集・削除ができる
- [ ] Todoに複数のカテゴリを設定できる
- [ ] カテゴリごとに色分け表示される
- [ ] カテゴリでTodoをフィルターできる
- [ ] デフォルトカテゴリが初期表示される

## 技術詳細
- カラーパレット: Material Design Colors
- 多対多関係: SQLAlchemy relationship
- UIコンポーネント: Vuetify Chip/Badge

## 推定工数
2日

## 依存関係
- 003_todo_crud.mdが完了していること

## 備考
- デフォルトカテゴリ: 「仕事」「プライベート」「買い物」「その他」
- カテゴリのアイコン機能はMVP後に検討