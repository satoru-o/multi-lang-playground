// Typescript初なので細かく実装
// phase1 ねこちゃんの年齢を人間換算にするだけ

/**
 * ねこちゃんの年齢を人間年齢に換算します
 * @param catAge - ねこちゃんの年齢(正の整数のみ)
 */
function catAgeToHumanAge(catAge: number): number {
    if (!Number.isInteger(catAge)) {
        throw new TypeError("🐱年齢は整数だけにゃ！(バシィ！)")
    } else if (catAge <= 0) {
        throw new RangeError("🐱年齢は1歳より上にゃ！(けりけり！)")
    } else if (catAge <= 2) {
        const convertedCatAge: number = 18 + (catAge - 1) * 9
        return convertedCatAge
    } else {
        const convertedCatAge: number = 18 + 9 + (catAge - 2) * 4
        return convertedCatAge
    }
}

type CatLifestage = "子猫～若猫" | "成猫" | "シニア猫"

/**
 * 人間換算に変換した年齢からねこちゃんのライフステージを判定します
 * @param convertedCatAge
 */
function judgeCatLifestage(convertedCatAge:number): CatLifestage {
    if (convertedCatAge >= 56) {
        return "シニア猫"
    } else if (convertedCatAge >= 31) {
        return "成猫"
    } else {
        return "子猫～若猫"
    }
}

type CatComment = "にゃっ！" | "にゃー" | "にゃ"
/**
 * ねこちゃんのライフステージからコメントを決定する
 * @param CatLifestage
 */
function catCommentRouting(catLifestage:CatLifestage): CatComment {
    if (catLifestage === "子猫～若猫") {
        return "にゃっ！"
    } else if (catLifestage === "成猫") {
        return "にゃー"
    } else {
        return "にゃ"
    }
}

const nyanChanAge: number = 3
const convertedNyanChanAge: number = catAgeToHumanAge(nyanChanAge)
const nyanChanLifestage: CatLifestage = judgeCatLifestage(convertedNyanChanAge)
const nyanChanComment: CatComment = catCommentRouting(nyanChanLifestage)

console.log(`🐱ねこちゃん、いま ${convertedNyanChanAge} さい！`)
console.log(`🐱ねこちゃん、いま ${nyanChanLifestage} ！`)

for (let i = 0; i < nyanChanAge; i++) {
    const inputNyanChanAge = i + 1;
    
    const indexConvertedNyanChan: number = catAgeToHumanAge(inputNyanChanAge)
    const indexNyanChanLifestage: CatLifestage = judgeCatLifestage(indexConvertedNyanChan)
    const indexNyanChanComment: CatComment = catCommentRouting(indexNyanChanLifestage)

    console.log(`${inputNyanChanAge}歳(人間年齢${indexConvertedNyanChan}歳): ${indexNyanChanComment}`)
}

console.log(`この子は現在 ${nyanChanLifestage} です。（人間年齢換算: ${convertedNyanChanAge}歳）`)