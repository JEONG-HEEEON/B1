# =============================================
# 프롬프트 관리 프로그램
# =============================================

# ── 기본 데이터 (이전 미션 프롬프트 3개 이상) ──────────────
prompts = [
    {
        "id": 1,
        "title": "블로그 글 작성 도우미",
        "content": "당신은 전문 블로그 작가입니다. "
                   "주제: [주제]에 대해 독자가 쉽게 이해할 수 있도록 "
                   "서론-본론-결론 구조로 800자 내외의 글을 작성해주세요. "
                   "친근하고 읽기 쉬운 문체를 사용하세요.",
        "category": "텍스트 생성",
        "favorite": False
    },
    {
        "id": 2,
        "title": "이미지 프롬프트 생성기",
        "content": "다음 조건으로 이미지 생성 AI용 프롬프트를 만들어주세요. "
                   "주제: [주제], 스타일: [스타일], 분위기: [분위기]. "
                   "영어로 작성하고 세부 묘사를 포함해주세요.",
        "category": "이미지 생성",
        "favorite": False
    },
    {
        "id": 3,
        "title": "코드 리뷰어 페르소나",
        "content": "당신은 10년 경력의 시니어 개발자입니다. "
                   "아래 코드를 검토하고 다음 항목을 피드백해주세요: "
                   "1) 버그 가능성 2) 성능 개선점 3) 가독성 4) 보안 이슈. "
                   "친절하지만 명확하게 설명해주세요.",
        "category": "페르소나",
        "favorite": True
    },
    {
        "id": 4,
        "title": "유튜브 쇼츠 스크립트",
        "content": "60초 유튜브 쇼츠용 스크립트를 작성해주세요. "
                   "주제: [주제]. 훅(Hook) → 핵심 내용 → 행동 유도(CTA) "
                   "순서로 구성하고, 자막에 적합한 짧은 문장을 사용하세요.",
        "category": "영상 생성",
        "favorite": False
    },
    {
        "id": 5,
        "title": "이메일 자동 작성",
        "content": "아래 상황에 맞는 비즈니스 이메일을 작성해주세요. "
                   "발신자: [이름/직책], 수신자: [이름/직책], "
                   "목적: [목적]. 정중하고 간결한 문체로 작성해주세요.",
        "category": "자동화",
        "favorite": False
    },
]

# 다음 ID 추적용
next_id = len(prompts) + 1

# 카테고리 목록
CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]


# ── 메뉴 출력 ───────────────────────────────────────────────
def show_menu():
    print("\n" + "=" * 40)
    print("     📚 프롬프트 관리 프로그램")
    print("=" * 40)
    print("  1. 프롬프트 목록 보기")
    print("  2. 프롬프트 추가")
    print("  3. 카테고리별 조회")
    print("  4. 프롬프트 검색")
    print("  5. 프롬프트 상세 보기")
    print("  6. 즐겨찾기 관리")
    print("  0. 종료")
    print("=" * 40)


# ── 1. 프롬프트 목록 보기 ────────────────────────────────────
def show_list(target_list=None, title="전체 프롬프트 목록"):
    """프롬프트 목록을 출력하는 함수 (기본: 전체 목록)"""
    data = target_list if target_list is not None else prompts

    print(f"\n── {title} ──")

    if not data:
        print("  등록된 프롬프트가 없습니다.")
        return

    print(f"  총 {len(data)}개")
    print("-" * 40)
    for i, p in enumerate(data, 1):
        star = "⭐" if p["favorite"] else "  "
        print(f"  {i}. {star} [{p['category']}] {p['title']}")
    print("-" * 40)


# ── 2. 프롬프트 추가 ─────────────────────────────────────────
def add_prompt():
    global next_id
    print("\n── 프롬프트 추가 ──")

    # 제목 입력
    while True:
        title = input("  제목: ").strip()
        if title:
            break
        print("  ⚠️  제목을 입력해주세요.")

    # 내용 입력
    while True:
        content = input("  내용: ").strip()
        if content:
            break
        print("  ⚠️  내용을 입력해주세요.")

    # 카테고리 선택
    category = select_category()

    # 저장
    new_prompt = {
        "id": next_id,
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    }
    prompts.append(new_prompt)
    next_id += 1

    print(f"\n  ✅ '{title}' 프롬프트가 추가되었습니다!")


# ── 카테고리 선택 헬퍼 ──────────────────────────────────────
def select_category():
    """카테고리 목록을 보여주고 선택받는 함수"""
    print("\n  카테고리를 선택하세요:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    print(f"    {len(CATEGORIES) + 1}. 직접 입력")

    while True:
        choice = input("  번호 선택: ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(CATEGORIES):
                return CATEGORIES[num - 1]
            elif num == len(CATEGORIES) + 1:
                while True:
                    custom = input("  카테고리 직접 입력: ").strip()
                    if custom:
                        return custom
                    print("  ⚠️  카테고리를 입력해주세요.")
        print("  ⚠️  올바른 번호를 입력해주세요.")


# ── 3. 카테고리별 조회 ───────────────────────────────────────
def show_by_category():
    print("\n── 카테고리별 조회 ──")

    # 현재 사용 중인 카테고리 목록 추출
    used_categories = list(set(p["category"] for p in prompts))
    used_categories.sort()

    if not used_categories:
        print("  등록된 프롬프트가 없습니다.")
        return

    print("  카테고리 목록:")
    for i, cat in enumerate(used_categories, 1):
        count = sum(1 for p in prompts if p["category"] == cat)
        print(f"    {i}. {cat} ({count}개)")

    while True:
        choice = input("\n  번호 선택: ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(used_categories):
                selected = used_categories[num - 1]
                filtered = [p for p in prompts if p["category"] == selected]
                show_list(filtered, f"카테고리: {selected}")
                return
        print("  ⚠️  올바른 번호를 입력해주세요.")


# ── 4. 프롬프트 검색 ─────────────────────────────────────────
def search_prompt():
    print("\n── 프롬프트 검색 ──")

    keyword = input("  검색 키워드: ").strip()
    if not keyword:
        print("  ⚠️  키워드를 입력해주세요.")
        return

    # 제목 또는 내용에 키워드 포함 여부 검색 (대소문자 무시)
    results = [
        p for p in prompts
        if keyword.lower() in p["title"].lower()
        or keyword.lower() in p["content"].lower()
    ]

    if results:
        show_list(results, f"'{keyword}' 검색 결과")
    else:
        print(f"\n  검색 결과가 없습니다. (키워드: '{keyword}')")


# ── 5. 프롬프트 상세 보기 ────────────────────────────────────
def show_detail():
    print("\n── 프롬프트 상세 보기 ──")
    show_list()

    if not prompts:
        return

    while True:
        choice = input("\n  번호 입력 (취소: 0): ").strip()
        if choice == "0":
            return
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(prompts):
                p = prompts[num - 1]
                star = "⭐ 즐겨찾기" if p["favorite"] else "즐겨찾기 없음"
                print("\n" + "=" * 40)
                print(f"  제목    : {p['title']}")
                print(f"  카테고리: {p['category']}")
                print(f"  즐겨찾기: {star}")
                print(f"  내용    :")
                print(f"  {p['content']}")
                print("=" * 40)
                return
        print("  ⚠️  올바른 번호를 입력해주세요.")


# ── 6. 즐겨찾기 관리 ─────────────────────────────────────────
def manage_favorites():
    print("\n── 즐겨찾기 관리 ──")
    print("  1. 즐겨찾기 추가 / 해제")
    print("  2. 즐겨찾기 목록 보기")
    print("  0. 돌아가기")

    choice = input("\n  선택: ").strip()

    if choice == "1":
        toggle_favorite()
    elif choice == "2":
        show_favorites()
    elif choice == "0":
        return
    else:
        print("  ⚠️  올바른 번호를 입력해주세요.")


def toggle_favorite():
    """즐겨찾기 추가/해제"""
    show_list()

    if not prompts:
        return

    while True:
        choice = input("\n  번호 입력 (취소: 0): ").strip()
        if choice == "0":
            return
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(prompts):
                p = prompts[num - 1]
                p["favorite"] = not p["favorite"]  # 토글
                status = "⭐ 즐겨찾기 추가" if p["favorite"] else "즐겨찾기 해제"
                print(f"\n  ✅ '{p['title']}' → {status} 완료!")
                return
        print("  ⚠️  올바른 번호를 입력해주세요.")


def show_favorites():
    """즐겨찾기 목록 보기"""
    favorites = [p for p in prompts if p["favorite"]]
    show_list(favorites, "⭐ 즐겨찾기 목록")


# ── 메인 실행 루프 ───────────────────────────────────────────
def main():
    print("\n  프롬프트 관리 프로그램을 시작합니다!")

    while True:
        show_menu()
        choice = input("  메뉴 선택: ").strip()

        if choice == "1":
            show_list()
        elif choice == "2":
            add_prompt()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            manage_favorites()
        elif choice == "0":
            print("\n  프로그램을 종료합니다. 👋\n")
            break
        else:
            print("\n  ⚠️  올바른 번호를 입력해주세요.")


# ── 프로그램 시작점 ──────────────────────────────────────────
if __name__ == "__main__":
    main()