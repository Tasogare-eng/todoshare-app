# 003: Todo CRUD機能

## 概要
Todoの基本的な作成・読み込み・更新・削除機能の実装

## 目的
- Todo管理のコア機能を実装
- ユーザーごとのTodo管理を実現

## タスク

### データベース設計
- [ ] Todosテーブルの作成（Supabase）
- [ ] RLS（Row Level Security）ポリシーの設定
- [ ] インデックスの設定

### バックエンド実装
- [ ] Todoモデルの作成（SQLAlchemy）
- [ ] Pydanticスキーマの作成（TodoCreate, TodoUpdate, TodoResponse）
- [ ] Todo作成API（POST /api/todos）
- [ ] Todo一覧取得API（GET /api/todos）
- [ ] Todo詳細取得API（GET /api/todos/{id}）
- [ ] Todo更新API（PUT /api/todos/{id}）
- [ ] Todo削除API（DELETE /api/todos/{id}）
- [ ] Todo完了/未完了切り替えAPI（PATCH /api/todos/{id}/toggle）
- [ ] ページネーションの実装
- [ ] ソート機能の実装

### フロントエンド実装
- [ ] Todoストア（Pinia）の作成
- [ ] Todo一覧ページコンポーネント
- [ ] Todoカードコンポーネント
- [ ] Todo作成フォームコンポーネント
- [ ] Todo編集フォームコンポーネント
- [ ] Todo詳細モーダルコンポーネント
- [ ] 削除確認ダイアログコンポーネント
- [ ] チェックボックスによる完了/未完了切り替え
- [ ] ドラッグ&ドロップによる並び替え（オプション）

### バリデーション
- [ ] タイトル必須チェック
- [ ] タイトル最大文字数（100文字）チェック
- [ ] 説明最大文字数（500文字）チェック
- [ ] 権限チェック（自分のTodoのみ編集・削除可能）

### UI/UX
- [ ] ローディングステートの表示
- [ ] エラーハンドリング
- [ ] 成功メッセージの表示（トースト通知）
- [ ] 空ステートの表示（Todoが0件の場合）
- [ ] レスポンシブデザイン

### テスト
- [ ] Todo CRUD APIのユニットテスト
- [ ] Todoストアのテスト
- [ ] コンポーネントのテスト
- [ ] E2Eテスト（Todoの作成から削除まで）

## 完了条件
- [ ] Todoの作成・一覧表示・編集・削除ができる
- [ ] ログインユーザーごとにTodoが分離されている
- [ ] チェックボックスで完了/未完了が切り替えられる
- [ ] 他のユーザーのTodoにはアクセスできない
- [ ] ページネーションが動作する

## 技術詳細
- ORM: SQLAlchemy 2.0
- バリデーション: Pydantic v2
- ステート管理: Pinia
- API通信: Axios

## 推定工数
3日

## 依存関係
- 001_project_setup.mdが完了していること
- 002_authentication.mdが完了していること

## 備考
- リアルタイム更新はMVP後に検討
- オフライン対応はMVP後に検討