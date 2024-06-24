import {computed, ref} from 'vue'
import {defineStore} from 'pinia'

export const LangStore = defineStore('LangOption', () => {
    const LangList: { [key: string]: any } = ref({
        中文: 'zh',
        英语: 'en',
        西班牙语: 'spa',
        法语: 'fra',
        德语: 'de',
        俄语: 'ru',
        葡萄牙语: 'pt',
        日语: 'jp',
        韩语: 'kor',
        意大利语: 'it'
    })

    const TargetLangList: { [key: string]: any } = ref({
        中文: 'zh',
        '中文（巴金）': 'zh-bajin',
        '中文（冰心）': 'zh-bingxin',
        '中文（曹禺）': 'zh-caoyu',
        '中文（郭沫若）': 'zh-guomoruo',
        '中文（老舍）': 'zh-laoshe',
        '中文（刘慈欣）': 'zh-liucixin',
        '中文（鲁迅）': 'zh-luxun',
        '中文（莫言）': 'zh-moyan',
        '中文（沈从文）': 'zh-shencongwen',
        '中文（余华）': 'zh-yuhua',
        英语: 'en',
        '英语（拜伦）': 'en-bailun',
        '英语（查尔斯）': 'en-chaersi',
        '英语（笛福）': 'en-difu',
        '英语（歌德）': 'en-gede',
        '英语（海明威）': 'en-haimingwei',
        '英语（J.K.罗琳）': 'en-jkrowlin',
        '英语（欧亨利）': 'en-ouhenli',
        '英语（莎士比亚）': 'en-shashibiya',
        '英语（斯蒂芬妮）': 'en-sidifenni',
        '英语（雨果）': 'en-yuhuo',
        西班牙语: 'spa',
        法语: 'fra',
        德语: 'de',
        俄语: 'ru',
        葡萄牙语: 'pt',
        日语: 'jp',
        韩语: 'kor',
        意大利语: 'it'
    })

    const modelName = ref()

    const defaultSourceLang = ref('中文')
    const getSourceLang = computed(() => defaultSourceLang.value)
    const defaultTargetLang = ref('英语')
    const getTargetLang = computed(() => defaultTargetLang.value)
    const isInput = ref(false)

    function getLangKeys() {
        return Object.keys(LangList.value)
    }

    function getLangCode() {
        return {
            src: LangList.value[getSourceLang.value],
            tgt: TargetLangList.value[getTargetLang.value]
        }
    }

    function changeSourceLang(lang_name: string) {
        defaultSourceLang.value = lang_name
    }

    function changeTargetLang(lang_name: string) {
        defaultTargetLang.value = lang_name
    }

    function getTargetLangKeys() {
        return Object.keys(TargetLangList.value).filter((lang) => lang !== getSourceLang.value)
    }

    function getSourceLangKeys() {
        return Object.keys(LangList.value).filter((lang) => lang !== getTargetLang.value)
    }

    function setModelName(modelname) {
        modelName.value = modelname
    }

    function swapLang() {
        let pastSource = getSourceLang.value
        let pastTarget = getTargetLang.value
        if (pastTarget.includes('英语')) pastTarget = '英语'
        else if (pastTarget.includes('中文')) pastTarget = '中文'
        if (pastTarget === pastSource) {
            pastTarget === '英语' ? (pastSource = '中文') : (pastSource = '英语')
        }
        changeSourceLang(pastTarget)
        changeTargetLang(pastSource)
    }

    return {
        LangList,
        isInput,
        modelName,
        defaultTargetLang,
        getLangKeys,
        getLangCode,
        changeSourceLang,
        changeTargetLang,
        getSourceLang,
        getTargetLang,
        getTargetLangKeys,
        getSourceLangKeys,
        swapLang,
        setModelName
    }
})
