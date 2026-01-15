import streamlit as st
import operator
import pandas as pd

# --- 1. データ定義: タイプの構造（各機能のポジション） ---
# モデルAに基づき、各タイプの機能ポジションを定義
# P1:主導, P2:創造, P5:暗示, P6:動員 (これらがValued)
# --- 1. データ定義: モデルA 全ポジション (P1〜P8) ---
# [P1, P2, P3, P4, P5, P6, P7, P8] の順に格納
model_a_data = {
    "ILE (ENTp)": ["Ne", "Ti", "Se", "Fi", "Si", "Fe", "Ni", "Te"],
    "SEI (ISFp)": ["Si", "Fe", "Te", "Ni", "Ne", "Ti", "Se", "Fi"],
    "ESE (ESFj)": ["Fe", "Si", "Ne", "Ti", "Ti", "Ne", "Fi", "Se"],
    "LII (INTj)": ["Ti", "Ne", "Si", "Fe", "Fe", "Si", "Te", "Ni"],
    "EIE (ENFj)": ["Fe", "Ni", "Se", "Ti", "Ti", "Se", "Fi", "Ni"],
    "LSI (ISTj)": ["Ti", "Se", "Ni", "Fe", "Fe", "Ni", "Te", "Se"],
    "SLE (ESTp)": ["Se", "Ti", "Fe", "Ni", "Ni", "Fe", "Si", "Ti"],
    "IEI (INFp)": ["Ni", "Fe", "Ti", "Se", "Se", "Ti", "Ne", "Fe"],
    "SEE (ESFp)": ["Se", "Fi", "Te", "Ni", "Ni", "Te", "Si", "Fi"],
    "ILI (INTp)": ["Ni", "Te", "Fi", "Se", "Se", "Fi", "Ne", "Te"],
    "LIE (ENTj)": ["Te", "Ni", "Se", "Fi", "Fi", "Se", "Ti", "Ni"],
    "ESI (ISFj)": ["Fi", "Se", "Ni", "Te", "Te", "Ni", "Fe", "Se"],
    "LSE (ESTj)": ["Te", "Si", "Ne", "Fi", "Fi", "Ne", "Ti", "Si"],
    "EII (INFj)": ["Fi", "Ne", "Si", "Te", "Te", "Si", "Fe", "Ne"],
    "IEE (ENFp)": ["Ne", "Fi", "Te", "Si", "Si", "Te", "Ni", "Fi"],
    "SLI (ISTp)": ["Si", "Te", "Fi", "Ne", "Ne", "Fi", "Se", "Te"],
}

# 診断ロジック用に「価値機能(P1,P2,P5,P6)」だけを抽出した辞書を作る
socionics_structure = {k: {"P1": v[0], "P2": v[1], "P5": v[4], "P6": v[5]} for k, v in model_a_data.items()}

soci_to_mbti = {k: v for k, v in zip(socionics_structure.keys(), 
    ["ENTP", "ISFJ", "ESFJ", "INTP", "ENFJ", "ISTP", "ESTP", "INFJ", "ESFP", "INTJ", "ENTJ", "ISFP", "ESTJ", "INFP", "ENFP", "ISTJ"])}

# 質問リスト: 「能力」ではなく「価値（Valued/Unvalued）」を問う内容
questions = [
    {"id": 1, "func": "Ti", "text": "物事の論理的な整合性や、分類・体系化を考えるのが好きだ。"},
    {"id": 2, "func": "Ti", "text": "感情に流されず、客観的な法則に基づいて判断を下すべきだと思う。"},
    {"id": 3, "func": "Ti", "text": "複雑な仕組みを解き明かし、矛盾のない理論を構築することに達成感を感じる。"},
    {"id": 4, "func": "Ti", "text": "「なぜそうなるのか」という論理的な理由が不明確だと、納得がいかない。"},
    
    {"id": 5, "func": "Te", "text": "効率性や生産性を高めるための具体的な方法を知ることに興味がある。"},
    {"id": 6, "func": "Te", "text": "理論よりも、実際に役立つ知識やエビデンス（証拠）を重視する。"},
    {"id": 7, "func": "Te", "text": "無駄なプロセスを省き、最短ルートで成果を出すことに喜びを感じる。"},
    {"id": 8, "func": "Te", "text": "プロジェクトの進捗やコスト、実用的なリソースの管理が得意だと思う。"},
    
    {"id": 9, "func": "Fi", "text": "自分自身の誠実さや、個人的な好き嫌いの感覚を大切にしている。"},
    {"id": 10, "func": "Fi", "text": "表面的な付き合いより、少人数の相手との深い信頼関係を重視したい。"},
    {"id": 11, "func": "Fi", "text": "道徳的な正しさや、自分なりの価値基準を守って生きたいと思う。"},
    {"id": 12, "func": "Fi", "text": "人との心理的な距離感に敏感で、自分がどう感じるかを大事にする。"},
    
    {"id": 13, "func": "Fe", "text": "場の空気を盛り上げたり、人々の感情をポジティブに動かしたりしたい。"},
    {"id": 14, "func": "Fe", "text": "感情表現が豊かで、喜びや感動を周りの人と共有するのが好きだ。"},
    {"id": 15, "func": "Fe", "text": "グループの結束力を高め、活気ある雰囲気を維持することに価値を感じる。"},
    {"id": 16, "func": "Fe", "text": "他人の情熱や熱気を受けて、自分もエネルギーが湧いてくることが多い。"},

    {"id": 17, "func": "Si", "text": "心身の健康や、穏やかでリラックスした生活環境を整えることが大切だ。"},
    {"id": 18, "func": "Si", "text": "美味しい食事や快適な空間など、五感で感じる心地よさを追求したい。"},
    {"id": 19, "func": "Si", "text": "過度な緊張やストレスを避け、心身の調和が取れている状態を維持したい。"},
    {"id": 20, "func": "Si", "text": "身近な人たちの体調や、環境の細かな変化に気づき、ケアをすることに意味を感じる。"},
    
    {"id": 21, "func": "Se", "text": "目標を達成するために、強い意志を持って周囲に影響を及ぼすことが好きだ。"},
    {"id": 22, "func": "Se", "text": "困難な壁に突き当たったとき、自分の力でそれを突破することに快感を覚える。"},
    {"id": 23, "func": "Se", "text": "勝負事や競争において、勝利を勝ち取ることへの意欲が強い方だ。"},
    {"id": 24, "func": "Se", "text": "決断力を持って即座に行動し、現実の世界を動かしている感覚を求めている。"},
    
    {"id": 25, "func": "Ni", "text": "物事の長期的な展望や、将来に向けた大きな流れを予測することに惹かれる。"},
    {"id": 26, "func": "Ni", "text": "シンボルや隠された意味、一つの点から繋がる深いビジョンについて考えるのが好きだ。"},
    {"id": 27, "func": "Ni", "text": "急ぐことよりも、物事の「適切なタイミング」を待つことの重要性を理解している。"},
    {"id": 28, "func": "Ni", "text": "人生の目的や歴史のうねりなど、抽象的で精神的なテーマに価値を感じる。"},
    
    {"id": 29, "func": "Ne", "text": "新しいアイデアや可能性を思いついたとき、非常にワクワクする。"},
    {"id": 30, "func": "Ne", "text": "現状に満足せず、常に面白そうな選択肢や新しいチャンスを探し続けていたい。"},
    {"id": 31, "func": "Ne", "text": "型にはまらない斬新な発想や、多面的な視点を持つ人を尊敬する。"},
    {"id": 32, "func": "Ne", "text": "知的好奇心が旺盛で、未知の世界を探求すること自体に喜びを感じる。"},
]

# --- 2. 診断ロジック ---
def calculate_diagnosis(answers):
    # スコアマップ (1-5点を -2 ~ 2に変換)
    score_map = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}
    func_raw_scores = {f: 0 for f in ["Ti", "Te", "Fi", "Fe", "Si", "Se", "Ni", "Ne"]}
    
    for q in questions:
        func_raw_scores[q["func"]] += score_map.get(answers.get(q["id"], 3), 0)

    type_scores = {}
    for t_name, pos in socionics_structure.items():
        # ポジションによる重み付け
        # P1(主導): 4倍, P2(創造): 3倍, P6(動員): 2倍, P5(暗示): 1.5倍
        score = (func_raw_scores[pos["P1"]] * 4.0 + 
                 func_raw_scores[pos["P2"]] * 3.0 + 
                 func_raw_scores[pos["P6"]] * 2.0 + 
                 func_raw_scores[pos["P5"]] * 1.5)
        
        # 非価値機能への反発（他の4つの機能）
        unvalued = [f for f in ["Ti", "Te", "Fi", "Fe", "Si", "Se", "Ni", "Ne"] 
                    if f not in pos.values()]
        score -= sum(func_raw_scores[f] for f in unvalued) * 2.0
        
        type_scores[t_name] = round(score, 1)

    sorted_types = sorted(type_scores.items(), key=operator.itemgetter(1), reverse=True)
    return {
        "socionics": sorted_types[0][0],
        "mbti_equiv": soci_to_mbti[sorted_types[0][0]],
        "scores": func_raw_scores,
        "ranking": sorted_types[:5]
    }

# --- 3. UI ---
st.set_page_config(page_title="ソシオニクス診断", layout="centered")

st.title("(ΦωΦ) ソシオニクス診断")
st.write("価値非価値の要素をベースとした診断を行います")

# 解説タブの設置
desc_tab1, desc_tab2 = st.tabs(["💡 ソシオニクスとは？", "心理機能の解説"])

with desc_tab1:
    st.markdown("""
    モデルA：心の仕組み\n
    ソシオニクスでは、人間の心を8つの「ポジション」で考えます。\n
    主導機能 (P1):その人の核となる価値観です。息を吸うように自然に使える強みでもあり、こだわる領域でもあります。\n
    創造機能 (P2):主機能の目的を達成する道具であり、非常に器用です。他者とのコミュニケーションや問題解決に積極的に活用されます。\n
    役割機能 (P3):ある程度はこなせますが、長時間使うと非常に疲れます。自信はなく、あくまで社会に適応するために必要に迫られて使います。\n
    脆弱機能 (P4):意識していますが上手く扱えず、他人から強要されると動揺したり、拒絶反応を示すこともあります。\n
    暗示機能 (P5):自分ではほとんど使えませんが、この要素を持っている人に強く惹かれます。\n
    活性化機能 (P6):自分で得意になりたいと努力する部分です。ここが刺激されるとやる気が湧いてきます。\n
    無視機能 (P7):P1と同じくらい強い能力を持っていますが、価値を感じにくく、意図的に無視されます。\n
    示範機能 (P8):非常に強い機能ですが、当たり前すぎて意識しません。
    
    価値機能 (Valued):P1, P2, P5, P6。これらを共有する人とは意気投合しやすいと言われています（クアドラ）。
    
    ---
    この診断では、あなたがどの要素を大切にしたいか（価値）に基づき、モデルAの構造に当てはめて判定しています。
    """)

with desc_tab2:
    st.markdown("""
    ### 8つの情報要素
    | 要素 | 意味 | 大切にする価値観 |
    | :--- | :--- | :--- |
    | Ti | 内向論理 | 矛盾のない体系、ルール、公平な構造 |
    | Te | 外向論理 | 実用的な効率、データ、無駄のない改善 |
    | Fi | 内向倫理 | 個人的な絆、心の誠実さ、深い信頼 |
    | Fe | 外向倫理 | 感情の熱気、場の盛り上がり、情熱の共有 |
    | Si | 内向感覚 | 心身の快適さ、五感の調和、リラックス |
    | Se | 外向感覚 | 意志の強さ、現実を動かす力、直接的影響 |
    | Ni | 内向直感 | 将来の展望、隠れた意味、時の流れ |
    | Ne | 外向直感 | 未知の可能性、新しいアイデア、多角的な視点 |
    """)

st.divider()

user_answers = {}
for q in questions:
    st.markdown(f"#### {q['text']}")
    user_answers[q["id"]] = st.radio(
        label=f"q_{q['id']}",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {1: "全くそう思わない", 2: "そう思わない", 3: "どちらでもない", 4: "そう思う", 5: "非常にそう思う"}[x],
        horizontal=True,
        key=f"radio_{q['id']}",
        label_visibility="collapsed"
    )
    st.write("") # スペース用

if st.button("診断結果を算出", type="primary", use_container_width=True):
    res = calculate_diagnosis(user_answers)
    st.success("分析が完了しました。")
    st.header(f"結果: {res['socionics']}")

    # --- モデルAの表示ブロック ---
    st.divider()
    st.subheader("あなたのモデルA構造")
    
    # ここで先ほど定義した model_a_data を呼び出します
    funcs = model_a_data[res['socionics']]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**P1 (主導): {funcs[0]}**")
        st.warning(f"**P3 (役割): {funcs[2]}**")
        st.success(f"**P5 (暗示): {funcs[4]}**")
        st.error(f"**P7 (無視): {funcs[6]}**")
    with col_b:
        st.info(f"**P2 (創造): {funcs[1]}**")
        st.warning(f"**P4 (脆弱): {funcs[3]}**")
        st.success(f"**P6 (動員): {funcs[5]}**")
        st.error(f"**P8 (証明): {funcs[7]}**")

    st.caption("🟦 Ego (P1,P2) / 🟨 Super-Ego (P3,P4) / 🟩 Super-ID (P5,P6) / 🟥 Id (P7,P8)")

    # 最後にランキングとグラフを表示
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🥇 適合ランキング")
        for i, (name, score) in enumerate(res['ranking']):
            st.write(f"{i+1}. {name} : {score}点")
    with col2:
        st.write("### 機能別価値スコア")
        df = pd.DataFrame([res['scores']]).T.reset_index()
        df.columns = ["機能", "スコア"]
        st.bar_chart(df.set_index("機能"))
