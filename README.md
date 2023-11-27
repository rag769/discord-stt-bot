# discord-stt-bot
 A speech-to-text bot  for discord.

## 概要
Discord の Voice チャンネルの発言を文字起こしするBOT

## 特徴
* 音声認識は [wit.ai](https://wit.ai/)
* 某ROの某クホNPC風メッセージ

## 必要なもの
* Python 3.8 以上
  * 必要パッケージは requirements.txt
* [wit.ai](https://wit.ai/) アカウント＋トークン

## 使い方 (BOTプログラム)
1. config.py の変更
   * DISCORD_TOKEN
   * WIT_TOKEN
2. 必要ライブラリを取得  
   ```pip install -r requirements.txt```
3. プログラムを起動  
   ```python bot.py```


## 使い方 (Discord)
コマンドプレフィックスは設定(config.py)で変更可能。  
ここでは "```?```" が設定されているものとします。

### - 文字起こしの開始

文字起こし対象の Voice チャンネルに参加し、文字起こし先の Text チャンネルで下記コマンドを実行します。  
(既に別のチャンネルで文字起こししている場合は受付けません)

```
?kaku
```

### - 文字起こしの終了

下記コマンドを実行します。

```
?kakanai
```

__どこからでもだれからでも受け付けます。__


## 免責および注意事
* 本BOTの使用により損害が発生したとしても一切の責任を負いません。
* 本BOTの仕様は予告なしに変更する事があります。
