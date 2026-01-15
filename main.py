import streamlit as st
import operator
import pandas as pd

# --- 1. データ定義 ---
# 各タイプの「価値機能（Valued）」
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

all_funcs = ["Ti", "Te", "Fi", "Fe", "Si", "Se", "Ni", "Ne"]

soci_to_mbti = {
    "ILE (ENTp)": "ENTP", "SEI (ISFp)": "ISFJ", "ESE (ESFj)": "ESFJ", "LII (INTj)": "INTP",
    "EIE (ENFj)": "ENFJ", "LSI (ISTj)": "ISTP", "SLE (ESTp)": "ESTP", "IEI (INFp)": "INFJ",
    "SEE (ESFp)": "ESFP", "ILI (INTp)": "INTJ", "LIE (ENTj)": "ENTJ", "ESI (ISFj)": "ISFP",
    "LSE (ESTj)": "ESTJ", "EII (INFj)": "INFP", "IEE (ENFp)": "ENFP", "SLI (ISTp)": "ISTJ"
}

# 質問リスト (各機能5問、計40問)
questions = [
    # Ti
    {"id": 1, "func": "Ti", "text": "論理的矛盾を見つけると、それを正さずにはいられない。"},
    {"id": 2, "func": "Ti", "text": "物事の根本的な原理や構造を理解することに快感を覚える。"},
    {"id": 3, "func": "Ti", "text": "誰に対しても公平な、普遍的なルールを適用すべきだと思う。"},
    {"id": 4, "func": "Ti", "text": "感情的な訴えよりも、論理的な一貫性がある説明を信頼する。"},
    {"id": 5, "func": "Ti", "text": "複雑な情報を分類し、整理された体系を作るのが得意だ。"},
    # Te
    {"id": 6, "func": "Te", "text": "「どれだけ効率的に成果を出せるか」を常に考えて行動している。"},
    {"id": 7, "func": "Te", "text": "有用なデータや事実に基づいた、実用的なアドバイスを好む。"},
    {"id": 8, "func": "Te", "text": "目的達成のためなら、既存のやり方を合理的に作り変える。"},
    {"id": 9, "func": "Te", "text": "個人の感情よりも、組織や社会の生産性を重視すべきだ。"},
    {"id": 10, "func": "Te", "text": "専門的な知識を習得し、それを実生活で役立てるのが好きだ。"},
    # Fi
    {"id": 11, "func": "Fi", "text": "自分の内なる「好き・嫌い」の感覚を何よりも大切にしている。"},
    {"id": 12, "func": "Fi", "text": "人との親密な心の交流や、深い信頼関係を重視する。"},
    {"id": 13, "func": "Fi", "text": "他人の評価よりも、自分の良心に従って生きることを選ぶ。"},
    {"id": 14, "func": "Fi", "text": "相手の心の痛みに共感し、寄り添うことに大きな意味を感じる。"},
    {"id": 15, "func": "Fi", "text": "「この人は信頼できる」という直感的な判断を大切にする。"},
    # Fe
    {"id": 16, "func": "Fe", "text": "その場の情熱や感動を、みんなで共有して盛り上がるのが好きだ。"},
    {"id": 17, "func": "Fe", "text": "周囲の人が明るい気持ちになれるよう、振る舞いに気をつかう。"},
    {"id": 18, "func": "Fe", "text": "集団の団結力を高め、活気ある雰囲気を作ることにやりがいを感じる。"},
    {"id": 19, "func": "Fe", "text": "感情表現が豊かで、オープンなコミュニケーションを好む。"},
    {"id": 20, "func": "Fe", "text": "他人の感情を動かし、強い影響を与えることに魅力を感じる。"},
    # Si
    {"id": 21, "func": "Si", "text": "健康や快適さ、五感を通じた心地よさを維持することに価値を置く。"},
    {"id": 22, "func": "Si", "text": "生活の中の小さな変化や、体調の細かな波に敏感である。"},
    {"id": 23, "func": "Si", "text": "急激な変化よりも、安定してリラックスできる環境を好む。"},
    {"id": 24, "func": "Si", "text": "美的な調和や、洗練された空間・食事を楽しむ時間が大切だ。"},
    {"id": 25, "func": "Si", "text": "無理をせず、自分のペースを守って過ごすことが重要だと思う。"},
    # Se
    {"id": 26, "func": "Se", "text": "困難に直面したとき、自分の意志と力で状況を支配したいと思う。"},
    {"id": 27, "func": "Se", "text": "「今、この瞬間」の現実を動かす力強さに魅力を感じる。"},
    {"id": 28, "func": "Se", "text": "競争や挑戦的な状況において、自分の実力を発揮することに興奮する。"},
    {"id": 29, "func": "Se", "text": "目標を達成するために、周囲に直接的な影響を及ぼすことを厭わない。"},
    {"id": 30, "func": "Se", "text": "決断が速く、必要であればリスクを取って行動に移す。"},
    # Ni
    {"id": 31, "func": "Ni", "text": "目先の出来事よりも、その背後にある歴史や未来の流れに惹かれる。"},
    {"id": 32, "func": "Ni", "text": "人生の哲学的な意味や、抽象的なシンボルについて考えるのが好きだ。"},
    {"id": 33, "func": "Ni", "text": "物事の結末や、将来どのような変化が起きるかを予測するのが得意だ。"},
    {"id": 34, "func": "Ni", "text": "静かに内省し、自分の精神的な洞察を深める時間を必要とする。"},
    {"id": 35, "func": "Ni", "text": "「いつ、何をすべきか」という直感的なタイミングの感覚を信じている。"},
    # Ne
    {"id": 36, "func": "Ne", "text": "新しいアイデアや、まだ見ぬ可能性を探求することにワクワクする。"},
    {"id": 37, "func": "Ne", "text": "一つのことに縛られず、多種多様な選択肢を検討するのが好きだ。"},
    {"id": 38, "func": "Ne", "text": "型破りな発想や、ユニークな才能を持つ人に惹かれる。"},
    {"id": 39, "func": "Ne", "text": "知的好奇心が旺盛で、未知の分野を知ることに大きな喜びを感じる。"},
    {"id": 40, "func": "Ne", "text": "現状を打破するような、斬新なビジョンを常に求めている。"},
]

# --- 2. 診断ロジック ---
def calculate_diagnosis(answers):
    # スコアを -2 〜 2 に変換
    score_map = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}
    func_scores = {f: 0 for f in all_funcs}
    for q in questions:
        func_scores[q["func"]] += score_map.get(answers.get(q["id"], 3), 0)
    
    type_scores = {}
    for soc_type, valued_funcs in socionics_types.items():
        # 価値機能(Valued)は加算、非価値機能(Unvalued)は減算
        unvalued_funcs = [f for f in all_funcs if f not in valued_funcs]
        
        score = sum(func_scores[f] for f in valued_funcs)
        score -= sum(func_scores[f] for f in unvalued_funcs)
        
        type_scores[soc_type] = score
    
    sorted_types = sorted(type_scores.items(), key=operator.itemgetter(1), reverse=True)
    return {
        "socionics": sorted_types[0][0],
        "mbti_equiv": soci_to_mbti[sorted_types[0][0]],
        "scores": func_scores,
        "ranking": sorted_types[:5]
    }

# --- 3. Streamlit UI ---
st.set_page_config(page_title="ソシオニクス診断", page_icon="🧬")

st.title("🧬 ソシオニクス診断 (Ver 2.0)")

user_answers = {}

# 質問の表示
for q in questions:
    st.markdown(f"**Q{q['id']}. {q['text']}**")
    # ボタン形式（segmented_control）
    ans = st.radio(
        label="選択肢",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {1:"全く違う", 2:"違う", 3:"普通", 4:"そう思う", 5:"非常にそう思う"}[x],
        key=f"q_{q['id']}",
        horizontal=True,
        label_visibility="collapsed"
    )
    user_answers[q["id"]] = ans
    st.divider()

if st.button("診断結果を計算する", type="primary", use_container_width=True):
    result = calculate_diagnosis(user_answers)
    
    st.balloons()
    st.header(f"あなたのタイプは: **{result['socionics']}**")
    st.subheader(f"（MBTI推定: {result['mbti_equiv']}）")
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### 🏅 上位適合ランキング")
        for i, (t, s) in enumerate(result['ranking']):
            # スコアの正規化（見やすさのため）
            st.write(f"{i+1}. **{t}** (適合度: {s})")
            
    with col2:
        st.write("### 機能チャート")
        # グラフ用のデータ整形
        df = pd.DataFrame([result['scores']]).T.reset_index()
        df.columns = ["心理機能", "スコア"]
        st.bar_chart(df.set_index("心理機能"))
