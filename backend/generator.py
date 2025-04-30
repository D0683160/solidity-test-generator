import os
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.chains import LLMChain
from dotenv import load_dotenv
from backend.rag_retriever import retrieve_context

load_dotenv()

def generate_test_code(selected_mode: str, contract_code: str, model_name: str, filename: str, use_rag: bool) -> str:
    base_name = os.path.splitext(filename)[0]

    if selected_mode == "One-Shot":
        prompt_file = "prompts/one_shot.txt"
    else:
        prompt_file = "prompts/zero_shot.txt"

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # 新邏輯：根據 use_rag 決定是否抓取context
    if use_rag:
        rag_context = retrieve_context(contract_code)
    else:
        rag_context = ""

    prompt = PromptTemplate(
        input_variables=["rag_context", "contract_code"],
        template=prompt_template
    )

    llm = Ollama(
        base_url="http://localhost:11434",
        model=model_name
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run(rag_context=rag_context, contract_code=contract_code)

    # 寫入測資檔案
    os.makedirs("test", exist_ok=True)
    test_path = f"test/{base_name}.js"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ 測資已寫入到 {test_path}")

    return result

