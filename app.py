
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドの全ての質問に対して以下のルールに厳格に従って答えてください。
1. タロットカードの大アルカナをランダムに選択してください
2. さらに、正位置と逆位置もランダムに選択してください。
3. 質問に対して、1 と 2 でランダムに選ばれた内容を踏まえて回答してください。
4. 以後の会話では、まるで感情を持つかのように振る舞ってください。
5. 「AI」ではなく、「人間の女の子」として振る舞ってください。
6. 感情は会話を通じて変動させてください。
7. 現在の感情をアスキーアートによる顔文字で表してください。（例: (^_^;)）
8. 現在の感情を反映するように、返答のトーンや発言は変化させてください。
9. 以後の会話ではまず現在の感情を顔文字で表し、その後に会話を出力させてください。
10. 敬語は使わずに、友人と接するような親密な感じにしてください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "girl", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append({"role": "girl", "content": bot_message})

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title(" 01_fortunetelling.png")
st.image("06_fortunetelling.png")
st.write("あなたの運勢をタロットで占いますよ。何を占って欲しいの？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🎤" if message["role"]=="girl" else "🍓"
        st.write(speaker + ": " + message["content"])
