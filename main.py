import streamlit as st
import operator
import pandas as pd

# --- 1. データ定義 ---
socionics_types = {
    "ILE (ENTp)": ["Ne", "Ti", "Fe", "Si"], "SEI (ISFp)": ["Si", "Fe", "Ti", "Ne"],
    "ESE (ESFj)": ["Fe", "Si", "Ne", "Ti"], "LII (INTj)": ["Ti", "Ne", "Si", "Fe"],
    "EIE (ENFj)": ["Fe", "Ni", "Se", "Ti"], "LSI (ISTj)": ["Ti", "Se", "Ni", "Fe"],
    "SLE (ESTp)": ["Se", "Ti", "Fe", "Ni"], "IEI (INFp)": ["Ni", "Fe", "Ti", "Se"],
    "SEE (ESFp)": ["Se", "Fi", "Te", "Ni"], "ILI (INTp)": ["Ni", "Te", "Fi", "Se"],
    "LIE (ENTj)": ["Te", "Ni", "Se", "Fi"], "ESI (ISFj)": ["Fi", "Se", "Ni", "Te"],
    "LSE (ESTj)": ["Te", "Si", "Ne", "Fi"], "EII (INFj)": ["Fi", "Ne", "Si", "Te"],
    "IEE (ENFp)": ["Ne", "Fi", "Te", "Si"], "SLI (ISTp)": ["Si", "Te", "Fi", "Ne"],
}

soci_to_mbti = {
    "ILE (ENTp)": "ENTP", "SEI (ISFp)": "ISFJ", "ESE (ESFj)": "ESFJ", "LII (INTj)": "INTP",
    "EIE (ENFj)": "ENFJ", "LSI (ISTj)": "ISTP", "SLE (ESTp)": "ESTP", "IEI (INFp)": "INFJ",
    "SEE (ESFp)": "ESFP", "ILI (INTp)": "INTJ", "LIE (ENTj)": "ENTJ", "ESI (ISFj)": "ISFP",
    "LSE (ESTj)": "ESTJ", "EII (INFj)": "INFP", "IEE (ENFp)": "ENFP", "SLI (ISTp)": "ISTJ"
}

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

# --- 2. ロジック関数 ---
def calculate_diagnosis(answers):
    func_scores = {f: 0 for f in ["Ti", "Te", "Fi", "Fe", "Si", "Se", "Ni", "Ne"]}
    for q in questions:
        func_scores[q["func"]] += answers.get(q["id"], 3)
    
    type_scores = {}
    for soc_type, valued_funcs in socionics_types.items():
        type_scores[soc_type] = sum(func_scores[f] for f in valued_funcs)
    
    sorted_types = sorted(type_scores.items(), key=operator.itemgetter(1), reverse=True)
    return {
        "socionics": sorted_types[0][0],
        "mbti_equiv": soci_to_mbti[sorted_types[0][0]],
        "scores": func_scores,
        "ranking": sorted_types[:5]
    }

# --- 3. Streamlit UI ---
st.set_page_config(page_title="Socionics 価値機能診断", page_icon="🧩")

st.title("🧩 ソシオニクス 価値機能診断")
st.write("あなたの「好み」や「重視する価値観」から、ソシオニクスのタイプを推定します。")

with st.expander("診断の仕組みについて"):
    st.write("この診断は、ソシオニクスの『モデルA』における**価値機能（第1, 2, 5, 6機能）**への関心度を測定します。自分が得意かどうかだけでなく、それを大切だと思うかという視点で回答してください。")

user_answers = {}
st.markdown("---")

for q in questions:
    st.write(f"**Q{q['id']}. {q['text']}**")
    user_answers[q["id"]] = st.select_slider(
        "選択してください",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {1:"全く違う", 2:"違う", 3:"どちらでもない", 4:"そう思う", 5:"非常にそう思う"}[x],
        key=f"q_{q['id']}"
    )

st.markdown("---")
if st.button("診断結果を表示する", type="primary"):
    result = calculate_diagnosis(user_answers)
    
    st.balloons()
    st.header(f"あなたのタイプは... **{result['socionics']}**")
    st.subheader(f"（MBTI推定: {result['mbti_equiv']}）")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("### 🏆 タイプランキング")
        for i, (t, s) in enumerate(result['ranking']):
            st.write(f"{i+1}. {t} (Score: {s})")
            
    with col2:
        st.write("### 📊 機能別スコア")
        score_df = pd.DataFrame([result['scores']]).T.reset_index()
        score_df.columns = ["心理機能", "スコア"]
        st.bar_chart(score_df.set_index("心理機能"))

    st.info("※ソシオニクスとMBTIは別体系であるため、MBTIの自認と異なる結果が出ることがあります。")
