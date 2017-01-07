# wareki-python (β版)
元号(年号)と和暦を表現するクラス。西暦と和暦の相互変換可能。

## 和暦の表現方法

```python:
>>> Wareki(Gengo('平成'), 32)
Wareki(Gengo('平成'), 32)

>>> S(39)
Wareki(Gengo('昭和'), 39)

>>> str(H(32))
'平成32年'
```

## 西暦を和暦に変換する

```python:
>>> Wareki.from_ad(2020)
Wareki(Gengo('平成'), 32)
```

## 和暦を西暦に変換する

```python:
>>> H(32).to_ad()
2020

# 次のように、int()に渡すこともできます。
>>> int(H(32))
2020
```
