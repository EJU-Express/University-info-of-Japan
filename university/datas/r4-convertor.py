import json


def data_format(d, uni_type):
    print(d)

    def d_table(table):
        for tb in d['tables']:
            if table == tb['table']:
                return tb['datas']
        else:
            print("Table not found:", table)
            return None

    print("Table test", d_table("学校基本情報"))

    # ＝＝＝　基本情報　＝＝＝

    # ～学長任期～
    term_of_president__start = d_table("学校基本情報")['rows'][0][2]
    term_of_president__end = d_table("学校基本情報")['rows'][0][4]

    # 学校基本情報　長さは欠けた場合
    if len(d_table("学校基本情報")['rows'][0]) != 7:
        # また生きている学長の時代
        the_era_of_the_president_who_still_alive = ["大正", "昭和", "平成", "令和"]

        for era in the_era_of_the_president_who_still_alive:
            if era in term_of_president__end:
                term_of_president__end = term_of_president__end
                break
        else:
            term_of_president__end = ""

    term_of_president = f"{term_of_president__start}～{term_of_president__end}"

    # ～住所～
    address = f"〒{d_table("学校基本情報")['rows'][0][-3]} {d_table("学校基本情報")['rows'][0][-2]}"

    # ＝＝＝　学部　＝＝＝
    gakubu_list = []
    gakubu_tb = d_table('学部')
    gakubu_cols = gakubu_tb["cols"]

    # delete ['昼間', '夜間', '計', '2年次', '3年次', '4年次', '2年次', '3年次']
    gakubu_rows = gakubu_tb["rows"] if "部" in gakubu_tb["rows"][0] else gakubu_tb["rows"][1:]

    for row in gakubu_rows:
        if len(row) < 4:
            row.extend([None] * (4 - len(row)))

        gakubu_list.append({
            'name': row[0],
            'major': row[1],
            'pref': row[2],
            'city': row[3]
        })

    # ＝＝＝　研究科　＝＝＝
    kennkyuka_list = []
    kennkyuka_tb = d_table('研究科')
    kennkyuka_cols = kennkyuka_tb["cols"]
    kennkyuka_rows = kennkyuka_tb["rows"]

    for row in kennkyuka_rows:
        print(row)
        if len(row) < 4:
            row.extend([None] * (4 - len(row)))

        # Delete ["入学定員", "修業年限", "入学定員", "修業年限", "入学定員", "修業年限", "入学定員", "修業年限"]
        if row[0] == "入学定員":
            continue

        if row[4] is not None and isinstance(row[4], str) and any(char in ["昼", "夜"] for char in row[4]):
            day_night = row[4]
        else:
            day_night = None

        kennkyuka_list.append({
            'name': row[0],
            'major': row[1],
            'pref': row[2],
            'city': row[3],
            'day_night': day_night
        })

    # ＝＝＝　共同実施制度利用（学部）　＝＝＝
    UJIS_F_list = []
    UJIS_F_tb = d_table('共同実施制度利用（学部）')
    UJIS_F_cols = UJIS_F_tb["cols"]
    UJIS_F_rows = UJIS_F_tb["rows"]

    for row in UJIS_F_rows:
        if len(row) < 2:
            row.extend([None] * (2 - len(row)))

        # Delete ["入学定員", "修業年限", "入学定員", "修業年限", "入学定員", "修業年限", "入学定員", "修業年限"]
        if row[0] == "入学定員":
            continue

        UJIS_F_list.append({
            'name': row[0],
            'master': row[1],
        })

    # ＝＝＝　共同実施制度利用（研究科）　＝＝＝
    UJIS_G_list = []
    UJIS_G_tb = d_table('共同実施制度利用（研究科）')
    UJIS_G_cols = UJIS_G_tb["cols"]
    UJIS_G_rows = UJIS_G_tb["rows"]

    for row in UJIS_G_rows:
        if len(row) < 2:
            row.extend([None] * (2 - len(row)))

        UJIS_G_list.append({
            'name': row[0],
            'master': row[1],
        })

    # ＝＝＝　学部・研究科所在地（キャンパス名など）　＝＝＝
    campus_list = []
    campus_tb = d_table('学部・研究科所在地（キャンパス名など）')
    campus_cols = campus_tb["cols"]
    campus_rows = campus_tb["rows"]

    for row in campus_rows:
        if len(row) < 4:
            row.extend([None] * (4 - len(row)))

        campus_list.append({
            'name': row[0],
            'post': row[1],
            'addr': row[2],
            'tel': row[3],
        })

    # ＝＝＝　学部沿革　＝＝＝
    history_F_list = []
    history_F_tb = d_table('学部沿革')
    history_F_cols = history_F_tb["cols"]
    history_F_rows = history_F_tb["rows"]

    for row in history_F_rows:
        if len(row) < 2:
            row.extend([None] * (2 - len(row)))

        history_F_list.append({
            'date': row[0],
            'detail': row[1],
        })

    # ＝＝＝　大学院沿革　＝＝＝
    history_G_list = []
    history_G_tb = d_table('大学院沿革')
    history_G_cols = history_G_tb["cols"]
    history_G_rows = history_G_tb["rows"]

    for row in history_G_rows:
        if len(row) < 2:
            row.extend([None] * (2 - len(row)))

        history_G_list.append({
            'date': row[0],
            'detail': row[1],
        })

    return {
        "name": d['name'].replace(" ", "　"),
        "name_eng": d['name_eng'].replace("　", ""),
        "type": uni_type,

        "mext_code": d_table("学校基本情報")['rows'][0][0],
        "president": d_table("学校基本情報")['rows'][0][1],
        "term_president": term_of_president,
        "addr": address,
        "tel": d_table("学校基本情報")['rows'][0][-1],

        "faculty": {
            "name": "学部",
            "rows": gakubu_list
        },

        "graduate_course": {
            "name": "研究科",
            "rows": kennkyuka_list
        },

        "UJIS-F": {
            "table": "共同実施制度利用（学部）",
            "rows": UJIS_F_list
        },
        "UJIS-G": {
            "name": "共同実施制度利用（研究科）",
            "rows": UJIS_G_list
        },

        # "IANU": {
        #     "name": "国立大学附置研究所附属施設",
        #     "rows": [
        #         {
        #             "附置研究所名": "低温科学研究所",
        #             "附属施設": "環オホーツク観測研究センター",
        #             "所在地住所": "〒060-0819 北海道札幌市北区北19条西8丁目",
        #             "電話番号": "011-716-2111"
        #         }
        #     ]
        # },
        # "RINU": {
        #     "name": "国立大学附置研究所",
        #     "rows": [
        #         {
        #             "附置研究所名": "＊低温科学研究所",
        #             "所在地住所": "〒060-0819 北海道札幌市北区北19条西8丁目",
        #             "電話番号": "011-716-2111",
        #             "設置年月日": "昭和16年11月25日",
        #             "備考": ""
        #         }
        #     ]
        # },
        #
        "History-F": {
            "name": "学部沿革",
            "rows": history_F_list
        },

        "History-G": {
            "name": "大学院沿革",
            "rows": history_G_list
        },

        "campus": {
            "name": "学部・研究科所在地（キャンパス名など）",
            "rows": campus_list,

        },
    }


if __name__ == '__main__':
    filelist = [
        ["20230420_mxt_daigakuc01_000230747_01.xlsx.json", "国立"],
        ["20230420_mxt_daigakuc01_000230747_02.xlsx.json", "公立"],
        ["20230420_mxt_daigakuc01_000230747_03-1.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-2.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-3.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-4.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-5.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-6.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-7.xlsx.json", "私立"],
        ["20230420_mxt_daigakuc01_000230747_03-8.xlsx.json", "私立"]
    ]

    unis = []

    for file in filelist:
        with open(f'../mext_original/r4/{file[0]}', 'r', encoding='utf-8') as f:
            unis_j = json.loads(f.read())  # 大学リスト　JSON

        for uni in unis_j:
            unis.append(data_format(uni, file[1]))

    with open('./r4-university-info.json', 'w', encoding='utf-8') as s:
        json.dump(unis, s, ensure_ascii=False)
