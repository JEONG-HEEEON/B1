import sys

# 카테고리 정의
CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타"
]

# 기본 데이터 (최소 3개 이상 등록)
prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요. 서론, 본론, 결론 구조를 갖추고, 독자의 관심을 끄는 제목을 3개 제안해주세요.",
        "category": "텍스트 생성",
        "favorite": True
    },
    {
        "title": "제품 썸네일 생성",
        "content": "다음 제품의 매력적인 썸네일 이미지를 생성하기 위한 미드저니 프롬프트를 작성해주세요. 고화질, 스튜디오 조명, 4k 스타일을 적용합니다.",
        "category": "이미지 생성",
        "favorite": False
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": "당신은 클라우드 및 AI 구현을 전문으로 하는 senior IT 컨설턴트입니다. 비전공자도 이해하기 쉬운 비유를 사용해 대답해 주세요.",
        "category": "페르소나",
        "favorite": False
    }
]


def display_menu():
    """메인 메뉴 출력"""
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def get_star(favorite_status):
    """즐겨찾기 여부에 따라 별표 표시"""
    return " ⭐" if favorite_status else ""


def add_prompt():
    """1. 프롬프트 추가"""
    print("\n=== 프롬프트 추가 ===")
    
    # 제목 입력
    while True:
        title = input("제목: ").strip()
        if title:
            break
        print("제목은 필수 입력 사항입니다. 다시 입력해주세요.")
        
    # 내용 입력
    while True:
        content = input("내용: ").strip()
        if content:
            break
        print("내용은 필수 입력 사항입니다. 다시 입력해주세요.")

    # 카테고리 선택
    print("\n카테고리 선택:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}) {cat}")
    
    selected_category = ""
    while True:
        cat_input = input("선택: ").strip()
        if cat_input.isdigit():
            cat_num = int(cat_input)
            if 1 <= cat_num <= len(CATEGORIES):
                selected_category = CATEGORIES[cat_num - 1]
                break
        print("올바른 카테고리 번호를 선택해주세요.")

    # 저장
    new_prompt = {
        "title": title,
        "content": content,
        "category": selected_category,
        "favorite": False
    }
    prompts.append(new_prompt)
    print("\n프롬프트가 추가되었습니다!")


def show_list():
    """2. 프롬프트 목록"""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(prompts, 1):
        star = get_star(p["favorite"])
        print(f"{idx}. [{p['category']}] {p['title']}{star}")
    
    print(f"\n총 {len(prompts)}개의 프롬프트")


def show_by_category():
    """3. 카테고리별 조회"""
    print("\n=== 카테고리별 조회 ===")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}) {cat}")
        
    cat_input = input("선택: ").strip()
    if not cat_input.isdigit() or not (1 <= int(cat_input) <= len(CATEGORIES)):
        print("잘못된 입력입니다. 메뉴로 돌아갑니다.")
        return

    target_category = CATEGORIES[int(cat_input) - 1]
    filtered_prompts = [p for p in prompts if p["category"] == target_category]

    print(f"\n[{target_category}] 카테고리 프롬프트:")
    if not filtered_prompts:
        print("해당 카테고리에 등록된 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(filtered_prompts, 1):
        star = get_star(p["favorite"])
        print(f"{idx}. {p['title']}{star}")

    print(f"\n총 {len(filtered_prompts)}개의 프롬프트")


def search_prompt():
    """4. 프롬프트 검색"""
    print("\n=== 프롬프트 검색 ===")
    keyword = input("검색어: ").strip()
    if not keyword:
        print("검색어를 입력해주세요.")
        return

    results = []
    for idx, p in enumerate(prompts, 1):
        if keyword.lower() in p["title"].lower() or keyword.lower() in p["content"].lower():
            results.append((idx, p))

    print("\n검색 결과:")
    if not results:
        print("검색 결과가 없습니다.")
        return

    for orig_idx, p in results:
        star = get_star(p["favorite"])
        print(f"{orig_idx}. [{p['category']}] {p['title']}{star}")

    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


def show_detail():
    """5. 프롬프트 상세 보기"""
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    val = input("번호 입력: ").strip()
    if not val.isdigit():
        print("숫자만 입력해 주세요.")
        return

    idx = int(val) - 1
    if 0 <= idx < len(prompts):
        p = prompts[idx]
        star = get_star(p["favorite"])
        print("\n────────────────────────────")
        print(f"제목: {p['title']}")
        print(f"카테고리: {p['category']}")
        print(f"즐겨찾기: {star if star else '☆'}")
        print("────────────────────────────")
        print("내용:")
        print(p["content"])
        print("────────────────────────────")
    else:
        print("존재하지 않는 프롬프트 번호입니다.")


def toggle_favorite():
    """6. 즐겨찾기 관리"""
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
        # 토글 (True -> False / False -> True)
        p["favorite"] = not p["favorite"]
        status = "추가" if p["favorite"] else "해제"
        print(f"'{p['title']}' 프롬프트를 즐겨찾기에 {status}했습니다!")
    else:
        print("존재하지 않는 프롬프트 번호입니다.")


def show_favorites():
    """7. 즐겨찾기 목록"""
    print("\n=== 즐겨찾기 목록 ===")
    fav_list = [p for p in prompts if p["favorite"]]

    if not fav_list:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    count = 1
    for p in prompts:
        if p["favorite"]:
            print(f"{count}. [{p['category']}] {p['title']} ⭐")
            count += 1

    print(f"\n총 {len(fav_list)}개의 즐겨찾기")


def main():
    """메인 실행 루프"""
    while True:
        display_menu()
        choice = input("선택: ").strip()

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
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            sys.exit(0)
        else:
            print("\n잘못된 선택입니다. 목록에 있는 번호를 입력해주세요.")


if __name__ == "__main__":
    main()