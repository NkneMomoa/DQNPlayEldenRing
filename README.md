### DQNPlayEldenRing
#UndergraduateThesis  →　But  Not Success


I have set up 11 player actions: ① Do nothing, ② Attack, ③ Jump, ④-⑦ Move up, down, left, right, ⑧-⑪ Dodge actions in the up, down, left, right directions.

In this study, it was difficult to obtain environment information from memory to obtain commercially available Elden Ring environment information. Therefore, during training, all environment information was obtained through image recognition (OpenCV). 

Therefore, in this study, the enemy's hit point bar (referred to as "HP bar"), the player's HP bar, and stamina bar were quantified from the game screen and used to assess the environment state and rewards. Additionally, when attacked by an enemy, a debuff bar indicating attribute damage appears in the center of the screen. In this experiment, the character cannot take actions to recover their own HP, so the debuff progress bar reaches 100% and no additional attribute damage is generated. However, this progress bar is located in the center of the screen, so to avoid it affecting the screen analysis, those parts were removed before capturing. Therefore, the player and enemy states were captured in a screen size of 144 in length and 68 in width, then downscaled by 2 and converted to grayscale before being input into the CNN for environment state assessment. The captured area is indicated by the frame in Figure 2. The numerical settings for each reward are shown in Table 3.

![image](https://github.com/NkneMomoa/DQNPlayEldenRing/assets/65263314/48681a7d-dd7e-45ec-99c1-b2cc77975592)

Figure 2. Captured Screen Area


|State|Reward |
| :-: | :-: |
|<p>Player HP bar = 0</p><p>Enemy BOSS HP bar = 0</p><p>Player gets hit by enemy attack</p><p>Player's attack hits the enemy</p><p>Stamina bar becomes empty after performing an action</p>|<p>-100</p><p>+100</p><p>-45</p><p>+30</p><p>-10</p>|

Table 3. Reward Settings

The DQN neural network consists of a combination of a Current Network and a Target Network. The structure of each network includes convolutional layers, pooling layers, hidden layers, and an output layer. Additionally, dropout is implemented in the convolutional layers and hidden layers. Dropout is a technique used during the training of neural networks to randomly deactivate a certain percentage of neurons, thereby preventing overfitting.<sup>4)</sup> The two neural networks are constructed with the same settings, as shown in Table 4. Table 4. Neural Network Configuration

|Input Layer|tf.placeholder||
| :-: | :-: | :- |
|<p>Convolutional Layer</p><p>Pooling Layer</p>|<p>5，5，32，64</p><p>2\*2</p>|Activation Function ReLU|
|<p>Convolutional Layer</p><p>Pooling Layer</p>|<p>5，5，32，64</p><p>2\*2</p>|Activation Function ReLU|
|Fully Connected Layer|512|Activation Function ReLU|
|Hidden Layer|Dropout　0.5||
|Fully Connected Layer|256|Activation Function ReLU|
|Hidden Layer|Dropout　0.25||
|Output Layer|Dropout　0.25||

The exploration method for selecting actions is using the ε-greedy strategy, which determines whether the agent chooses an action or not. For each state, the expected reward that each action yields is saved as the Q-value. The Q-value is obtained using a neural network trained with the Q-function. In the code, the self.Q_value.eval() function is called to compute the Q-value for the current state. In the ε-greedy strategy, actions are randomly chosen with a probability of ε, and the action with the maximum Q-value is chosen with a probability of 1-ε. The code uses the random.random() function to return True with a probability of ε and False with a probability of 1-ε. If random.random() returns True (i.e., with a probability of ε), a random action is chosen from the action space. On the other hand, if random.random() returns False (i.e., with a probability of 1-ε), the action with the maximum Q-value is selected. To select the action with the maximum Q-value, the np.argmax() function is used to obtain the index of the maximum value from the Q-value list. Finally, in this function, the agent selects actions randomly.

The details of the parameters used in this approach are presented in Table 5.

Table 5. Used Parameters 


<table>
  <tr>
    <th></th>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td rowspan="3">General Parameters</td>
    <td>ACTION_SIZE</td>
    <td>11</td>
  </tr>
  <tr>
    <td>EPISODES</td>
    <td>1000</td>
  </tr>
  <tr>
    <td>UPDATE_STEP</td>
    <td>50</td>
  </tr>
  <tr>
    <td rowspan="4">DQN Hyperparameters</td>
    <td>GAMMA</td>
    <td>0.9</td>
  </tr>
  <tr>
    <td>Learning rate</td>
    <td>0.0005</td>
  </tr>
  <tr>
    <td>Epsilon initial value</td>
    <td>0.5</td>
  </tr>
  <tr>
    <td>Epsilon final value</td>
    <td>0.01</td>
  </tr>
  <tr>
    <td rowspan="3">Mini-batch Sizes</td>
    <td>SMALL_BATCH_SIZE</td>
    <td>18</td>
  </tr>
  <tr>
    <td>BIG_BATCH_SIZE</td>
    <td>144</td>
  </tr>
  <tr>
    <td>BATCH_SIZE_DOOR</td>
    <td>1000</td>
  </tr>
</table>


### 日本語：

プレイヤーのアクションを11個設置した：①何もしない、②攻撃、③ジャンプ、④～⑦上下左右の移動、⑧～⑪上下左右の回避アクションの①～⑪である。

本研究では市販されたElden Ring環境情報を得るため、メモリからの環境情報読み取りは困難で、故に訓練中すべての環境情報は画像認識（OpenCV）の手段で得られた。

そこで、今回の研究はゲーム画面から、敵のヒットポイントバー（以下「HPバー」と称する）、プレイヤーのHPバー、体力バーを数値化し環境状態とrewardの判断に使用した。また、敵から攻撃を受けた場合、画面の中央に属性ダメージのデバフバーが出る、今回の実験のキャラクターは、自分のHPを回復する行動を取れないために、デバフプログレスバーは100％に達して额外の属性ダメージが生成しない。しかし、このプログレスバーは画面の真ん中にあり、プログレスバーが画面の分析に影響を与えないように、これらの部分を取り除いてキャプチャーしていた。故に長さ144、幅68の画面でプレイヤーと敵の状態をキャプチャーし、それを2倍縮小してグレースケールに変換してCNNに入力し環境状態を判断するためのデータとする。キャプチャーした範囲は図2の枠に表す。また、各Rewardの数値設置は表３に表す。

![image](https://github.com/NkneMomoa/DQNPlayEldenRing/assets/65263314/48681a7d-dd7e-45ec-99c1-b2cc77975592)

図2. 画面キャプチャーした範囲


|状態|Reward |
| :-: | :-: |
|<p>プレイヤーHPバー = ０</p><p>敵BOSS HPバー = ０</p><p>自分が敵の攻撃を受けた</p><p>自分の攻撃が敵に当たる</p><p>アクションを実行後体力バーがエンプティ</p>|<p>-100</p><p>+100</p><p>-45</p><p>+30</p><p>-10</p>|

表３. Rewardの設定



DQNのニューラルネットワークはCurrent　NetworkとTarget Networkで組み合わせた。各層の構造は、畳み込み層、プーリング層、隠れ層、出力層からなるニューラルネットワークです。また、畳み込み層と隠れ層にドロップアウトを実装している。ドロップアウトとは、ニューラルネットワークの学習中に一定の割合でニューロンを無効化することで、過学習を防ぐ手法です。<sup>4)</sup>二つのニューラルネットワークは構築を同じく設定し表４に表す。

表４. ニューラルネットワーク構築

|入力層|tf.placeholder||
| :-: | :-: | :- |
|<p>畳み込み層</p><p>プーリング層</p>|<p>5，5，32，64</p><p>2\*2</p>|活性化関数ReLU|
|<p>畳み込み層</p><p>プーリング層</p>|<p>5，5，32，64</p><p>2\*2</p>|活性化関数ReLU|
|全結合層|512|活性化関数ReLU|
|隠れ層|Dropout　0.5||
|全結合層|256|活性化関数ReLU|
|隠れ層|Dropout　0.25||
|輸出層|Dropout　0.25||

Actionの探索方法はε-greedy法と呼ばれる手法を使用して、エージェントが行動を選択するかどうかを決定している。まず、各状態に対して、各行動が与える期待報酬をQ値として保存しる。Q値は、Q関数を使用して学習されるニューラルネットワークで出力される。コードでは、Q関数を使用して、現在の状態に対するQ値を求めるために、self.Q\_value.eval()関数を呼び出している。ε-greedy法では、確率εでランダムに行動を選択し、確率1-εでQ値が最大の行動を選択するというものである。コードでは、random.random()関数を使用して、確率εでTrue、確率1-εでFalseを返すようにしている。もし、random.random()関数がTrueを返す場合、つまり確率εである場合、行動空間からランダムな行動を選択する。一方で、random.random()関数がFalseを返す場合、つまり確率1-εである場合、Q値が最大の行動を選択する。Q値が最大の行動を選択するためには、Q値のリストから、最大値のインデックスを取得するために、np.argmax()関数を使用している。最後に、この関数では、エージェントがランダムに行動を選択する。

また、今回使用した各パラメータの詳細は表５に示す。



表5.　 DQN のハイパーパラメータ

<table><tr><th></th><th>パラメータ</th><th>数値</th></tr>
<tr><td rowspan="3">一般パラメータ</td><td>ACITON SIZE</td><td>11</td></tr>
<tr><td>EPISODES</td><td>1000</td></tr>
<tr><td>UPDATE_STEP</td><td>50</td></tr>
<tr><td rowspan="4">DQN のハイパーパラメータ</td><td>GAMMA</td><td>0\.9</td></tr>
<tr><td>学習率</td><td>0\.0005</td></tr>
<tr><td>イプシロンの開始値</td><td>0\.5</td></tr>
<tr><td>イプシロンの最終値</td><td>0\.01</td></tr>
<tr><td rowspan="3">ミニバッチのサイズ</td><td>SMALL_BATCH_SIZE</td><td>18</td></tr>
<tr><td>BIG_BATCH_SIZE</td><td>144</td></tr>
<tr><td>BATCH_SIZE_DOOR</td><td>1000</td></tr>
</table>
