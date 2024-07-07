# Jetson NanoでRoomba 980を操作しよう！初心者のための完全ガイド

## はじめに

こんにちは！この記事では、Jetson NanoというミニコンピューターをRoomba 980に接続し、操作する方法を詳しくご紹介します。プログラミングで掃除機ロボットを動かすなんて、ワクワクしますよね。難しそうに思えるかもしれませんが、一緒に頑張れば誰でもできるようになります！

## 必要な機材

まずは、必要な機材を確認しましょう：

1. Jetson Nano
2. Roomba 980
3. USB-MicroUSBケーブル
4. Jetson Nano用電源ケーブル
5. モニター、キーボード、マウス（初期設定用）
6. ネットワーク環境（有線LANまたはWi-Fi）

## Jetson Nanoの準備

Jetson Nanoは小型のコンピューターです。使用前にOSをインストールする必要があります：

1. NVIDIAの公式サイトからJetson Nano Developer Kit SDカードイメージをダウンロード
2. イメージをSDカードに書き込む（Etcher等のツールを使用）
3. SDカードをJetson Nanoに挿入し、電源を入れる
4. 画面の指示に従ってセットアップを完了
5. ネットワークに接続し、IPアドレスをメモしておく

## SSH接続の設定

Jetson Nanoをヘッドレス（モニターなし）で操作するために、SSH接続を設定します。この過程には、SSH鍵の作成、Jetson Nanoの設定、制御用PCの設定が含まれます。

### SSH鍵の作成

1. 制御用PCで端末（ターミナル）を開きます。

2. 以下のコマンドを実行してSSH鍵を生成します：

   ```python
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_for_jet
   ```

3. パスフレーズの入力を求められますが、セキュリティを重視する場合を除き、空白のままEnterを押して進めます。

4. これにより、`~/.ssh/id_rsa_for_jet`（秘密鍵）と`~/.ssh/id_rsa_for_jet.pub`（公開鍵）が作成されます。

### Jetson Nanoの設定

1. Jetson Nanoに直接アクセスできる状態で、端末を開きます。

2. SSHを有効にします：
3. 
   ```python
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

4. 制御用PCで作成した公開鍵をJetson Nanoに追加します：
   ```python
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```

5. 制御用PCからJetson Nanoに公開鍵をコピーします。制御用PCで以下のコマンドを実行：
   ```python
   scp ~/.ssh/id_rsa_for_jet.pub maki@maki-jetson:~/.ssh/authorized_keys
   ```
   （`maki`と`maki-jetson`は適宜あなたのユーザー名とJetson NanoのIPアドレスに置き換えてください）

6. Jetson Nanoで、コピーした鍵の権限を設定します：
   ```python
   chmod 600 ~/.ssh/authorized_keys
   ```

### 制御用PCの設定

1. 制御用PCの`~/.ssh/config`ファイルに以下の設定を追加します：

   ```
   Host maki-jetson
     HostName maki-jetson
     User maki
     IdentityFile "~/.ssh/id_rsa_for_jet"
   ```

   - `HostName`はJetson NanoのIPアドレスまたはホスト名
   - `User`はJetson Nanoのユーザー名
   - `IdentityFile`は先ほど作成した秘密鍵のパス

2. SSH接続をテストします：
   ```python
   ssh maki-jetson
   ```

これで、パスワード入力なしでJetson Nanoに安全に接続できるようになりました。

## Roomba 980との接続

次に、Roomba 980とJetson Nanoを接続します：

1. Roomba 980の清掃ボタン付近にあるMicroUSBポートを探す
2. USB-MicroUSBケーブルでRoombaとJetson Nanoを接続
3. SSHでJetson Nanoに接続し、端末を開く

## デバイスの確認と詳細情報の取得

接続後、デバイスが正しく認識されているか確認します：

1. 端末で以下のコマンドを実行：

```python
ls -l /dev/ttyACM*
```

```python
maki@maki-jetson2:~$ ls -l /dev/ttyACM*
crw-rw---- 1 maki maki 166, 0  7月  2 20:48 /dev/ttyACM0
```

`/dev/ttyACM0`のような表示が出れば接続成功です。

2. デバイスの詳細情報を取得するには、次のコマンドを使用：

```python
udevadm info -a -n /dev/ttyACM0
```

```python
  looking at parent device '/devices/70090000.xusb/usb1/1-3/1-3.1':
    KERNELS=="1-3.1"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb"
    ATTRS{authorized}=="1"
    ATTRS{avoid_reset_quirk}=="0"
    ATTRS{bConfigurationValue}=="1"
    ATTRS{bDeviceClass}=="02"
    ATTRS{bDeviceProtocol}=="00"
    ATTRS{bDeviceSubClass}=="00"
    ATTRS{bMaxPacketSize0}=="64"
    ATTRS{bMaxPower}=="100mA"
    ATTRS{bNumConfigurations}=="1"
    ATTRS{bNumInterfaces}==" 2"
    ATTRS{bcdDevice}=="0200"
    ATTRS{bmAttributes}=="c0"
    ATTRS{busnum}=="1"
    ATTRS{configuration}==""
    ATTRS{devnum}=="10"
    ATTRS{devpath}=="3.1"
    ATTRS{idProduct}=="0002"
    ATTRS{idVendor}=="27a6"
    ATTRS{ltm_capable}=="no"
    ATTRS{manufacturer}=="iRobot Corporation"
    ATTRS{maxchild}=="0"
    ATTRS{product}=="iRobot Roomba"
    ATTRS{quirks}=="0x0"
    ATTRS{removable}=="unknown"
    ATTRS{serial}=="4900574A3533"
    ATTRS{speed}=="12"
    ATTRS{urbnum}=="124"
    ATTRS{version}==" 2.00"
```

このコマンドは、接続されたRoombaの詳細情報を表示します。主な情報は以下の通りです：

- デバイス: `/dev/ttyACM0`
- サブシステム: `tty`
- ドライバ: `cdc_acm`
- 製造元: `iRobot Corporation`
- 製品: `iRobot Roomba`
- シリアル番号: `4900574A3533`
- ベンダーID: `27a6`
- プロダクトID: `0002`

この情報は、デバイスの識別やトラブルシューティングに役立ちます。

## 権限の設定

Jetson NanoがRoombaと通信できるように、権限を設定する必要があります：

1. 端末で以下のコマンドを実行：

```python
sudo chown $USER:$USER /dev/ttyACM0
```

2. 権限が変更されたか確認：

```python
ls -l /dev/ttyACM0
```

ユーザー名とグループ名が自分のものになっていれば成功です。

## Pythonでの操作

Pythonを使ってRoombaを制御します。まず、必要なライブラリをインストールしましょう：

```python
pip3 install pyserial
```

次に、`roomba_control.py`というファイルを作成し、以下の内容を書き込みます：

```python
import serial
import time

# Roombaとの接続を開始
ser = serial.Serial('/dev/ttyACM0', 115200)

# Roombaを起動
ser.write(b'\x80')  # START command
time.sleep(0.1)

# 安全モードに設定
ser.write(b'\x83')  # SAFE mode
time.sleep(0.1)

# コマンドを送信
command = bytes([0x8B, 0xFF, 0x00, 0xFF])
ser.write(command)
time.sleep(1)  # 1秒間動作

# 接続を終了
ser.close()
```

<blockquote class="twitter-tweet" data-media-max-width="560"><p lang="ja" dir="ltr">Roomba980をPCから操作できた！<br>（超シンプルなコマンドです、LEDが消えるだけですが、、、） <a href="https://t.co/FGFjNBTDI8">https://t.co/FGFjNBTDI8</a> <a href="https://t.co/TuOUDQLICt">pic.twitter.com/TuOUDQLICt</a></p>&mdash; Maki@Sunwood AI Labs. (@hAru_mAki_ch) <a href="https://twitter.com/hAru_mAki_ch/status/1808107654696550869?ref_src=twsrc%5Etfw">July 2, 2024</a></blockquote> 

## トラブルシューティング

問題が発生した場合の対処方法：

1. 「Permission denied」エラーが出る場合：
   - 権限の設定を再確認
   - `sudo chmod 666 /dev/ttyACM0`コマンドを試す

2. Roombaが反応しない場合：
   - ケーブルの接続を確認
   - Roombaのバッテリー残量を確認

3. デバイスが認識されない場合：
   - `udevadm info -a -n /dev/ttyACM0`コマンドでデバイス情報を確認
   - USBケーブルや接続ポートを変更してみる

## 発展的な使い方

基本操作ができるようになったら、次のステップに挑戦してみましょう：

1. センサー情報の取得：Roombaの各種センサーから情報を読み取り、障害物回避などの機能を実装

2. 自動掃除プログラム：特定のパターンで動くよう命令を組み合わせ、自動掃除プログラムを作成

3. カメラとの連携：Jetson Nanoにカメラを接続し、画像認識と組み合わせた高度な動作を実現

## まとめ

Jetson NanoでRoomba 980を操作する方法について詳しく解説しました。SSH接続の設定により、リモートからの操作も可能になりました。最初は難しく感じるかもしれませんが、一歩ずつ進めていけば必ず成功します！

ロボットを自分でプログラミングして動かすのは、とてもエキサイティングな体験です。ぜひいろいろな動きを試してみてください。失敗を恐れずに、何度もチャレンジすることが大切です。

これからもロボットプログラミングの世界を楽しんでいってくださいね。頑張ってください！



## 参考サイト

https://mementomorisince2013.blogspot.com/2019/01/roomba-980raspberry-pi.html

https://qiita.com/kosystem/items/0023cfee941fdf099087

https://qiita.com/ozwk/items/7ed89479cf4931970edd


<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
