import subprocess

def run_tests():
    try:
        # 執行 Hardhat 測資
        test_process = subprocess.run(
            ["npx", "hardhat", "test"],
            check=True,
            capture_output=True,
            text=True
        )
        test_output = test_process.stdout
    except subprocess.CalledProcessError as e:
        test_output = f"❌ 測試執行錯誤:\n{e.stdout}\n{e.stderr}"

    try:
        # 執行 Hardhat 覆蓋率分析
        coverage_process = subprocess.run(
            ["npx", "hardhat", "coverage"],
            check=True,
            capture_output=True,
            text=True
        )
        coverage_output = coverage_process.stdout
    except subprocess.CalledProcessError as e:
        coverage_output = f"❌ 覆蓋率分析錯誤:\n{e.stdout}\n{e.stderr}"

    return test_output, coverage_output

