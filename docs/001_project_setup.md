# 001: プロジェクトセットアップ

## 概要
TodoShareプロジェクトの初期環境構築とプロジェクト基盤の設定

## 目的
- 開発環境の構築
- プロジェクト構造の確立
- 基本的な設定ファイルの作成

## タスク

### フロントエンド環境構築
- [x] Vue 3プロジェクトの作成（Vite使用）
- [x] TypeScriptの設定
- [x] Piniaのインストールと設定
- [x] Vue Routerの設定
- [ ] UIライブラリ（Vuetify 3 or PrimeVue）の選定とインストール
- [x] ESLintとPrettierの設定
- [x] 環境変数の設定（.env.development, .env.production）

### バックエンド環境構築
- [x] FastAPIプロジェクトの作成
- [x] プロジェクト構造の設定（app/, models/, routes/, services/）
- [x] 仮想環境の作成
- [x] requirements.txtの作成
- [x] 環境変数の設定（.env）
- [x] CORSの設定
- [x] ロギング設定

### Supabase設定
- [ ] Supabaseプロジェクトの作成
- [ ] データベーススキーマの設計
- [ ] 環境変数へのSupabase接続情報の追加
- [ ] Supabase CLIのインストール

### 開発環境
- [x] Dockerfileの作成（フロントエンド・バックエンド）
- [x] docker-compose.ymlの作成
- [x] .gitignoreの設定
- [x] README.mdの作成

### CI/CD基盤
- [ ] GitHub リポジトリの作成
- [ ] GitHub Actionsの基本設定
- [ ] ブランチ保護ルールの設定

## 完了条件
- [x] フロントエンドが`npm run dev`で起動する
- [x] バックエンドが`uvicorn main:app --reload`で起動する
- [x] フロントエンドからバックエンドAPIにアクセスできる
- [ ] Supabaseとの接続が確認できる
- [x] Dockerコンテナで両サービスが起動する

## 技術詳細
- Node.js: v18以上
- Python: 3.10以上
- PostgreSQL: 14以上（Supabase）

## 推定工数
2日

## 依存関係
なし（最初のタスク）

## 備考
- Supabaseの無料枠制限に注意
- 開発環境と本番環境の設定を明確に分離する