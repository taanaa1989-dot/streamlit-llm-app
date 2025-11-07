# Streamlit Community Cloud デプロイ手順

## 1. リポジトリの準備
- GitHubにこのプロジェクトをプッシュしてください
- `.env`ファイルは`.gitignore`に含まれているため、GitHubにはアップロードされません

## 2. Streamlit Community Cloudでのデプロイ
1. https://share.streamlit.io/ にアクセス
2. GitHubアカウントでサインイン
3. "New app" をクリック
4. リポジトリを選択
5. ブランチとファイルパス（app.py）を指定

## 3. シークレットの設定
デプロイ後、以下の手順でAPIキーを設定してください：

1. アプリの管理画面で "Settings" をクリック
2. "Secrets" セクションを選択
3. 以下の形式でシークレットを追加：

```toml
[secrets]
OPENAI_API_KEY = "your_actual_openai_api_key_here"
```

## 4. Python バージョン
- `.python-version` ファイルでPython 3.11を指定済み
- Streamlit Community Cloudで自動的に認識されます

## 5. 依存関係
- `requirements.txt` にすべての必要なパッケージを記載済み
- デプロイ時に自動的にインストールされます

## トラブルシューティング
- デプロイエラーが発生した場合は、ログを確認してください
- パッケージのバージョン競合が発生した場合は、requirements.txtを調整してください