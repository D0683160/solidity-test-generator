import streamlit as st
import requests
import os

st.set_page_config(page_title="🛠️ Solidity 測資自動生成器 (FastAPI版)", layout="wide")
st.title("🛠️ Solidity 測資自動生成器")

# --- 自動抓模型列表 ---
with st.spinner("讀取可用模型中..."):
    model_list = []
    try:
        res = requests.get("http://localhost:8000/list_models")
        model_list = res.json().get("models", [])
    except Exception as e:
        st.error(f"讀取模型列表失敗：{e}")

if not model_list:
    st.error("⚠️ 沒有讀到任何模型，請確認 Ollama 有啟動！")
    st.stop()

# 選擇生成模式
mode = st.selectbox("選擇生成模式", ["One-Shot", "Zero-Shot"], key="prompt_mode")

# 選擇是否啟用RAG
use_rag = st.selectbox("是否啟用RAG輔助？", ["啟用", "不啟用"], key="use_rag") == "啟用"

# 選擇模型
model = st.selectbox("選擇使用的模型", model_list, key="model_choice")

# 上傳 Solidity 合約
uploaded_file = st.file_uploader("上傳 Solidity 合約 (.sol)", type=["sol"])

contract_code = ""
uploaded_filename = None

if uploaded_file is not None:
    contract_code = uploaded_file.read().decode()
    uploaded_filename = uploaded_file.name

# 手動貼合約內容
contract_code_textarea = st.text_area("或直接貼上 Solidity 代碼", height=300)

if contract_code_textarea.strip():
    contract_code = contract_code_textarea
    uploaded_filename = "UploadedContract.sol"

# --- 產生測資按鈕
if st.button("🚀 產生測資") and contract_code:
    with st.spinner("生成測資中..."):
        res = requests.post(
            "http://localhost:8000/generate_test",
            json={
                "mode": mode,
                "model": model,
                "filename": uploaded_filename,
                "contract_code": contract_code,
                "use_rag": use_rag
            }
        )
        if res.status_code == 200:
            st.session_state["test_code"] = res.json()["test_code"]
            st.success("✅ 測資生成完成！")
        else:
            st.error(f"❌ 產生測資失敗：{res.status_code}\n{res.text}")

# --- 顯示生成的測資 + 執行測資按鈕
if "test_code" in st.session_state:
    st.subheader("📜 生成的測資")
    st.code(st.session_state["test_code"], language="javascript")

    st.download_button(
        label="💾 下載測資檔",
        data=st.session_state["test_code"],
        file_name=os.path.splitext(uploaded_filename)[0] + ".js" if uploaded_filename else "generated_test.js",
        mime="text/javascript"
    )

    if st.button("🧪 執行測資 + 產生覆蓋率報告"):
        with st.spinner("執行測試中..."):
            res = requests.post("http://localhost:8000/run_tests")
            if res.status_code == 200:
                st.session_state["test_result"] = res.json()["test_result"]
                st.session_state["coverage_result"] = res.json()["coverage_result"]
            else:
                st.error(f"❌ 執行測試失敗：{res.status_code}\n{res.text}")

# --- 顯示 Hardhat 測資結果 & 覆蓋率
if "test_result" in st.session_state:
    st.subheader("📄 測試結果")
    st.code(st.session_state["test_result"], language="bash")

if "coverage_result" in st.session_state:
    st.subheader("📊 覆蓋率報告")
    st.code(st.session_state["coverage_result"], language="bash")

