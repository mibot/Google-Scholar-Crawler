import os
import re

import pandas as pd
from base import db, cur

import random

from mstranslator import Translator

key_choices = ["e6e5859bfb4b40baa45e2105dc4880e9",
               "9ed1db3b52234167b9aadf2cbc4c9b78", ]


def languageDetection():
    # sql = 'select id from resolved_papers where downloaded = 1 and npages >= 5 and pdf2text = 1 and english = 0 and id in (12,	70,	74,	77,	92,	108,	110,	111,	113,	127,	128,	129,	133,	136,	145,	149,	151,	189,	210,	223,	238,	247,	253,	276,	287,	289,	291,	292,	303,	308,	345,	346,	347,	349,	350,	351,	354,	355,	359,	360,	361,	362,	363,	364,	365,	368,	377,	381,	389,	393,	395,	406,	414,	424,	439,	446,	448,	549,	554,	558,	574,	577,	578,	579,	581,	582,	583,	585,	588,	589,	591,	592,	595,	597,	601,	604,	605,	609,	613,	621,	625,	682,	684,	712,	713,	714,	715,	716,	717,	719,	722,	723,	724,	726,	730,	731,	732,	734,	735,	738,	739,	740,	743,	749,	751,	752,	753,	754,	755,	758,	765,	782,	787,	816,	822,	830,	836,	851,	857,	860,	861,	869,	882,	970,	1044,	1045,	1047,	1050,	1052,	1055,	1056,	1057,	1058,	1060,	1061,	1062,	1063,	1064,	1065,	1066,	1068,	1069,	1072,	1073,	1074,	1075,	1076,	1079,	1080,	1083,	1084,	1086,	1087,	1089,	1094,	1100,	1104,	1105,	1106,	1115,	1116,	1117,	1122,	1124,	1125,	1126,	1131,	1133,	1142,	1143,	1146,	1150,	1151,	1172,	1174,	1176,	1184,	1194,	1248,	1283,	1301,	1307,	1309,	1367,	1381,	1417,	1419,	1452,	1456,	1482,	1491,	1507,	1511,	1513,	1522,	1542,	1562,	1585,	1587,	1591,	1624,	1626,	1628,	1652,	1687,	1688,	1689,	1692,	1693,	1694,	1696,	1698,	1699,	1701,	1704,	1710,	1711,	1714,	1716,	1719,	1720,	1727,	1728,	1730,	1745,	1750,	1751,	1755,	1757,	1770,	1809,	1815,	1820,	1831,	1835,	1872,	1884,	1887,	1898,	1935,	1955,	1993,	2009,	2025,	2026,	2029,	2030,	2031,	2199,	2241,	2244,	2246,	2275,	2276,	2277,	2278,	2279,	2305,	2323,	2324,	2325,	2327,	2328,	2347,	2360,	2402,	2404,	2410,	2415,	2442,	2448,	2450,	2451,	2452,	2461,	2462,	2467,	2477,	2509,	2510,	2512,	2513,	2518,	2522,	2524,	2531,	2543,	2547,	2554,	2555,	2576,	2577,	2578,	2579,	2580,	2583,	2586,	2605,	2609,	2624,	2629,	2646,	2651,	2652,	2653,	2655,	2656,	2659,	2661,	2662,	2671,	2676,	2677,	2756,	2757,	2758,	2760,	2761,	2762,	2768,	2771,	2772,	2773,	2774,	2776,	2777,	2781,	2782,	2783,	2786,	2789,	2790,	2791,	2792,	2793,	2794,	2795,	2798,	2811,	2815,	2822,	2869,	2884,	2907,	2913,	2920,	2924,	3029,	3127,	3141,	3146,	3172,	3173,	3174,	3175,	3176,	3177,	3178,	3180,	3182,	3183,	3184,	3185,	3189,	3192,	3194,	3198,	3199,	3202,	3203,	3207,	3208,	3211,	3223,	3224,	3230,	3236,	3252,	3253,	3262,	3275,	3302,	3305,	3316,	3365,	3388,	3389,	3391,	3392,	3396,	3397,	3398,	3399,	3400,	3401,	3402,	3405,	3406,	3408,	3409,	3412,	3415,	3416,	3418,	3419,	3420,	3421,	3422,	3423,	3424,	3425,	3426,	3427,	3428,	3431,	3432,	3433,	3436,	3438,	3439,	3443,	3444,	3445,	3446,	3450,	3452,	3455,	3456,	3458,	3461,	3466,	3467,	3470,	3503,	3526,	3532,	3536,	3538,	3541,	3542,	3543,	3549,	3563,	3573,	3597,	3598,	3620,	3626,	3662,	3819,	3921,	3922,	3923,	3925,	3927,	3931,	3932,	3933,	3934,	3935,	3936,	3937,	3938,	3939,	3940,	3942,	3943,	3944,	3945,	3948,	3950,	3952,	3953,	3954,	3955,	3957,	3958,	3959,	3960,	3961,	3963,	3965,	3966,	3967,	3968,	3971,	3972,	3980,	3988,	3995,	4000,	4005,	4011,	4039,	4043,	4046,	4048,	4050,	4059,	4077,	4086,	4089,	4098,	4101,	4104,	4109,	4111,	4123,	4127,	4170,	4184,	4203,	4215,	4221,	4235,	4287,	4295,	4345,	4362,	4367,	4448,	4449,	4451,	4452,	4453,	4454,	4455,	4457,	4458,	4459,	4460,	4461,	4462,	4463,	4464,	4465,	4466,	4467,	4468,	4469,	4470,	4472,	4478,	4480,	4481,	4482,	4496,	4500,	4504,	4508,	4513,	4518,	4523,	4524,	4548,	4551,	4567,	4572,	4598,	4607,	4608,	4611,	4657,	4786,	4788,	4789,	4791,	4792,	4793,	4794,	4795,	4796,	4797,	4798,	4799,	4804,	4805,	4811,	4815,	4817,	4819,	4829,	4839,	4840,	5037,	5038,	5040,	5047,	5179,	5191,	5192,	5210,	5248,	5249,	5266,	5275,	5276,	5322,	5323,	5327,	5330,	5362,	5410,	5411,	5416,	5451,	5462,	5493,	5494,	5496,	5519,	5536,	5548,	5555,	5587,	5588,	5589,	5590,	5591,	5594,	5599,	5617,	5633,	5636,	5660,	5667,	5695,	5697,	5701,	5702,	5706,	5767,	5768,	5769,	5773,	5778,	5786,	5831,	5832,	5833,	5835,	5836,	5837,	5839,	5844,	5849,	5850,	5858,	5860,	5889,	5901,	5915,	5916,	5918,	5920,	5991,	5992,	5993,	5994,	5995,	6009,	6045,	6079,	6080,	6081,	6083,	6084,	6085,	6086,	6087,	6100,	6101,	6107,	6185,	6249,	6278,	6279,	6280,	6281,	6282,	6283,	6285,	6305,	6306,	6387,	6393,	6396,	6397,	6398,	6411,	6439,	6498,	6505,	6511,	6513,	6518,	6520,	6524,	6525,	6526,	6527,	6532,	6543,	6553,	6555,	6565,	6566,	6569,	6573,	6574,	6581,	6585,	6601,	6605,	6606,	6612,	6615,	6617,	6621,	6645,	6646,	6648,	6651,	6652,	6658,	6660,	6667,	6672,	6676,	6682,	6684,	6688,	6690,	6692,	6693,	6700,	6704,	6743,	6769,	6771,	6772,	6775,	6778,	6783,	6785,	6789,	6793,	6818,	6824,	6829,	6830,	6834,	6839,	6845,	6846,	6849,	6850,	6855,	6859,	6866,	6873,	6878,	6887,	6888,	6889,	6890,	6907,	6926,	6945,	6948,	6954,	6963,	7006,	7066,	7082,	7102,	7121,	7162,	7163,	7271,	7272,	7273,	7285,	7314,	7315,	7350,	7362,	7364,	7398,	7441,	7442,	7443,	7444,	7446,	7451,	7454,	7456,	7462,	7464,	7504,	7515,	7516,	7547,	7548,	7634,	7659,	7660,	7661,	7662,	7663,	7664,	7665,	7672,	7776,	7777,	7783,	7784,	7788,	7789,	7792,	7795,	7797,	7798,	7799,	7809,	7831,	7889,	7917,	7918,	7920,	7926,	7930,	7932,	7933,	7935,	7936,	7941,	7944,	7960,	7962,	7971,	8008,	8017,	8070,	8075,	8076,	8110,	8111,	8112,	8117,	8120,	8128,	8129,	8130,	8133,	8136,	8140,	8143,	8144,	8145,	8148,	8149,	8150,	8153,	8154,	8159,	8163,	8203,	8225,	8268,	8270,	8302,	8310,	8312,	8419,	8421,	8496,	8497,	8498,	8500,	8505,	8506,	8507,	8508,	8510,	8513,	8517,	8533,	8543,	8584,	8710,	8717,	8718,	8719,	8720,	8721,	8722,	8724,	8726,	8730,	8732,	8733,	8734,	8737,	8739,	8740,	8741,	8742,	8743,	8744,	8745,	8747,	8748,	8750,	8751,	8752,	8753,	8754,	8755,	8756,	8757,	8759,	8761,	8764,	8766,	8768,	8769,	8773,	8774,	8775,	8784,	8811,	8817,	9042,	9056,	9207,	9219,	9240,	9249,	9273,	9318,	9322,	9422,	9457,	9485,	9562,	9623,	9647,	9836,	9837,	9922,	10067,	10068,	10069,	10168,	10185,	10288,	10400,	10401,	10513,	10515,	10606,	10700,	10702,	10703,	10771,	10772,	10819,	10821,	10927,	11019,	11056,	11113,	11142,	11143,	11225,	11226,	11227,	11343,	11361,	11362,	11364,	11377,	11448,	11460,	11461,	11462,	11463,	11465,	11466,	11468,	11493,	11609,	11610,	11611,	11617,	11638,	11659,	11718,	11748,	11749,	11750,	11751,	11762,	11821,	11850,	11891,	11898,	11911,	11913,	11914,	11915,	11916,	11917,	11918,	11919,	11920,	11921,	11922,	11923,	11926,	11928,	11934,	11955,	11980,	12026,	12030,	12044,	12092,	12093,	12094,	12095,	12096,	12098,	12100,	12101,	12102,	12103,	12104,	12105,	12106,	12107,	12108,	12109,	12110,	12111,	12112,	12113,	12114,	12122,	12123,	12125,	12144,	12147,	12234,	12235,	12237,	12256,	12305,	12339,	12346,	12407,	12448,	12511,	12665,	12705,	12706,	12708,	12709,	12710,	12711,	12712,	12713,	12714,	12716,	12717,	12718,	12719,	12720,	12721,	12722,	12725,	12729,	12742,	12753,	12762,	12802,	12813,	12816,	12821,	12823,	12843,	12856,	12905,	12907,	13006,	13061,	13062,	13063,	13137,	13138,	13198,	13329,	13330,	13331,	13332,	13494,	13495,	13582,	13583,	13584,	13585,	13586,	13697,	13833,	13834,	13835,	13836,	13837,	13840,	14160,	14161,	14200,	14341,	14342,	14343,	14590,	14591,	14597,	14610,	14614,	14631,	14632,	14633,	14634,	14635,	14650,	14655,	14656,	14689,	14726,	14777,	14870,	14871,	14872,	14921,	14922,	14923,	14991,	14992,	14993,	14994,	14995,	15136,	15137,	15138,	15139,	15140,	15141,	15142,	15143,	15152,	15216,	15265,	15277,	15387,	15388,	15483,	15546,	15550,	15587,	15590,	15623,	15641,	15653,	15711,	15712,	15730,	15743,	15763,	15794,	15805,	15821,	15831,	15884,	15932,	16039,	16122,	16124,	16153,	16175,	16181,	16220,	16233,	16264,	16277,	16306,	16361,	16377,	16391,	16392,	16393,	16402,	16404,	16431,	16439,	16440,	16444,	16447,	16448,	16455,	16457,	16463,	16468,	16513,	16524,	16528,	16551,	16569,	16594,	16596,	16600,	16610,	16647,	16648,	16718,	16731,	16763,	16765,	16794,	16795,	16899,	16948,	16962,	16993,	16998,	17011,	17013,	17034,	17061,	17062,	17141,	17142,	17143,	17144,	17155,	17158,	17248,	17262,	17263,	17264,	17265,	17266,	17333,	17334,	17335,	17395,	17396,	17398,	17400,	17401,	17405,	17410,	17412,	17417,	17420,	17431,	17547,	17584,	17585,	17587,	17599,	17674,	17676,	17677,	17679,	17711,	17719,	17749,	17750,	17751,	17752,	17753,	17754,	17756,	17757,	17811,	17812,	17814,	17948,	17963,	17964,	17965,	17989,	17998,	18083,	18139,	18145,	18165,	18229,	18230,	18257,	18264,	18273,	18321,	18322,	18323,	18351,	18515,	18548,	18599,	18600,	18623,	18637,	18675,	18676,	18687,	18698,	18736,	18753,	18768,	18792,	18794,	18797,	18823,	18828,	18830,	18850,	18851,	18853,	18854,	18857,	18882,	18885,	18886,	18887,	18888,	18891,	18892,	18893,	18894,	18898,	18901,	18904,	18930,	18947,	18967,	18968,	18970,	18972,	18973,	18974,	18976,	18977,	18980,	18982,	18983,	18984,	18985,	18986,	18991,	19006,	19059,	19060,	19061,	19062,	19064,	19066,	19067,	19069,	19071,	19103,	19104,	19110,	19116,	19153,	19180,	19181,	19186,	19263,	19272,	19273,	19280,	19318,	19409,	19425,	19428,	19456,	19528,	19531,	19538,	19606,	19607,	19609,	19610,	19612,	19613,	19616,	19623,	19636,	19647,	19648,	19685,	19798,	19799,	19800,	19801,	19802,	19805,	19806,	19807,	19808,	19811,	19812,	19813,	19816,	19820,	19821,	19836,	19874,	19875,	19878,	19960,	19985,	20051,	20052,	20053,	20054,	20055,	20056,	20057,	20058,	20059,	20061,	20062,	20063,	20064,	20065,	20066,	20069,	20070,	20071,	20072,	20074,	20078,	20079,	20081,	20084,	20088,	20090,	20110,	20156,	20157,	20168,	20189,	20193,	20245,	20344,	20345,	20346,	20347,	20348,	20349,	20350,	20353,	20354,	20355,	20356,	20357,	20358,	20359,	20360,	20361,	20362,	20363,	20365,	20368,	20370,	20371,	20373,	20374,	20377,	20391,	20392,	20396,	20398,	20400,	20444,	20476,	20520,	20682,	20685,	20687,	20688,	20689,	20690,	20691,	20692,	20693,	20694,	20695,	20698,	20699,	20700,	20701,	20702,	20703,	20707,	20709,	20714,	20728,	20760,	20774,	20864,	20865,	20866,	20867,	20868,	20869,	20870,	20872,	20874,	20899,	20909,	20962,	21041,	21042,	21117,	21118,	21121,	21139,	21146,	21227,	21271,	21272,	21273,	21274,	21275,	21425,	21430,	21493,	21505,	21507,	21510,	21513,	21612,	21616,	21621,	21622,	21623,	21624,	21667,	21675,	21751,	21765,	21766,	21767,	21846,	21847,	21856,	21857,	21858,	21871,	21872,	21873,	21875,	21876,	21877,	21881,	21883,	21885,	21924,	21925,	21957,	21977,	21978,	21979,	21980,	21984,	21985,	21993,	21997,	21999,	22001,	22031,	22033,	22082,	22113,	22175,	22228,	22247,	22271,	22272,	22371,	22374,	22462,	22463,	22613,	22694,	22695,	22696,	22697,	22700,	22880,	22881,	22882,	22883,	22884,	22901,	22977,	22978,	22979,	22981,	23030,	23032,	23191,	23230,	23236,	23238,	23291,	23340,	23453,	23552,	23553,	23744,	23761,	23774,	24016,	24025,	24037,	24085,	24090,	24096,	24125,	24126,	24128,	24129,	24130,	24132,	24133,	24140,	24141,	24142,	24145,	24150,	24151,	24152,	24153,	24155,	24168,	24169,	24170,	24171,	24172,	24173,	24174,	24181,	24186,	24187,	24189,	24190,	24192,	24193,	24206,	24207,	24208,	24209,	24210,	24211,	24212,	24213,	24214,	24239,	24243,	24244,	24246,	24247,	24249,	24250,	24251,	24252,	24253,	24254,	24255,	24256,	24257,	24258,	24261,	24290,	24297,	24298,	24299,	24300,	24301,	24302,	24303,	24304,	24305,	24307,	24308,	24315,	24326,	24330,	24334,	24335,	24336,	24350,	24364,	24365,	24366,	24367,	24368,	24371,	24372,	24390,	24391,	24393,	24405,	24406,	24408,	24411,	24412,	24413,	24415,	24438,	24439,	24440,	24473,	24474,	24476,	24477,	24478,	24479,	24480,	24481,	24483,	24484,	24485,	24486,	24487,	24520,	24522,	24523,	24524,	24525,	24526,	24527,	24528,	24529,	24530,	24531,	24532,	24533,	24535,	24536,	24537,	24540,	24541,	24542,	24543,	24544,	24545,	24546,	24547,	24549,	24550,	24576,	24586,	24621,	24622,	24623,	24624,	24625,	24626,	24627,	24628,	24629,	24630,	24631,	24632,	24633,	24634,	24635,	24636,	24637,	24638,	24639,	24640,	24641,	24642,	24644,	24645,	24646,	24647,	24648,	24651,	24652,	24653,	24654,	24655,	24656,	24657,	24712,	24713,	24714,	24715,	24716,	24717,	24719,	24720,	24721,	24722,	24723,	24724,	24731,	24775,	24795,	24812,	24831,	24833,	24835,	24836,	24845,	24846,	24851,	24869,	24877,	24888,	24889,	24907,	24926,	24952,	25091,	25169,	25177,	25178,	25195,	25206,	25247,	25248,	25251,	25267,	25340,	25345,	25455,	25456,	25460,	25464,	25754,	25822,	25845,	25865,	25890,	25891,	25893,	25914,	25975,	25976,	25978,	25980,	25982,	25986,	25996,	26003,	26074,	26112,	26143,	26172,	26182,	26183,	26186,	26194,	26202,	26283,	26284,	26287,	26289,	26293,	26303,	26316,	26320,	26322,	26463,	26465,	26467,	26469,	26476,	26481,	26486,	26489,	26497,	26596,	26663,	26678,	26717,	27136,	27183,	27307,	27340,	27341,	27342,	27344,	27348,	27355,	27607,	27608,	27609,	27610,	27623,	27635,	27641,	27922,	27937,	28165,	28263,	28277,	28422,	28433,	28437,	28508,	28738,	28739,	28740,	28743,	28748,	28820,	28990,	28993,	28997,	29008,	29009,	29010,	29011,	29079,	29084,	29090,	29093,	29101,	29102,	29104,	29105,	29106,	29112,	29113,	29114,	29119,	29120,	29122,	29123,	29124,	29125,	29129,	29130,	29133,	29134,	29135,	29137,	29139,	29146,	29147,	29172,	29174,	29176,	29184,	29191,	29192,	29194,	29200,	29201,	29203,	29221,	29224,	29225,	29226,	29232,	29234,	29258,	29265,	29268,	29273,	29274,	29275,	29276,	29277,	29278,	29280,	29281,	29282,	29300,	29301,	29302,	29310,	29313,	29314,	29315,	29316,	29320,	29382,	29435,	29436,	29454,	29457,	29458,	29468,	29469,	29470,	29473,	29475,	29476,	29477,	29481,	29482,	29483,	29485,	29500,	29501,	29503,	29504,	29505,	29508,	29513,	29515,	29524,	29532,	29533,	29534,	29535,	29537,	29549,	29553,	29556,	29561,	29574,	29618,	29634,	29635,	29637,	29639,	29665,	29666,	29668,	29669,	29672,	29682,	29693,	29709,	29710,	29711,	29717,	29741,	29742,	29746,	29747,	29752,	29753,	29755,	29756,	29759,	29804,	29805,	29832,	29998,	30003,	30005,	30006,	30007,	30009,	30019,	30025,	30040,	30074,	30075,	30077,	30078,	30080,	30082,	30083,	30084,	30290,	30291,	30293,	30349,	30350,	30351,	30352,	30353,	30354,	30358,	30376,	30392,	30424,	30426,	30589,	30590,	30591,	30613,	30614,	30615,	30616,	30617,	30619,	30627,	30628,	30647,	30954,	30958,	30985,	30986,	31316,	31317,	31331,	31334,	31336,	31357,	31358,	31359,	31360,	31497,	31501,	31502,	31503,	31504,	31526,	31527,	31528,	31882,	31883,	31884,	31890,	31891,	31892,	31893,	31894,	31929,	31966,	31970,	32153,	32498,	32520,	32583,	32618,	32683,	32769,	32780,	32788,	32847,	32848,	32857,	32872,	33058,	33148,	33153,	33255,	33275,	33279,	33300,	33513,	33519,	33520,	33521,	33522,	33524,	33525,	33527,	33528,	33534,	33578,	33579,	33580,	33581,	33582,	33584,	33585,	33586,	33587,	33589,	33591,	33593,	33594,	33599,	33600,	33602,	33619,	33634,	33655,	33753,	33845,	33846,	33866,	33868,	33869,	33871,	33873,	33883,	33888,	33890,	33891,	33907,	33926,	33931,	33933,	33934,	33936,	33972,	33973,	33978,	33987,	33988,	33989,	33990,	33991,	33992,	33993,	33997,	33998,	34000,	34001,	34007,	34015,	34050,	34058,	34081,	34082,	34085,	34086,	34089,	34091,	34092,	34095,	34260,	34265,	34293,	34294,	34295,	34296,	34297,	34309,	34315,	34316,	34320,	34346,	34399,	34419,	34461,	34462,	34463,	34464,	34465,	34469,	34503,	34527,	34590,	34816,	34827,	34845,	34846,	34849,	34852,	34853,	34863,	34941,	34971,	35015,	35020,	35134,	35136,	35144,	35156,	35206,	35221,	35264,	35285,	35292,	35294,	35295,	35296,	35299,	35300,	35301,	35309,	35311,	35315,	35321,	35323,	35324,	35328,	35329,	35330,	35331,	35332,	35342,	35343,	35347,	35351,	35356,	35357,	35386,	35415,	35428,	35440,	35459,	35467,	35471,	35474,	35529,	35562,	35575,	35634,	35637,	35646,	35655,	35663,	35691,	35704,	35732,	35733,	35744,	35835,	35853,	35881,	35884,	35887,	35889,	35893,	35894,	35896,	35897,	35898,	35899,	35900,	35901,	35902,	35907,	35909,	35910,	35917,	35918,	35920,	35921,	35923,	35926,	35928,	35929,	35930,	35939,	35941,	35943,	35944,	35948,	35949,	35950,	35951,	35953,	35954,	35957,	35979,	35997,	35998,	36000,	36018,	36021,	36023,	36089,	36093,	36098,	36099,	36102,	36105,	36111,	36136,	36154,	36172,	36173,	36175,	36193,	36200,	36210,	36223,	36225,	36226,	36229,	36230,	36233,	36239,	36240,	36241,	36242,	36244,	36246,	36247,	36248,	36249,	36258,	36264,	36267,	36269,	36370,	36433,	36437,	36469,	36479,	36480,	36481,	36504,	36515,	36520,	36521,	36529,	36530,	36550,	36584,	36599,	36600,	36608,	36614,	36666,	36674,	36685,	36707,	36717,	36736,	36743,	36756,	36760,	36775,	36784,	36785,	36787,	36804,	36830,	36843,	36844,	36850,	36854,	36860,	36870,	36874,	36875,	36876,	36877,	36879,	36952,	36958,	36979,	36980,	36991,	36996,	37050,	37051,	37058,	37092,	37093,	37111,	37117,	37120,	37123,	37137,	37142,	37147,	37148,	37149,	37150,	37151,	37152,	37170,	37176,	37187,	37190,	37192,	37193,	37198,	37201,	37205,	37209,	37217,	37221,	37226,	37227,	37231,	37242,	37244,	37255,	37266,	37319,	37324,	37352,	37365,	37375,	37415,	37429,	37448,	37450,	37452,	37495,	37518,	37519,	37569,	37570,	37572,	37573,	37576,	37597,	37608,	37627,	37676,	37677,	37735,	37743,	37748,	37749,	37750,	37751,	37756,	37758,	37766,	37767,	37792,	37801,	37805,	37807,	37808,	37812,	37828,	37834,	37835,	37838,	37840,	37841,	37842,	37843,	37844,	37845,	37846,	37849,	37850,	37852,	37854,	37863,	37866,	37873,	37877,	37880,	37881,	37883,	37897,	37900,	37908,	37927,	37996,	38008,	38081,	38085,	38091,	38092,	38161,	38183,	38187,	38195,	38200,	38282,	38292,	38300,	38302,	38303,	38309,	38314,	38316,	38317,	38321,	38360,	38368,	38374,	38382,	38398,	38399,	38402,	38403,	38410,	38411,	38420,	38429,	38431,	38439,	38452,	38464,	38467,	38483,	38499,	38500,	38514,	38515,	38530,	38533,	38547,	38548,	38556,	38558,	38559,	38560,	38561,	38563,	38564,	38565,	38566,	38567,	38568,	38569,	38571,	38574,	38575,	38578,	38619,	38635);'
    sql = 'select id from resolved_papers where downloaded = 1 and npages >= 5 and pdf2text = 1 and english = 0 and id in (12,	70,	74,	77,	92,	108,	110,	111,	113,	127,	128,	129,	133,	136,	145,	149,	151,	189,	210,	223,	238,	247,	253,	276,	287,	289,	291,	292,	303,	308,	345,	346,	347,	349,	350,	351,	354,	355,	359,	360,	361,	362,	363,	364,	365,	368,	377,	381,	389,	393,	395,	406,	414,	424,	439,	446,	448,	549,	554,	558,	574,	577,	578,	579,	581,	582,	583,	585,	588,	589,	591,	592,	595,	597,	601,	604,	605,	609,	613,	621,	625,	682,	684,	712,	713,	714,	715,	716,	717,	719,	722,	723,	724,	726,	730,	731,	732,	734,	735,	738,	739,	740,	743,	749,	751,	752,	753,	754,	755,	758,	765,	782,	787,	816,	822,	830,	836,	851,	857,	860,	861,	869,	882,	970,	1044,	1045,	1047,	1050,	1052,	1055,	1056,	1057,	1058,	1060,	1061,	1062,	1063,	1064,	1065,	1066,	1068,	1069,	1072,	1073,	1074,	1075,	1076,	1079,	1080,	1083,	1084,	1086,	1087,	1089,	1094,	1100,	1104,	1105,	1106,	1115,	1116,	1117,	1122,	1124,	1125,	1126,	1131,	1133,	1142,	1143,	1146,	1150,	1151,	1172,	1174,	1176,	1184,	1194,	1248,	1283,	1301,	1307,	1309,	1367,	1381,	1417,	1419,	1452,	1456,	1482,	1491,	1507,	1511,	1513,	1522,	1542,	1562,	1585,	1587,	1591,	1624,	1626,	1628,	1652,	1687,	1688,	1689,	1692,	1693,	1694,	1696,	1698,	1699,	1701,	1704,	1710,	1711,	1714,	1716,	1719,	1720,	1727,	1728,	1730,	1745,	1750,	1751,	1755,	1757,	1770,	1809,	1815,	1820,	1831,	1835,	1872,	1884,	1887,	1898,	1935,	1955,	1993,	2009,	2025,	2026,	2029,	2030,	2031,	2199,	2241,	2244,	2246,	2275,	2276,	2277,	2278,	2279,	2305,	2323,	2324,	2325,	2327,	2328,	2347,	2360,	2402,	2404,	2410,	2415,	2442,	2448,	2450,	2451,	2452,	2461,	2462,	2467,	2477,	2509,	2510,	2512,	2513,	2518,	2522,	2524,	2531,	2543,	2547,	2554,	2555,	2576,	2577,	2578,	2579,	2580,	2583,	2586,	2605,	2609,	2624,	2629,	2646,	2651,	2652,	2653,	2655,	2656,	2659,	2661,	2662,	2671,	2676,	2677,	2756,	2757,	2758,	2760,	2761,	2762,	2768,	2771,	2772,	2773,	2774,	2776,	2777,	2781,	2782,	2783,	2786,	2789,	2790,	2791,	2792,	2793,	2794,	2795,	2798,	2811,	2815,	2822,	2869,	2884,	2907,	2913,	2920,	2924,	3029,	3127,	3141,	3146,	3172,	3173,	3174,	3175,	3176,	3177,	3178,	3180,	3182,	3183,	3184,	3185,	3189,	3192,	3194,	3198,	3199,	3202,	3203,	3207,	3208,	3211,	3223,	3224,	3230,	3236,	3252,	3253,	3262,	3275,	3302,	3305,	3316,	3365,	3388,	3389,	3391,	3392,	3396,	3397,	3398,	3399,	3400,	3401,	3402,	3405,	3406,	3408,	3409,	3412,	3415,	3416,	3418,	3419,	3420,	3421,	3422,	3423,	3424,	3425,	3426,	3427,	3428,	3431,	3432,	3433,	3436,	3438,	3439,	3443,	3444,	3445,	3446,	3450,	3452,	3455,	3456,	3458,	3461,	3466,	3467,	3470,	3503,	3526,	3532,	3536,	3538,	3541,	3542,	3543,	3549,	3563,	3573,	3597,	3598,	3620,	3626,	3662,	3819,	3921,	3922,	3923,	3925,	3927,	3931,	3932,	3933,	3934,	3935,	3936,	3937,	3938,	3939,	3940,	3942,	3943,	3944,	3945,	3948,	3950,	3952,	3953,	3954,	3955,	3957,	3958,	3959,	3960,	3961,	3963,	3965,	3966,	3967,	3968,	3971,	3972,	3980,	3988,	3995,	4000,	4005,	4011,	4039,	4043,	4046,	4048,	4050,	4059,	4077,	4086,	4089,	4098,	4101,	4104,	4109,	4111,	4123,	4127,	4170,	4184,	4203,	4215,	4221,	4235,	4287,	4295,	4345,	4362,	4367,	4448,	4449,	4451,	4452,	4453,	4454,	4455,	4457,	4458,	4459,	4460,	4461,	4462,	4463,	4464,	4465,	4466,	4467,	4468,	4469,	4470,	4472,	4478,	4480,	4481,	4482,	4496,	4500,	4504,	4508,	4513,	4518,	4523,	4524,	4548,	4551,	4567,	4572,	4598,	4607,	4608,	4611,	4657,	4786,	4788,	4789,	4791,	4792,	4793,	4794,	4795,	4796,	4797,	4798,	4799,	4804,	4805,	4811,	4815,	4817,	4819,	4829,	4839,	4840,	5037,	5038,	5040,	5047,	5179,	5191,	5192,	5210,	5248,	5249,	5266,	5275,	5276,	5322,	5323,	5327,	5330,	5362,	5410,	5411,	5416,	5451,	5462,	5493,	5494,	5496,	5519,	5536,	5548,	5555,	5587,	5588,	5589,	5590,	5591,	5594,	5599,	5617,	5633,	5636,	5660,	5667,	5695,	5697,	5701,	5702,	5706,	5767,	5768,	5769,	5773,	5778,	5786,	5831,	5832,	5833,	5835,	5836,	5837,	5839,	5844,	5849,	5850,	5858,	5860,	5889,	5901,	5915,	5916,	5918,	5920,	5991,	5992,	5993,	5994,	5995,	6009,	6045,	6079,	6080,	6081,	6083,	6084,	6085,	6086,	6087,	6100,	6101,	6107,	6185,	6249,	6278,	6279,	6280,	6281,	6282,	6283,	6285,	6305,	6306,	6387,	6393,	6396,	6397,	6398,	6411,	6439,	6498,	6505,	6511,	6513,	6518,	6520,	6524,	6525,	6526,	6527,	6532,	6543,	6553,	6555,	6565,	6566,	6569,	6573,	6574,	6581,	6585,	6601,	6605,	6606,	6612,	6615,	6617,	6621,	6645,	6646,	6648,	6651,	6652,	6658,	6660,	6667,	6672,	6676,	6682,	6684,	6688,	6690,	6692,	6693,	6700,	6704,	6743,	6769,	6771,	6772,	6775,	6778,	6783,	6785,	6789,	6793,	6818,	6824,	6829,	6830,	6834,	6839,	6845,	6846,	6849,	6850,	6855,	6859,	6866,	6873,	6878,	6887,	6888,	6889,	6890,	6907,	6926,	6945,	6948,	6954,	6963,	7006,	7066,	7082,	7102,	7121,	7162,	7163,	7271,	7272,	7273,	7285,	7314,	7315,	7350,	7362,	7364,	7398,	7441,	7442,	7443,	7444,	7446,	7451,	7454,	7456,	7462,	7464,	7504,	7515,	7516,	7547,	7548,	7634,	7659,	7660,	7661,	7662,	7663,	7664,	7665,	7672,	7776,	7777,	7783,	7784,	7788,	7789,	7792,	7795,	7797,	7798,	7799,	7809,	7831,	7889,	7917,	7918,	7920,	7926,	7930,	7932,	7933,	7935,	7936,	7941,	7944,	7960,	7962,	7971,	8008,	8017,	8070,	8075,	8076,	8110,	8111,	8112,	8117,	8120,	8128,	8129,	8130,	8133,	8136,	8140,	8143,	8144,	8145,	8148,	8149,	8150,	8153,	8154,	8159,	8163,	8203,	8225,	8268,	8270,	8302,	8310,	8312,	8419,	8421,	8496,	8497,	8498,	8500,	8505,	8506,	8507,	8508,	8510,	8513,	8517,	8533,	8543,	8584,	8710,	8717,	8718,	8719,	8720,	8721,	8722,	8724,	8726,	8730,	8732,	8733,	8734,	8737,	8739,	8740,	8741,	8742,	8743,	8744,	8745,	8747,	8748,	8750,	8751,	8752,	8753,	8754,	8755,	8756,	8757,	8759,	8761,	8764,	8766,	8768,	8769,	8773,	8774,	8775,	8784,	8811,	8817,	9042,	9056,	9207,	9219,	9240,	9249,	9273,	9318,	9322,	9422,	9457,	9485,	9562,	9623,	9647,	9836,	9837,	9922,	10067,	10068,	10069,	10168,	10185,	10288,	10400,	10401,	10513,	10515,	10606,	10700,	10702,	10703,	10771,	10772,	10819,	10821,	10927,	11019,	11056,	11113,	11142,	11143,	11225,	11226,	11227,	11343,	11361,	11362,	11364,	11377,	11448,	11460,	11461,	11462,	11463,	11465,	11466,	11468,	11493,	11609,	11610,	11611,	11617,	11638,	11659,	11718,	11748,	11749,	11750,	11751,	11762,	11821,	11850,	11891,	11898,	11911,	11913,	11914,	11915,	11916,	11917,	11918,	11919,	11920,	11921,	11922,	11923,	11926,	11928,	11934,	11955,	11980,	12026,	12030,	12044,	12092,	12093,	12094,	12095,	12096,	12098,	12100,	12101,	12102,	12103,	12104,	12105,	12106,	12107,	12108,	12109,	12110,	12111,	12112,	12113,	12114,	12122,	12123,	12125,	12144,	12147,	12234,	12235,	12237,	12256,	12305,	12339,	12346,	12407,	12448,	12511,	12665,	12705,	12706,	12708,	12709,	12710,	12711,	12712,	12713,	12714,	12716,	12717,	12718,	12719,	12720,	12721,	12722,	12725,	12729,	12742,	12753,	12762,	12802,	12813,	12816,	12821,	12823,	12843,	12856,	12905,	12907,	13006,	13061,	13062,	13063,	13137,	13138,	13198,	13329,	13330,	13331,	13332,	13494,	13495,	13582,	13583,	13584,	13585,	13586,	13697,	13833,	13834,	13835,	13836,	13837,	13840,	14160,	14161,	14200,	14341,	14342,	14343,	14590,	14591,	14597,	14610,	14614,	14631,	14632,	14633,	14634,	14635,	14650,	14655,	14656,	14689,	14726,	14777,	14870,	14871,	14872,	14921,	14922,	14923,	14991,	14992,	14993,	14994,	14995,	15136,	15137,	15138,	15139,	15140,	15141,	15142,	15143,	15152,	15216,	15265,	15277,	15387,	15388,	15483,	15546,	15550,	15587,	15590,	15623,	15641,	15653,	15711,	15712,	15730,	15743,	15763,	15794,	15805,	15821,	15831,	15884,	15932,	16039,	16122,	16124,	16153,	16175,	16181,	16220,	16233,	16264,	16277,	16306,	16361,	16377,	16391,	16392,	16393,	16402,	16404,	16431,	16439,	16440,	16444,	16447,	16448,	16455,	16457,	16463,	16468,	16513,	16524,	16528,	16551,	16569,	16594,	16596,	16600,	16610,	16647,	16648,	16718,	16731,	16763,	16765,	16794,	16795,	16899,	16948,	16962,	16993,	16998,	17011,	17013,	17034,	17061,	17062,	17141,	17142,	17143,	17144,	17155,	17158,	17248,	17262,	17263,	17264,	17265,	17266,	17333,	17334,	17335,	17395,	17396,	17398,	17400,	17401,	17405,	17410,	17412,	17417,	17420,	17431,	17547,	17584,	17585,	17587,	17599,	17674,	17676,	17677,	17679,	17711,	17719,	17749,	17750,	17751,	17752,	17753,	17754,	17756,	17757,	17811,	17812,	17814,	17948,	17963,	17964,	17965,	17989,	17998,	18083,	18139,	18145,	18165,	18229,	18230,	18257,	18264,	18273,	18321,	18322,	18323,	18351,	18515,	18548,	18599,	18600,	18623,	18637,	18675,	18676,	18687,	18698,	18736,	18753,	18768,	18792,	18794,	18797,	18823,	18828,	18830,	18850,	18851,	18853,	18854,	18857,	18882,	18885,	18886,	18887,	18888,	18891,	18892,	18893,	18894,	18898,	18901,	18904,	18930,	18947,	18967,	18968,	18970,	18972,	18973,	18974,	18976,	18977,	18980,	18982,	18983,	18984,	18985,	18986,	18991,	19006,	19059,	19060,	19061,	19062,	19064,	19066,	19067,	19069,	19071,	19103,	19104,	19110,	19116,	19153,	19180,	19181,	19186,	19263,	19272,	19273,	19280,	19318,	19409,	19425,	19428,	19456,	19528,	19531,	19538,	19606,	19607,	19609,	19610,	19612,	19613,	19616,	19623,	19636,	19647,	19648,	19685,	19798,	19799,	19800,	19801,	19802,	19805,	19806,	19807,	19808,	19811,	19812,	19813,	19816,	19820,	19821,	19836,	19874,	19875,	19878,	19960,	19985,	20051,	20052,	20053,	20054,	20055,	20056,	20057,	20058,	20059,	20061,	20062,	20063,	20064,	20065,	20066,	20069,	20070,	20071,	20072,	20074,	20078,	20079,	20081,	20084,	20088,	20090,	20110,	20156,	20157,	20168,	20189,	20193,	20245,	20344,	20345,	20346,	20347,	20348,	20349,	20350,	20353,	20354,	20355,	20356,	20357,	20358,	20359,	20360,	20361,	20362,	20363,	20365,	20368,	20370,	20371,	20373,	20374,	20377,	20391,	20392,	20396,	20398,	20400,	20444,	20476,	20520,	20682,	20685,	20687,	20688,	20689,	20690,	20691,	20692,	20693,	20694,	20695,	20698,	20699,	20700,	20701,	20702,	20703,	20707,	20709,	20714,	20728,	20760,	20774,	20864,	20865,	20866,	20867,	20868,	20869,	20870,	20872,	20874,	20899,	20909,	20962,	21041,	21042,	21117,	21118,	21121,	21139,	21146,	21227,	21271,	21272,	21273,	21274,	21275,	21425,	21430,	21493,	21505,	21507,	21510,	21513,	21612,	21616,	21621,	21622,	21623,	21624,	21667,	21675,	21751,	21765,	21766,	21767,	21846,	21847,	21856,	21857,	21858,	21871,	21872,	21873,	21875,	21876,	21877,	21881,	21883,	21885,	21924,	21925,	21957,	21977,	21978,	21979,	21980,	21984,	21985,	21993,	21997,	21999,	22001,	22031,	22033,	22082,	22113,	22175,	22228,	22247,	22271,	22272,	22371,	22374,	22462,	22463,	22613,	22694,	22695,	22696,	22697,	22700,	22880,	22881,	22882,	22883,	22884,	22901,	22977,	22978,	22979,	22981,	23030,	23032,	23191,	23230,	23236,	23238,	23291,	23340,	23453,	23552,	23553,	23744,	23761,	23774,	24016,	24025,	24037,	24085,	24090,	24096,	24125,	24126,	24128,	24129,	24130,	24132,	24133,	24140,	24141,	24142,	24145,	24150,	24151,	24152,	24153,	24155,	24168,	24169,	24170,	24171,	24172,	24173,	24174,	24181,	24186,	24187,	24189,	24190,	24192,	24193,	24206,	24207,	24208,	24209,	24210,	24211,	24212,	24213,	24214,	24239,	24243,	24244,	24246,	24247,	24249,	24250,	24251,	24252,	24253,	24254,	24255,	24256,	24257,	24258,	24261,	24290,	24297,	24298,	24299,	24300,	24301,	24302,	24303,	24304,	24305,	24307,	24308,	24315,	24326,	24330,	24334,	24335,	24336,	24350,	24364,	24365,	24366,	24367,	24368,	24371,	24372,	24390,	24391,	24393,	24405,	24406,	24408,	24411,	24412,	24413,	24415,	24438,	24439,	24440,	24473,	24474,	24476,	24477,	24478,	24479,	24480,	24481,	24483,	24484,	24485,	24486,	24487,	24520,	24522,	24523,	24524,	24525,	24526,	24527,	24528,	24529,	24530,	24531,	24532,	24533,	24535,	24536,	24537,	24540,	24541,	24542,	24543,	24544,	24545,	24546,	24547,	24549,	24550,	24576,	24586,	24621,	24622,	24623,	24624,	24625,	24626,	24627,	24628,	24629,	24630,	24631,	24632,	24633,	24634,	24635,	24636,	24637,	24638,	24639,	24640,	24641,	24642,	24644,	24645,	24646,	24647,	24648,	24651,	24652,	24653,	24654,	24655,	24656,	24657,	24712,	24713,	24714,	24715,	24716,	24717,	24719,	24720,	24721,	24722,	24723,	24724,	24731,	24775,	24795,	24812,	24831,	24833,	24835,	24836,	24845,	24846,	24851,	24869,	24877,	24888,	24889,	24907,	24926,	24952,	25091,	25169,	25177,	25178,	25195,	25206,	25247,	25248,	25251,	25267,	25340,	25345,	25455,	25456,	25460,	25464,	25754,	25822,	25845,	25865,	25890,	25891,	25893,	25914,	25975,	25976,	25978,	25980,	25982,	25986,	25996,	26003,	26074,	26112,	26143,	26172,	26182,	26183,	26186,	26194,	26202,	26283,	26284,	26287,	26289,	26293,	26303,	26316,	26320,	26322,	26463,	26465,	26467,	26469,	26476,	26481,	26486,	26489,	26497,	26596,	26663,	26678,	26717,	27136,	27183,	27307,	27340,	27341,	27342,	27344,	27348,	27355,	27607,	27608,	27609,	27610,	27623,	27635,	27641,	27922,	27937,	28165,	28263,	28277,	28422,	28433,	28437,	28508,	28738,	28739,	28740,	28743,	28748,	28820,	28990,	28993,	28997,	29008,	29009,	29010,	29011,	29079,	29084,	29090,	29093,	29101,	29102,	29104,	29105,	29106,	29112,	29113,	29114,	29119,	29120,	29122,	29123,	29124,	29125,	29129,	29130,	29133,	29134,	29135,	29137,	29139,	29146,	29147,	29172,	29174,	29176,	29184,	29191,	29192,	29194,	29200,	29201,	29203,	29221,	29224,	29225,	29226,	29232,	29234,	29258,	29265,	29268,	29273,	29274,	29275,	29276,	29277,	29278,	29280,	29281,	29282,	29300,	29301,	29302,	29310,	29313,	29314,	29315,	29316,	29320,	29382,	29435,	29436,	29454,	29457,	29458,	29468,	29469,	29470,	29473,	29475,	29476,	29477,	29481,	29482,	29483,	29485,	29500,	29501,	29503,	29504,	29505,	29508,	29513,	29515,	29524,	29532,	29533,	29534,	29535,	29537,	29549,	29553,	29556,	29561,	29574,	29618,	29634,	29635,	29637,	29639,	29665,	29666,	29668,	29669,	29672,	29682,	29693,	29709,	29710,	29711,	29717,	29741,	29742,	29746,	29747,	29752,	29753,	29755,	29756,	29759,	29804,	29805,	29832,	29998,	30003,	30005,	30006,	30007,	30009,	30019,	30025,	30040,	30074,	30075,	30077,	30078,	30080,	30082,	30083,	30084,	30290,	30291,	30293,	30349,	30350,	30351,	30352,	30353,	30354,	30358,	30376,	30392,	30424,	30426,	30589,	30590,	30591,	30613,	30614,	30615,	30616,	30617,	30619,	30627,	30628,	30647,	30954,	30958,	30985,	30986,	31316,	31317,	31331,	31334,	31336,	31357,	31358,	31359,	31360,	31497,	31501,	31502,	31503,	31504,	31526,	31527,	31528,	31882,	31883,	31884,	31890,	31891,	31892,	31893,	31894,	31929,	31966,	31970,	32153,	32498,	32520,	32583,	32618,	32683,	32769,	32780,	32788,	32847,	32848,	32857,	32872,	33058,	33148,	33153,	33255,	33275,	33279,	33300,	33513,	33519,	33520,	33521,	33522,	33524,	33525,	33527,	33528,	33534,	33578,	33579,	33580,	33581,	33582,	33584,	33585,	33586,	33587,	33589,	33591,	33593,	33594,	33599,	33600,	33602,	33619,	33634,	33655,	33753,	33845,	33846,	33866,	33868,	33869,	33871,	33873,	33883,	33888,	33890,	33891,	33907,	33926,	33931,	33933,	33934,	33936,	33972,	33973,	33978,	33987,	33988,	33989,	33990,	33991,	33992,	33993,	33997,	33998,	34000,	34001,	34007,	34015,	34050,	34058,	34081,	34082,	34085,	34086,	34089,	34091,	34092,	34095,	34260,	34265,	34293,	34294,	34295,	34296,	34297,	34309,	34315,	34316,	34320,	34346,	34399,	34419,	34461,	34462,	34463,	34464,	34465,	34469,	34503,	34527,	34590,	34816,	34827,	34845,	34846,	34849,	34852,	34853,	34863,	34941,	34971,	35015,	35020,	35134,	35136,	35144,	35156,	35206,	35221,	35264,	35285,	35292,	35294,	35295,	35296,	35299,	35300,	35301,	35309,	35311,	35315,	35321,	35323,	35324,	35328,	35329,	35330,	35331,	35332,	35342,	35343,	35347,	35351,	35356,	35357,	35386,	35415,	35428,	35440,	35459,	35467,	35471,	35474,	35529,	35562,	35575,	35634,	35637,	35646,	35655,	35663,	35691,	35704,	35732,	35733,	35744,	35835,	35853,	35881,	35884,	35887,	35889,	35893,	35894,	35896,	35897,	35898,	35899,	35900,	35901,	35902,	35907,	35909,	35910,	35917,	35918,	35920,	35921,	35923,	35926,	35928,	35929,	35930,	35939,	35941,	35943,	35944,	35948,	35949,	35950,	35951,	35953,	35954,	35957,	35979,	35997,	35998,	36000,	36018,	36021,	36023,	36089,	36093,	36098,	36099,	36102,	36105,	36111,	36136,	36154,	36172,	36173,	36175,	36193,	36200,	36210,	36223,	36225,	36226,	36229,	36230,	36233,	36239,	36240,	36241,	36242,	36244,	36246,	36247,	36248,	36249,	36258,	36264,	36267,	36269,	36370,	36433,	36437,	36469,	36479,	36480,	36481,	36504,	36515,	36520,	36521,	36529,	36530,	36550,	36584,	36599,	36600,	36608,	36614,	36666,	36674,	36685,	36707,	36717,	36736,	36743,	36756,	36760,	36775,	36784,	36785,	36787,	36804,	36830,	36843,	36844,	36850,	36854,	36860,	36870,	36874,	36875,	36876,	36877,	36879,	36952,	36958,	36979,	36980,	36991,	36996,	37050,	37051,	37058,	37092,	37093,	37111,	37117,	37120,	37123,	37137,	37142,	37147,	37148,	37149,	37150,	37151,	37152,	37170,	37176,	37187,	37190,	37192,	37193,	37198,	37201,	37205,	37209,	37217,	37221,	37226,	37227,	37231,	37242,	37244,	37255,	37266,	37319,	37324,	37352,	37365,	37375,	37415,	37429,	37448,	37450,	37452,	37495,	37518,	37519,	37569,	37570,	37572,	37573,	37576,	37597,	37608,	37627,	37676,	37677,	37735,	37743,	37748,	37749,	37750,	37751,	37756,	37758,	37766,	37767,	37792,	37801,	37805,	37807,	37808,	37812,	37828,	37834,	37835,	37838,	37840,	37841,	37842,	37843,	37844,	37845,	37846,	37849,	37850,	37852,	37854,	37863,	37866,	37873,	37877,	37880,	37881,	37883,	37897,	37900,	37908,	37927,	37996,	38008,	38081,	38085,	38091,	38092,	38161,	38183,	38187,	38195,	38200,	38282,	38292,	38300,	38302,	38303,	38309,	38314,	38316,	38317,	38321,	38360,	38368,	38374,	38382,	38398,	38399,	38402,	38403,	38410,	38411,	38420,	38429,	38431,	38439,	38452,	38464,	38467,	38483,	38499,	38500,	38514,	38515,	38530,	38533,	38547,	38548,	38556,	38558,	38559,	38560,	38561,	38563,	38564,	38565,	38566,	38567,	38568,	38569,	38571,	38574,	38575,	38578,	38619,	38635);'
    print(sql)
    papers = pd.read_sql(sql, con=db)

    for index, row in papers.iterrows():

        lang = None
        id = row[0]
        english = 0
        other = 0
        text = ""
        res = ""
        print (id)
        if id:

            # with open(os.path.join('data/txt', str(id) + '.txt')) as infile:
            with open(os.path.join('/Volumes/SeagateBackupPlusDrive/CLPD2019_FULL/txt', str(id) + '.txt')) as infile:
                for line in infile:
                    if not re.match(r'^\s*$', line):
                        line = re.sub(r"-\n", "", line)
                        line = re.sub(r"\n", " ", line)
                        text += line
                infile.close()
            lenText = len(text)

            nrequest = round(float(lenText) / 5000)
            count = 1
            while count <= nrequest:
                res = ''
                content = ""

                posIni = (count * 5000) - 5000
                posFin = (count * 5000) - 1

                content += text[posIni:posFin]
                try:
                    translator = Translator(random.choice(key_choices))
                    res = translator.detect_lang([content])

                except:
                    pass
                if res:
                    if res == 'en':
                        english += 1
                    else:
                        other += 1
                count += 1
            if english > other:
                lang = "English"
                sql = "update resolved_papers set english = 1 where id = %s" % (id)
            else:
                lang = "Other"
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
        print("Id: %s. Language: %s" % (id, lang))
    print("Done!")