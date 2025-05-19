from bs4 import BeautifulSoup
import re
import os
import requests


def get_problem_info(workbook_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    print(f"🌐 요청 중: {workbook_url}")
    response = requests.get(workbook_url, headers=headers)
    print(f"📥 응답 수신 완료: 상태 코드 {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    problem_map = {}

    for a_tag in soup.select('a[href^="/problem/"]'):
        href = a_tag.get("href")
        prob_id = href.split("/")[-1]
        prob_title = a_tag.text.strip()
        norm_title = re.sub(r"[^가-힣a-zA-Z0-9]", "", prob_title)

        if prob_id.isdigit():
            problem_map[norm_title] = prob_id
            print(f'  🔍 {norm_title} ← "{prob_title}" → {prob_id}')

    print(f"\n📋 추출된 문제 수: {len(problem_map)}개")
    return problem_map


# 파일 리네이밍
def rename_files(folder_path, problem_map):
    renamed = 0
    files = os.listdir(folder_path)
    print(f"📁 디렉토리 목록: {files}")
    for fname in files:
        ext = os.path.splitext(fname)[1]
        if ext not in [".cpp", ".py"]:
            continue
        base = os.path.splitext(fname)[0]
        normalized = re.sub(r"[^가-힣a-zA-Z0-9]", "", base)
        print(f"🔎 파일 체크: {fname} → 정규화: {normalized}")
        if normalized in problem_map:
            prob_id = problem_map[normalized]
            new_name = f"{prob_id}{ext}"
            old_path = os.path.join(folder_path, fname)
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"✔️ {fname} → {new_name}")
                renamed += 1
        else:
            print(f"⚠️ 매핑 실패: {normalized}는 문제집에 없음")
    return renamed


# links.txt에서 단원별 코드와 URL 읽기
def parse_links():
    with open("links.txt", encoding="utf-8") as f:
        lines = [line.strip().split(",") for line in f if line.strip()]
    print(f"🧾 links.txt 내용:\n{lines}")
    return [
        (code.strip(), url.strip()) for code, _, url in lines if url.startswith("http")
    ]


# 전체 자동 처리
def auto_rename_all():
    print("📂 links.txt에서 단원별 문제집 읽는 중...")
    links = parse_links()
    total = 0
    for code, url in links:
        folder = f"../{code}/"
        if not os.path.isdir(folder):
            print(f"❌ 폴더 없음: {folder}")
            continue
        print(f"\n📥 {code} - 문제집 URL: {url}")
        try:
            problem_map = get_problem_info(url)
        except Exception as e:
            print(f"❌ 문제집 파싱 실패: {e}")
            continue
        print(f"🔁 파일 리네이밍 중 in {folder} ...")
        try:
            count = rename_files(folder, problem_map)
            print(f"✅ {count}개 파일 변경 완료")
            total += count
        except Exception as e:
            print(f"❌ 리네이밍 오류: {e}")
    print(f"\n🎉 전체 완료! 총 {total}개 파일 변경됨.")


if __name__ == "__main__":
    auto_rename_all()
