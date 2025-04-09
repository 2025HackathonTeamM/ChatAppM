###ChatApp

This is a team chat application built with Flask and MySQL (via Docker).

###クローン準備
以下のコマンドでリポジトリをクローンしてください（SSH推奨）：

```bash
git clone git@github.com:2025HackathonTeamM/ChatAppM.git
cd ChatAppM

###.envファイルの作成：.envファイルはgitでダウンロードしたものをそのまま使えない性質のものなので、各自.env.exampleをローカルで.envに変更してください
cp .env.example .env

###開発環境の開発
#Python 3.11以上推奨
#必要なパッケージをインストール
python -m venv venv         # 仮想環境（あれば推奨）
source venv/bin/activate    # 仮想環境に入る（Mac/Linux）
pip install -r requirements.txt 　　#このコマンドでFlaskやpython-dotenvなど必要なパッケージがダウンロードされます！
