###ChatApp

This is a team chat application built with Flask and MySQL (via Docker).

###クローン準備
以下のコマンドでリポジトリをクローンしてください（SSH推奨）：

```bash
git clone git@github.com:2025HackathonTeamM/ChatAppM.git
cd ChatAppM

###.envファイルの作成：.envファイルはgitでダウンロードしたものをそのまま使えない性質のものなので、各自.env.exampleをローカルで.envに変更してください
cp .env.example .env

##Dockerを使ったアプリの起動
このアプリはDockerを用いて構築・起動します。
docker compose up --build
Flaskアプリ：http://localhost:55000 でアクセスできます）
このプロジェクトは Docker を使って構築されており、依存パッケージ（Flask など）は
Dockerfile 内で自動的にインストールされます。

そのため、開発者が手動で `pip install` を実行する必要はありません
#このコマンドでFlaskやpython-dotenvなど必要なパッケージがダウンロードされます！
