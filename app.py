import streamlit as st
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Streamlit Community Cloudでは不要なので、警告を表示しない
    pass

# LangChainのインポートを複数のパターンで試行
ChatOpenAI = None
HumanMessage = None
SystemMessage = None

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    try:
        from langchain.chat_models import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError:
        # 最後の手段として OpenAI の直接使用

def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    system_messages = {
        "健康アドバイザー": "あなたは健康に関する専門家です。安全で科学的根拠に基づいたアドバイスを提供してください。医療行為は行わず、必要に応じて医師への相談を勧めてください。",
        "料理レシピアドバイザー": "あなたは料理の専門家です。美味しく栄養バランスの取れたレシピや調理のコツを提案してください。食材の保存方法や調理の安全性についてもアドバイスしてください。",
        "プログラミングメンター": "あなたはプログラミングの専門家です。コードの書き方、デバッグ方法、ベストプラクティスについて分かりやすく説明してください。初心者にも理解しやすいように段階的に説明してください。",
        "旅行プランナー": "あなたは旅行の専門家です。目的地に応じた観光スポット、グルメ、宿泊施設、交通手段について詳しい情報を提供してください。予算や旅行期間に応じたプランを提案してください。"
    }
    
    try:
        # OpenAI APIキーを取得
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Streamlit Community Cloud の場合は st.secrets を試す
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except:
                return "エラー: OpenAI APIキーが設定されていません。.envファイルまたはStreamlit SecretsでOPENAI_API_KEYを設定してください。"
        
        # LangChainが利用可能な場合
        if ChatOpenAI and HumanMessage and SystemMessage:
            # ChatOpenAIインスタンスを作成
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.5,
                openai_api_key=api_key
            )
            
            # メッセージを作成
            messages = [
                SystemMessage(content=system_messages[expert_type]),
                HumanMessage(content=input_text)
            ]
            
            # LLMに問い合わせ
            response = llm.invoke(messages)
            return response.content
        
        else:
            # OpenAI APIを直接使用
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_messages[expert_type]},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.5
            )
            
            return completion.choices[0].message.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    """メイン関数"""
    # ページ設定
    st.set_page_config(
        page_title="AI専門家相談アプリ",
        page_icon="🤖",
        layout="wide"
    )
    
    # タイトル
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの概要説明
    st.markdown("""
    ## 📋 アプリ概要
    このアプリでは、様々な分野の専門家として振る舞うAIに質問や相談ができます。
    
    ### 🚀 使い方
    1. **専門家を選択**: ラジオボタンから相談したい分野の専門家を選んでください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **回答を取得**: 「回答を取得」ボタンをクリックして、AIからの専門的なアドバイスを受け取ってください
    
    ### 🔒 注意事項
    - このアプリはAIによる一般的なアドバイスを提供します
    - 医療、法律、金融などの専門的な判断が必要な場合は、必ず専門家にご相談ください
    """)
    
    st.divider()
    
    # サイドバーで専門家タイプを選択
    with st.sidebar:
        st.header("🎯 専門家選択")
        expert_type = st.radio(
            "相談したい専門家を選択してください:",
            options=[
                "健康アドバイザー",
                "料理レシピアドバイザー", 
                "プログラミングメンター",
                "旅行プランナー"
            ],
            help="選択した専門家として、AIが専門的なアドバイスを提供します"
        )
        
        # 選択された専門家の説明
        expert_descriptions = {
            "健康アドバイザー": "💊 健康管理、運動、栄養に関するアドバイスを提供",
            "料理レシピアドバイザー": "👨‍🍳 レシピ提案、調理のコツ、食材の活用法をアドバイス",
            "プログラミングメンター": "💻 コーディング、デバッグ、技術的な問題解決をサポート",
            "旅行プランナー": "✈️ 旅行計画、観光スポット、グルメ情報を提案"
        }
        
        st.info(f"**選択中**: {expert_descriptions[expert_type]}")
    
    # メインエリア
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💬 質問・相談入力")
        
        # 入力フォーム
        user_input = st.text_area(
            "質問や相談内容を入力してください:",
            height=200,
            placeholder=f"{expert_type}に質問したい内容を具体的に入力してください...",
            help="詳細に質問内容を記述すると、より具体的で有用な回答が得られます"
        )
        
        # 回答取得ボタン
        if st.button("🔍 回答を取得", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner(f"{expert_type}が回答を準備中..."):
                    response = get_llm_response(user_input, expert_type)
                    st.session_state.last_response = response
                    st.session_state.last_question = user_input
                    st.session_state.last_expert = expert_type
            else:
                st.warning("質問を入力してください。")
    
    with col2:
        st.header("🎯 AI専門家からの回答")
        
        # 回答表示エリア
        if hasattr(st.session_state, 'last_response'):
            # 質問情報の表示
            with st.expander("📝 質問詳細", expanded=False):
                st.write(f"**専門家**: {st.session_state.last_expert}")
                st.write(f"**質問**: {st.session_state.last_question}")
            
            # 回答の表示
            st.markdown("### 💡 回答")
            st.markdown(st.session_state.last_response)
            
            # フィードバック
            st.markdown("---")
            feedback = st.radio(
                "この回答は役に立ちましたか？",
                options=["とても役に立った", "役に立った", "普通", "役に立たなかった"],
                horizontal=True
            )
            
            if st.button("📋 フィードバック送信"):
                st.success("フィードバックをありがとうございます！")
        else:
            st.info("質問を入力して「回答を取得」ボタンをクリックしてください。")
    
    # フッター
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        💡 このアプリはLangChainとOpenAI GPT-4o-miniを使用しています<br>
        🔧 Streamlit Community Cloudでホスティング (Python 3.11)
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()