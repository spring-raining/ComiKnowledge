# -*- coding: utf-8 -*-

APP_NAME = "ComiKnowledge"
VERSION = "C85.2.0"
COMIKET_NUMBER = 88
HEADER_NAME = "ComicMarket88"
DEFAULT_COLOR = {1: "FF944A",
                 2: "FF00FF",
                 3: "FFF700",
                 4: "00B54A",
                 5: "00B5FF",
                 6: "9C529C",
                 7: "0000FF",
                 8: "00FF00",
                 9: "FF0000"}
BLOCK_ID = {1: u"東A",
            2: u"東B",
            3: u"東C",
            4: u"東D",
            5: u"東E",
            6: u"東F",
            7: u"東G",
            8: u"東H",
            9: u"東I",
            10: u"東J",
            11: u"東K",
            12: u"東L",
            13: u"東M",
            14: u"東N",
            15: u"東O",
            16: u"東P",
            17: u"東Q",
            18: u"東R",
            19: u"東S",
            20: u"東T",
            21: u"東U",
            22: u"東V",
            23: u"東W",
            24: u"東X",
            25: u"東Y",
            26: u"東Z",
            27: u"東ア",
            28: u"東イ",
            29: u"東ウ",
            30: u"東エ",
            31: u"東オ",
            32: u"東カ",
            33: u"東キ",
            34: u"東ク",
            35: u"東ケ",
            36: u"東コ",
            37: u"東サ",
            38: u"東シ",
            39: u"東ス",
            40: u"東セ",
            41: u"東ソ",
            42: u"東タ",
            43: u"東チ",
            44: u"東ツ",
            45: u"東テ",
            46: u"東ト",
            47: u"東ナ",
            48: u"東ニ",
            49: u"東ヌ",
            50: u"東ネ",
            51: u"東ノ",
            52: u"東ハ",
            53: u"東パ",
            54: u"東ヒ",
            55: u"東ピ",
            56: u"東フ",
            57: u"東プ",
            58: u"東ヘ",
            59: u"東ペ",
            60: u"東ホ",
            61: u"東ポ",
            62: u"東マ",
            63: u"東ミ",
            64: u"東ム",
            65: u"東メ",
            66: u"東モ",
            67: u"東ヤ",
            68: u"東ユ",
            69: u"東ヨ",
            70: u"東ラ",
            71: u"東リ",
            72: u"東ル",
            73: u"東レ",
            74: u"東ロ",
            75: u"西あ",
            76: u"西い",
            77: u"西う",
            78: u"西え",
            79: u"西お",
            80: u"西か",
            81: u"西き",
            82: u"西く",
            83: u"西け",
            84: u"西こ",
            85: u"西さ",
            86: u"西し",
            87: u"西す",
            88: u"西せ",
            89: u"西そ",
            90: u"西た",
            91: u"西ち",
            92: u"西つ",
            93: u"西て",
            94: u"西と",
            95: u"西な",
            96: u"西に",
            97: u"西ぬ",
            98: u"西ね",
            99: u"西の",
            100: u"西は",
            101: u"西ひ",
            102: u"西ふ",
            103: u"西へ",
            104: u"西ほ",
            105: u"西ま",
            106: u"西み",
            107: u"西む",
            108: u"西め",
            109: u"西も",
            110: u"西や",
            111: u"西ゆ",
            112: u"西よ",
            113: u"西ら",
            114: u"西り",
            115: u"西る",
            116: u"西れ"}
SPACE_NUMBER = {
    1:{
         1: 89          ,  3: 60 ,  4: 60 ,  5: 60 ,  6: 60 ,  7: 60 ,  8: 60 ,  9: 60 , 10: 60 , 11: 60 , 12: 60 , 13: 48 , 14: 48 , 15: 60 , 16: 60 , 17: 60 , 18: 60 , 19: 60 , 20: 60 , 21: 60 , 22: 60 , 23: 60 , 24: 60 , 25: 48 , 26: 48 , 27: 60 , 28: 60 , 29: 60 , 30: 60 , 31: 60 , 32: 60 , 33: 60 , 34: 60 , 35: 60 , 36: 60 , 37: 52 ,
        38: 89 , 39: 52 , 40: 60 , 41: 60 , 42: 60 , 43: 60 , 44: 60 , 45: 60 , 46: 60 , 47: 60 , 48: 60 , 49: 60 , 50: 48 , 51: 48 , 52: 60 , 53: 60 , 54: 60 , 55: 60 , 56: 60 , 57: 60 , 58: 60 , 59: 60 , 60: 60 , 61: 60 , 62: 48 , 63: 48 , 64: 60 , 65: 60 , 66: 60 , 67: 60 , 68: 60 , 69: 60 , 70: 60 , 71: 60 , 72: 60 , 73: 60 , 74: 52 ,
        75: 72 , 76: 44 , 77: 46 , 78: 46 , 79: 46 , 80: 46 , 81: 44 , 82: 42 , 83: 42 , 84: 42 , 85: 42 , 86: 42 , 87: 42 , 88: 18 , 89: 18 , 90: 22 , 91: 22 , 92: 22 , 93: 22 , 94: 22 , 95: 20 , 96: 20 , 97: 22 , 98: 22 , 99: 22 , 100: 22 , 101: 22 , 102: 18 , 103: 18 , 104: 42 , 105: 42 , 106: 42 , 107: 42 , 108: 42 , 109: 42 , 110: 44 , 111: 46 , 112: 46 , 113: 46 , 114: 46 , 115: 44 , 116: 72
    },
    2:{
         1: 89 ,  2: 52 ,  3: 60 ,  4: 60 ,  5: 60 ,  6: 60 ,  7: 60 ,  8: 60 ,  9: 60 , 10: 60 , 11: 60 , 12: 60 , 13: 48 , 14: 48 , 15: 60 , 16: 60 , 17: 60 , 18: 60 , 19: 60 , 20: 60 , 21: 60 , 22: 60 , 23: 60 , 24: 60 , 25: 48 , 26: 48 , 27: 60 , 28: 60 , 29: 60 , 30: 60 , 31: 60 , 32: 60 , 33: 60 , 34: 60 , 35: 60 , 36: 60 , 37: 52 ,
        38: 89 , 39: 52 , 40: 60 , 41: 60 , 42: 60 , 43: 60 , 44: 60 , 45: 60 , 46: 60 , 47: 60 , 48: 60 , 49: 60 , 50: 48 , 51: 48 , 52: 60 , 53: 60 , 54: 60 , 55: 60 , 56: 60 , 57: 60 , 58: 60 , 59: 60 , 60: 60 , 61: 60 , 62: 48 , 63: 48 , 64: 60 , 65: 60 , 66: 60 , 67: 60 , 68: 60 , 69: 60 , 70: 60 , 71: 60 , 72: 60 , 73: 60 , 74: 52 ,
        75: 72 , 76: 44 , 77: 46 , 78: 46 , 79: 46 , 80: 46 , 81: 44 , 82: 42 , 83: 42 , 84: 42 , 85: 42 , 86: 42 , 87: 42 , 88: 18 , 89: 18 , 90: 22 , 91: 22 , 92: 22 , 93: 22 , 94: 22 , 95: 20 , 96: 20 , 97: 22 , 98: 22 , 99: 22 , 100: 22 , 101: 22 , 102: 18 , 103: 18 , 104: 42 , 105: 42 , 106: 42 , 107: 42 , 108: 42 , 109: 42 , 110: 44 , 111: 46 , 112: 46 , 113: 46 , 114: 46 , 115: 44 , 116: 72
    },
    3:{
         1: 89          ,  3: 60 ,  4: 60 ,  5: 60 ,  6: 60 ,  7: 60 ,  8: 60 ,  9: 60 , 10: 60 , 11: 60 , 12: 60 , 13: 48 , 14: 48 , 15: 60 , 16: 60 , 17: 60 , 18: 60 , 19: 60 , 20: 60 , 21: 60 , 22: 60 , 23: 60 , 24: 60 , 25: 48 , 26: 48 , 27: 60 , 28: 60 , 29: 60 , 30: 60 , 31: 60 , 32: 60 , 33: 60 , 34: 60 , 35: 60 , 36: 60 ,
        38: 89          , 40: 60 , 41: 60 , 42: 60 , 43: 60 , 44: 60 , 45: 60 , 46: 60 , 47: 60 , 48: 60 , 49: 60 , 50: 48 , 51: 48 , 52: 60 , 53: 60 , 54: 60 , 55: 60 , 56: 60 , 57: 60 , 58: 60 , 59: 60 , 60: 60 , 61: 60 , 62: 48 , 63: 48 , 64: 60 , 65: 60 , 66: 60 , 67: 60 , 68: 60 , 69: 60 , 70: 60 , 71: 60 , 72: 60 , 73: 60 , 74: 52 ,
        75: 72 , 76: 44 , 77: 46 , 78: 46 , 79: 46 , 80: 46 , 81: 44 , 82: 42 , 83: 42 , 84: 42 , 85: 42 , 86: 42 , 87: 42 , 88: 18 , 89: 18 , 90: 22 , 91: 22 , 92: 22 , 93: 22 , 94: 22 , 95: 20 , 96: 20 , 97: 22 , 98: 22 , 99: 22 , 100: 22 , 101: 22 , 102: 18 , 103: 18 , 104: 42 , 105: 42 , 106: 42 , 107: 42 , 108: 42 , 109: 42 , 110: 44 , 111: 46 , 112: 46 , 113: 46 , 114: 46 , 115: 44 , 116: 72
    }
}