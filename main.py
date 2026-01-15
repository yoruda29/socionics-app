import streamlit as st
import operator
import pandas as pd

# --- 1. データ定義: タイプの構造（各機能のポジション） ---
# モデルAに基づき、各タイプの機能ポジションを定義
# P1:主導, P2:創造, P5:暗示, P6:動員 (これらがValued)
socionics_structure = {
    "ILE (ENTp)": {"P1": "Ne", "P2": "Ti", "P5": "Si", "P6": "Fe"},
    "SEI (ISFp)": {"P1": "Si", "P2": "Fe", "P5": "Ne", "P6": "Ti"},
    "ESE (ESFj)": {"P1": "Fe", "P2": "Si", "P5": "Ti", "P6": "Ne"},
    "LII (INTj)": {"P1": "Ti", "P2": "Ne", "P5": "Fe", "P6": "Si"},
    "EIE (ENFj)": {"P1": "Fe", "P2": "Ni", "P5": "Ti", "P6": "Se"},
    "LSI (ISTj)": {"P1": "Ti", "P2": "Se", "P5": "Fe", "P6": "Ni"},
    "SLE (ESTp)": {"P1": "Se", "P2": "Ti", "P5": "Ni", "P6": "Fe"},
    "IEI (INFp)": {"P1": "Ni", "P2": "Fe", "P5": "Se", "P6": "Ti"},
    "SEE (ESFp)": {"P1": "Se", "P2": "Fi", "P5": "Ni", "P6": "Te"},
    "ILI (INTp)": {"P1": "Ni", "P2": "Te", "P5": "Se", "P6": "Fi"},
    "LIE (ENTj)": {"P1": "Te", "P2": "Ni", "P5": "Fi", "P6": "Se"},
    "ESI (ISFj)": {"P1": "Fi", "P2": "Se", "P5": "Te", "P6": "Ni"},
    "LSE (ESTj)": {"P1": "Te", "P2": "Si", "P5": "Fi", "P6": "Ne"},
    "EII (INFj)": {"P1": "Fi", "P2": "Ne", "P5": "Te", "P6": "Si"},
    "IEE (ENFp)": {"P1": "Ne", "P2": "Fi", "P5": "Si", "P6": "Te"},
    "SLI (ISTp)": {"P1": "Si", "P2": "Te", "P5": "Ne", "P6": "Fi"},
}

soci_to_mbti = {k: v for k, v in zip(socionics_structure.keys(), 
    ["ENTP", "ISFJ", "ESFJ", "INTP", "ENFJ", "ISTP", "ESTP", "INFJ", "ESFP", "INTJ", "ENTJ", "ISFP", "ESTJ", "INFP", "ENFP", "ISTJ"])}

# 質問リスト: 「能力」ではなく「価値（Valued/Unvalued）」を問う内容
questions = [
    # Ti: 論理的整合性への価値
    {"id": 1, "func": "Ti", "text": "感情的に納得するよりも、論理的な一貫性が保たれていることに深い安らぎを感じる。"},
    {"id": 2, "func": "Ti", "text": "物事の仕組みやルールが明確で、矛盾がない状態を何よりも重要視したい。"},
    {"id": 3, "func": "Ti", "text": "たとえ冷酷だと思われても、正しい論理的基準を貫く生き方に惹かれる。"},
    # Te: 実用的効率への価値
    {"id": 4, "func": "Te", "text": "単なる理論よりも、実際に役立つデータや結果を出すための「賢い方法」を常に求めている。"},
    {"id": 5, "func": "Te", "text": "無駄な努力を嫌い、客観的な事実に基づいてテキパキと状況を改善することに価値を感じる。"},
    {"id": 6, "func": "Te", "text": "自分がどう思うかより、それが「社会的に見て有効か、実利があるか」を基準に判断したい。"},
    # Fi: 個人的な絆・誠実さへの価値
    {"id": 7, "func": "Fi", "text": "表面的な愛想よりも、内面にある真実の思いや、一対一の深い信頼関係を大切にしたい。"},
    {"id": 8, "func": "Fi", "text": "自分なりの「善悪の基準」をしっかり持ち、自分の心に嘘をつかないことを人生の誇りにしたい。"},
    {"id": 9, "func": "Fi", "text": "他人の評価がどうあれ、自分が「好き」と感じる感覚や、人への好意を尊重して生きたい。"},
    # Fe: 感情の共有・熱狂への価値
    {"id": 10, "func": "Fe", "text": "場の空気が冷めているよりも、感情がオープンに表現され、みんなで熱狂を共有できる状態が好きだ。"},
    {"id": 11, "func": "Fe", "text": "自分の内面を黙って守るより、周囲の感情をポジティブに揺さぶり、盛り上げたいという欲求がある。"},
    {"id": 12, "func": "Fe", "text": "人々の情熱が目に見える形で溢れ出している環境にいると、自分も生きてる実感が湧く。"},
    # Si: 心身の調和・快適さへの価値
    {"id": 13, "func": "Si", "text": "野心のために無理をするよりも、日々の暮らしの快適さや、心身の健康を整えることを優先したい。"},
    {"id": 14, "func": "Si", "text": "五感（味、触り心地、空間）が心地よく調和していることに、高い価値を置いている。"},
    {"id": 15, "func": "Si", "text": "殺伐とした競争よりも、平穏でリラックスできる温かな環境に惹かれる。"},
    # Se: 意志の力・影響力への価値
    {"id": 16, "func": "Se", "text": "受動的に待つのではなく、自らの意志で現実を動かし、状況をコントロールすることに魅力を感じる。"},
    {"id": 17, "func": "Se", "text": "強さや決断力を持って、困難を突破していく人に強く惹かれる（あるいは自分もそうありたい）。"},
    {"id": 18, "func": "Se", "text": "目に見える勝利や、確固たる影響力を手に入れることは、人生において重要なことだと思う。"},
    # Ni: 将来のビジョン・隠れた意味への価値
    {"id": 19, "func": "Ni", "text": "目先の利益よりも、物事が将来どう変化していくかという「時間の流れ」や「予兆」に意識が向く。"},
    {"id": 20, "func": "Ni", "text": "現実の裏側に隠された深い意味や、人生の運命的なつながりを探求することに価値を感じる。"},
    {"id": 21, "func": "Ni", "text": "焦って行動するより、全体の流れを見極め、本質的なタイミングを待つことの方が大切だと思う。"},
    # Ne: 未知の可能性・アイデアへの価値
    {"id": 22, "func": "Ne", "text": "すでに知られていることよりも、まだ誰も試していない新しいアイデアや可能性に心が躍る。"},
    {"id": 23, "func": "Ne", "text": "一つの答えに縛られず、常に「もし～だったら？」と多角的な視点を持つ人でありたい。"},
    {"id": 24, "func": "Ne", "text": "平凡な日常から抜け出し、何かユニークで知的な刺激がある未来を追い求めていたい。"},
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
st.set_page_config(page_title="ソシオニクス価値観診断", layout="centered")

st.title("🧩 ソシオニクス価値観診断 (精密版)")
st.write("「何ができるか」ではなく、あなたが**「何を大切だと思うか」**を教えてください。")

user_answers = {}
for q in questions:
    st.markdown(f"#### {q['text']}")
    user_answers[q["id"]] = st.radio(
        label=f"q_{q['id']}",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {1: "全く違う", 2: "違う", 3: "どちらでもない", 4: "惹かれる", 5: "非常に惹かれる"}[x],
        horizontal=True,
        key=f"radio_{q['id']}",
        label_visibility="collapsed"
    )
    st.write("") # スペース用

if st.button("診断結果を算出", type="primary", use_container_width=True):
    res = calculate_diagnosis(user_answers)
    st.success("分析が完了しました。")
    
    st.header(f"結果: {res['socionics']}")
    st.subheader(f"（MBTIタイプ: {res['mbti_equiv']}）")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🥇 適合ランキング")
        for i, (name, score) in enumerate(res['ranking']):
            st.write(f"{i+1}. {name} : {score}点")
    with col2:
        st.write("### 📊 機能別価値スコア")
        df = pd.DataFrame([res['scores']]).T.reset_index()
        df.columns = ["機能", "スコア"]
        st.bar_chart(df.set_index("機能"))
