# 整理
"""
1. ねこちゃんの年齢を取得する
2. 与えられたねこちゃんの年齢を人間換算にする
3. 2.でも求めた年齢からライフステージを判定する
4. 1歳から与えられた年齢まで人間換算した値とねこちゃんコメントを出力する
5. 最後にねこちゃんの年齢を人間換算した値とライフステージを出力する

とりあえず、
- ねこちゃん年齢->人間換算年齢変換関数
- ねこちゃんライフステージ判定関数
- ねこちゃんライフステージからねこちゃんコメント決定関数
- 後はハンドラーでループとprintがあればいい
"""

def cat_age_human_age_conversion(cat_age: int) -> int:
    """
    1歳のねこちゃんは人間で18歳換算
    2歳は+9する(27歳になる)
    3歳以降は1歳増加するごとに+4歳として扱う

    Arg:
        cat_age: int ねこちゃんの年齢(正の整数のみ)
    Return:
        converted_cat_age: int 人間換算された年齢
    Exception:
        cat_age <= 0 1歳以上である必要がある
    """

    if type(cat_age) != int:
        raise TypeError(f"不正なデータ型にゃ！(容赦ない砂かけ): {cat_age} (正の整数のみ許可されています)")
    elif cat_age <= 0:
        raise ValueError(f"不正な値にゃ！(情け容赦ない砂かけ): {cat_age} (正の整数のみ許可されています)")
    elif cat_age <= 2:
        converted_cat_age = 18 + (cat_age - 1) * 9
    else:
        converted_cat_age = 18 + 9 + (cat_age - 2) * 4
    
    return converted_cat_age

def judge_cat_lifestage(converted_cat_age: int) -> str:
    """
    ねこちゃんの年齢を人間換算に変換した年齢でライフステージを判定する
    30歳以下：子猫～若猫
    31~55歳：成猫
    56歳以上：シニア猫

    Arg:
        converted_cat_age: str 人間換算されたねこちゃんの年齢
    Return:
        cat_lifestage: str ねこちゃんのライフステージ
    """

    cat_lifestage = ""

    if converted_cat_age >= 56:
        cat_lifestage = "シニア猫"
    elif converted_cat_age >= 31:
        cat_lifestage = "成猫"
    else:
        cat_lifestage = "子猫～若猫"
    
    return cat_lifestage

def cat_comment_routing(cat_lifestage: str) -> str:
    """
    ねこちゃんのライフステージからコメントを決定する
    子猫～若猫：にゃっ！
    成猫：にゃー
    シニア猫：にゃ
    
    Arg:
        cat_lifestage: str ねこちゃんのライフステージ
    Return:
        cat_comment: str ねこちゃんのコメント
    """

    cat_comment = ""

    if cat_lifestage == "シニア猫":
        cat_comment = "にゃ"
    elif cat_lifestage == "成猫":
        cat_comment = "にゃー"
    else:
        cat_comment = "にゃっ！"
    
    return cat_comment

if __name__ == '__main__':
    cat_age = 5

    for i in range(cat_age):
        input_cat_age = i + 1
        converted_cat_age = cat_age_human_age_conversion(input_cat_age)
        cat_lifestage = judge_cat_lifestage(converted_cat_age)
        cat_comment = cat_comment_routing(cat_lifestage)

        print(f"{input_cat_age}歳(人間年齢{converted_cat_age}歳): 🐱{cat_comment}")
    
    print(f"この子は現在 {cat_lifestage} です。 （人間年齢換算: {converted_cat_age}歳）")