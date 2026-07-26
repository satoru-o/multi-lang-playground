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

const nyanChanAge: number = 3
const convertedNyanChanAge: number = catAgeToHumanAge(nyanChanAge)

console.log(`🐱ねこちゃん、いま ${convertedNyanChanAge} さい！`)