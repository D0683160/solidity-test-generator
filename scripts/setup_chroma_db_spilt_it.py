import os
import shutil
import subprocess
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# 設定
coverage_repo_url = "https://github.com/sc-forks/solidity-coverage.git"
temp_repo_dir = "temp_solidity_coverage"
contracts_root = os.path.join(temp_repo_dir, "contracts")
tests_root = os.path.join(temp_repo_dir, "test")
persist_directory = "chroma_db"

# 清理舊的 chroma_db
if os.path.exists(persist_directory):
    print("🧹 移除舊的 chroma_db...")
    shutil.rmtree(persist_directory)

# 清理舊的 temp repo
if os.path.exists(temp_repo_dir):
    print("🧹 移除舊的暫存 repo...")
    shutil.rmtree(temp_repo_dir)

# Clone solidity-coverage
print(f"📥 正在下載 {coverage_repo_url}...")
subprocess.run(["git", "clone", coverage_repo_url, temp_repo_dir], check=True)

# 建 Embedding
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents = []

# 處理 contracts/ 所有子資料夾
for root, dirs, files in os.walk(contracts_root):
    for file in files:
        if file.endswith(".sol"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={"source": os.path.relpath(path, temp_repo_dir)}
                )
                documents.append(doc)

# 處理 test/ 所有子資料夾
for root, dirs, files in os.walk(tests_root):
    for file in files:
        if file.endswith(".js"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # 切每個 it() 區塊
            it_blocks = re.findall(r'it\((.*?)\{(.*?)\}\)', content, flags=re.DOTALL)

            for idx, (it_title, it_body) in enumerate(it_blocks):
                it_title_clean = it_title.strip().strip('"').strip("'")
                full_content = f"it({it_title.strip()} {{ {it_body.strip()} }}"  # 還原成完整結構
                doc = Document(
                    page_content=full_content,
                    metadata={
                        "source": os.path.relpath(path, temp_repo_dir),
                        "it_title": it_title_clean,
                        "it_index": idx
                    }
                )
                documents.append(doc)

# 建立新的 ChromaDB
vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=persist_directory
)

vectordb.persist()

# 清理 temp repo
print("🧹 刪除下載的暫存 repo...")
shutil.rmtree(temp_repo_dir)

print(f"✅ 成功建立切 it() 的 ChromaDB！收錄 {len(documents)} 份資料")

