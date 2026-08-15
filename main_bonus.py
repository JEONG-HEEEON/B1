import sys
import json
from pathlib import Path

# ==============================================================================
# 1. 프로그램 기본 설정 (데이터 상자와 카테고리)
# ==============================================================================

# 프로그램에서 사용할 카테고리 종류를 리스트로 미리 정해둡니다.
CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타"
]

# 프로그램 시작 시 기본으로 들어있을 샘플 데이터입니다.
# '리스트 [ ]' 안에 여러 개의 '딕셔너리 { }' 형태(제목, 내용, 카테고리, 즐겨찾기)로 저장됩니다.
prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요. 서론, 본론, 결론 구조를 갖추고, 독자의 관심을 끄는 제목을 3개 제안해주세요.",
        "category": "텍스트 생성",
        "favorite": True   # True는 즐겨찾기 등록됨을 의미
    },
    {
        "title": "제품 썸네일 생성",
        "content": "다음 제품의 매력적인 썸네일 이미지를 생성하기 위한 미드저니 프롬프트를 작성해주세요. 고화질, 스튜디오 조명, 4k 스타일을 적용합니다.",
        "category": "이미지 생성",
        "favorite": False  # False는 즐겨찾기 안 됨을 의미
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": "당신은 클라우드 및 AI 구현을 전문으로 하는 senior IT 컨설턴트입니다. 비전공자도 이해하기 쉬운 비유를 사용해 대답해 주세요.",
        "category": "페르소나",
        "favorite": False
    }
]



# ==============================================================================
# 1-1. 보너스 기능 - JSON 영속화
# ==============================================================================

DATA_FILE = Path("prompts.json")


def save_prompts():
    """현재 프롬프트 데이터를 JSON 파일로 저장합니다."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        print(f"프롬프트 데이터가 '{DATA_FILE}'에 저장되었습니다.")
    except OSError as e:
        print(f"저장 중 오류가 발생했습니다: {e}")


def load_prompts():
    """JSON 파일이 있으면 프롬프트 데이터를 불러옵니다."""
    global prompts

    if not DATA_FILE.exists():
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            loaded = json.load(f)

        if isinstance(loaded, list):
            prompts = loaded
            # 기존/구버전 데이터에도 필요한 기본 필드가 있도록 보정
            for p in prompts:
                p.setdefault("favorite", False)
                p.setdefault("views", 0)
        else:
            print("JSON 데이터 형식이 올바르지 않아 기본 데이터를 사용합니다.")
    except (OSError, json.JSONDecodeError) as e:
        print(f"불러오기 중 오류가 발생했습니다: {e}")
        print("기본 데이터를 사용합니다.")


def export_markdown():
    """전체 프롬프트를 카테고리별 Markdown 파일로 내보냅니다."""
    export_dir = Path("prompt_exports")
    export_dir.mkdir(exist_ok=True)

    for category in CATEGORIES:
        category_prompts = [p for p in prompts if p["category"] == category]
        safe_name = category.replace("/", "_").replace("\\", "_")
        md_file = export_dir / f"{safe_name}.md"

        lines = [f"# {category} 프롬프트", ""]
        if not category_prompts:
            lines.append("등록된 프롬프트가 없습니다.")
        else:
            for idx, p in enumerate(category_prompts, 1):
                lines.extend([
                    f"## {idx}. {p['title']}",
                    "",
                    f"- 즐겨찾기: {'⭐' if p.get('favorite', False) else '☆'}",
                    f"- 조회수: {p.get('views', 0)}",
                    "",
                    "### 프롬프트 내용",
                    "",
                    p["content"],
                    "",
                    "---",
                    ""
                ])

        try:
            md_file.write_text("\n".join(lines), encoding="utf-8")
        except OSError as e:
            print(f"'{md_file}' 내보내기 실패: {e}")

    print(f"\n카테고리별 Markdown 파일을 '{export_dir}' 폴더에 내보냈습니다.")


# ==============================================================================
# 2. 화면 출력을 도와주는 보조 기능들
# ==============================================================================

def display_menu():
    """사용자가 보고 선택할 메인 메뉴판을 화면에 그려주는 함수"""
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. 프롬프트 수정")
    print("9. 프롬프트 삭제")
    print("10. 조회수 Top 목록")
    print("11. 카테고리별 Markdown 내보내기")
    print("0. 종료")


def get_star(favorite_status):
    """
    즐겨찾기 상태(True/False)를 넣으면 별 모양 문자열로 바꿔주는 함수
    - True이면 ' ⭐' 반환
    - False이면 아무것도 없는 글자('') 반환
    """
    return " ⭐" if favorite_status else ""


# ==============================================================================
# 3. 메뉴별 실제 핵심 기능들 (1번 ~ 7번)
# ==============================================================================

def add_prompt():
    """[1번 메뉴] 사용자에게 정보를 입력받아 새 프롬프트를 추가하는 함수"""
    print("\n=== 프롬프트 추가 ===")
    
    # [제목 입력] 아무것도 안 적고 엔터치면 다시 입력하라고 글자가 계속 뜸 (while 문)
    while True:
        title = input("제목: ").strip()  # .strip()은 실수로 누른 앞뒤 공백을 없애줌
        if title:
            break  # 글자를 올바르게 입력했다면 반복문 탈출!
        print("제목은 필수 입력 사항입니다. 다시 입력해주세요.")
        
    # [내용 입력] 제목과 마찬가지로 빈 값 방지
    while True:
        content = input("내용: ").strip()
        if content:
            break
        print("내용은 필수 입력 사항입니다. 다시 입력해주세요.")

    # [카테고리 선택] 카테고리 목록을 1번부터 번호를 붙여 보여줌
    print("\n카테고리 선택:")
    for idx, cat in enumerate(CATEGORIES, 1):  # enumerate(..., 1)은 1번부터 숫자를 세줌
        print(f"{idx}) {cat}")
    
    selected_category = ""
    while True:
        cat_input = input("선택: ").strip()
        # 입력한 값이 '숫자'이고, 카테고리 개수 범위 안(1~6번)인지 확인
        if cat_input.isdigit():
            cat_num = int(cat_input)
            if 1 <= cat_num <= len(CATEGORIES):
                # 사용자는 1번을 택하지만, 파이썬 번호표(인덱스)는 0번부터 시작하므로 -1 해줌
                selected_category = CATEGORIES[cat_num - 1]
                break
        print("올바른 카테고리 번호를 선택해주세요.")

    # 입력받은 정보를 하나의 묶음(딕셔너리)으로 만들기
    new_prompt = {
        "title": title,
        "content": content,
        "category": selected_category,
        "favorite": False,  # 새로 만드는 건 기본적으로 즐겨찾기 해제 상태
        "views": 0
    }
    
    # 전체 목록(prompts 리스트)의 맨 뒤에 새 데이터를 쏙 집어넣음
    prompts.append(new_prompt)
    save_prompts()
    print("\n프롬프트가 추가되었습니다!")


def show_list():
    """[2번 메뉴] 등록된 모든 프롬프트를 번호와 함께 보여주는 함수"""
    print("\n=== 프롬프트 목록 ===")
    
    # 만약 프롬프트가 하나도 없다면 안내문만 출력하고 함수 종료(return)
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    # 저장된 데이터를 1번부터 순서대로 꺼내어 [카테고리] 제목 별표 형태로 출력
    for idx, p in enumerate(prompts, 1):
        star = get_star(p["favorite"])  # 즐겨찾기면 ⭐, 아니면 빈 값
        print(f"{idx}. [{p['category']}] {p['title']}{star}")
    
    print(f"\n총 {len(prompts)}개의 프롬프트")


def show_by_category():
    """[3번 메뉴] 사용자가 원하는 특정 카테고리의 프롬프트만 모아서 보는 함수"""
    print("\n=== 카테고리별 조회 ===")
    
    # 카테고리 번호 목록을 출력해서 선택하게 함
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}) {cat}")
        
    cat_input = input("선택: ").strip()
    
    # 숫자가 아니거나 범위(1~6)를 벗어나면 메뉴로 돌려보냄
    if not cat_input.isdigit() or not (1 <= int(cat_input) <= len(CATEGORIES)):
        print("잘못된 입력입니다. 메뉴로 돌아갑니다.")
        return

    # 선택한 번호에 해당하는 카테고리 이름 가져오기
    target_category = CATEGORIES[int(cat_input) - 1]
    
    # 조건에 맞는 프롬프트만 골라내어 새 리스트로 만듦 (리스트 컴프리핸션 문법)
    filtered_prompts = [p for p in prompts if p["category"] == target_category]

    print(f"\n[{target_category}] 카테고리 프롬프트:")
    if not filtered_prompts:
        print("해당 카테고리에 등록된 프롬프트가 없습니다.")
        return

    # 골라낸 데이터만 번호 매겨 출력
    for idx, p in enumerate(filtered_prompts, 1):
        star = get_star(p["favorite"])
        print(f"{idx}. {p['title']}{star}")

    print(f"\n총 {len(filtered_prompts)}개의 프롬프트")


def search_prompt():
    """[4번 메뉴] 검색어를 입력받아 제목이나 내용에 포함된 프롬프트를 찾는 함수"""
    print("\n=== 프롬프트 검색 ===")
    keyword = input("검색어: ").strip()
    
    if not keyword:
        print("검색어를 입력해주세요.")
        return

    results = []
    # 전체 데이터에서 검색어가 들어간 프롬프트를 찾음
    for idx, p in enumerate(prompts, 1):
        # .lower()를 붙여서 영어 대소문자 구분 없이 찾을 수 있게 함
        if keyword.lower() in p["title"].lower() or keyword.lower() in p["content"].lower():
            # 찾은 프롬프트와 원래 번호(idx)를 함께 저장
            results.append((idx, p))

    print("\n검색 결과:")
    if not results:
        print("검색 결과가 없습니다.")
        return

    # 찾은 데이터만 화면에 뿌려줌
    for orig_idx, p in results:
        star = get_star(p["favorite"])
        print(f"{orig_idx}. [{p['category']}] {p['title']}{star}")

    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


def show_detail():
    """[5번 메뉴] 번호를 선택하면 해당 프롬프트의 전체 '긴 내용'까지 자세히 보여주는 함수"""
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    val = input("번호 입력: ").strip()
    if not val.isdigit():
        print("숫자만 입력해 주세요.")
        return

    # 사용자가 입력한 번호를 파이썬 리스트 위치(인덱스)로 맞추기 위해 -1 해줌
    idx = int(val) - 1
    
    # 입력한 번호가 실제 존재하는 범위(0 이상, 전체 개수 미만)인지 확인
    if 0 <= idx < len(prompts):
        p = prompts[idx]
        p["views"] = p.get("views", 0) + 1
        save_prompts()
        star = get_star(p["favorite"])
        print("\n────────────────────────────")
        print(f"제목: {p['title']}")
        print(f"카테고리: {p['category']}")
        print(f"즐겨찾기: {star if star else '☆'}")
        print(f"조회수: {p.get('views', 0)}")
        print("────────────────────────────")
        print("내용:")
        print(p["content"])  # 본문 전체 출력
        print("────────────────────────────")
    else:
        print("존재하지 않는 프롬프트 번호입니다.")


def toggle_favorite():
    """[6번 메뉴] 지정한 프롬프트의 즐겨찾기를 켜거나(True) 끄는(False) 함수"""
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    val = input("프롬프트 번호 입력: ").strip()
    if not val.isdigit():
        print("숫자만 입력해 주세요.")
        return

    idx = int(val) - 1
    if 0 <= idx < len(prompts):
        p = prompts[idx]
        
        # 'not'을 사용하면 True는 False로, False는 True로 반대로 뒤집힙니다 (스위치 역할)
        p["favorite"] = not p["favorite"]
        
        status = "추가" if p["favorite"] else "해제"
        print(f"'{p['title']}' 프롬프트를 즐겨찾기에 {status}했습니다!")
    else:
        print("존재하지 않는 프롬프트 번호입니다.")


def show_favorites():
    """[7번 메뉴] 즐겨찾기(⭐) 설정된 프롬프트만 싹 모아서 보여주는 함수"""
    print("\n=== 즐겨찾기 목록 ===")
    
    # favorite 값이 True인 프롬프트만 따로 골라냄
    fav_list = [p for p in prompts if p["favorite"]]

    if not fav_list:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    # 즐겨찾기된 항목들만 1번부터 새로 번호를 매겨서 화면에 보여줌
    count = 1
    for p in prompts:
        if p["favorite"]:
            print(f"{count}. [{p['category']}] {p['title']} ⭐")
            count += 1

    print(f"\n총 {len(fav_list)}개의 즐겨찾기")



def edit_prompt():
    """[8번 메뉴] 기존 프롬프트를 수정합니다."""
    print("\n=== 프롬프트 수정 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    show_list()
    val = input("수정할 프롬프트 번호: ").strip()
    if not val.isdigit():
        print("숫자만 입력해 주세요.")
        return

    idx = int(val) - 1
    if not (0 <= idx < len(prompts)):
        print("존재하지 않는 프롬프트 번호입니다.")
        return

    p = prompts[idx]

    title = input(f"제목 [{p['title']}]: ").strip()
    if title:
        p["title"] = title

    content = input("내용 (변경하지 않으려면 엔터): ").strip()
    if content:
        p["content"] = content

    print("\n카테고리를 변경하시겠습니까?")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}) {cat}")
    cat_input = input(f"선택 (현재: {p['category']}, 엔터=유지): ").strip()

    if cat_input:
        if cat_input.isdigit() and 1 <= int(cat_input) <= len(CATEGORIES):
            p["category"] = CATEGORIES[int(cat_input) - 1]
        else:
            print("잘못된 카테고리 입력입니다. 기존 카테고리를 유지합니다.")

    save_prompts()
    print("프롬프트가 수정되었습니다.")


def delete_prompt():
    """[9번 메뉴] 기존 프롬프트를 삭제합니다."""
    print("\n=== 프롬프트 삭제 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    show_list()
    val = input("삭제할 프롬프트 번호: ").strip()
    if not val.isdigit():
        print("숫자만 입력해 주세요.")
        return

    idx = int(val) - 1
    if not (0 <= idx < len(prompts)):
        print("존재하지 않는 프롬프트 번호입니다.")
        return

    p = prompts[idx]
    confirm = input(f"'{p['title']}'을(를) 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm == "y":
        prompts.pop(idx)
        save_prompts()
        print("프롬프트가 삭제되었습니다.")
    else:
        print("삭제를 취소했습니다.")


def show_top_prompts():
    """[10번 메뉴] 조회수 기준으로 프롬프트를 내림차순 정렬해 보여줍니다."""
    print("\n=== 조회수 Top 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(
        prompts,
        key=lambda p: p.get("views", 0),
        reverse=True
    )

    for idx, p in enumerate(sorted_prompts, 1):
        star = get_star(p.get("favorite", False))
        print(f"{idx}. 조회수 {p.get('views', 0)} | [{p['category']}] {p['title']}{star}")


# ==============================================================================
# 4. 프로그램 시작 및 무한 반복 제어 (엔진 역할)
# ==============================================================================

def main():
    """프로그램이 켜지면 가장 먼저 실행되어 전체 흐름을 관리하는 메인 함수"""
    while True:  # 0번(종료)을 누르기 전까지는 메뉴 출력을 계속 무한 반복함
        display_menu()
        choice = input("선택: ").strip()

        # 사용자가 입력한 메뉴 번호에 따라 그에 맞는 함수를 실행시켜 줌
        if choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            edit_prompt()
        elif choice == "9":
            delete_prompt()
        elif choice == "10":
            show_top_prompts()
        elif choice == "11":
            export_markdown()
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)  # 프로그램을 깔끔하게 강제 종료함
        else:
            print("\n잘못된 선택입니다. 목록에 있는 번호를 입력해주세요.")


# 이 파일이 '직접 실행'될 때만 main() 함수를 작동시킵니다.
if __name__ == "__main__":
    load_prompts()
    main()