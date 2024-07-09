import httpx
from bs4 import BeautifulSoup


async def get_3_tags(nickname):
    url = f'https://solved.ac/profile/{nickname}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 tbody 태그를 찾고 두 번째 tbody 요소를 선택
    tbody_tags = soup.find_all('tbody')

    if len(tbody_tags) < 2:
        raise Exception('Expected at least 2 tbody elements')

    second_tbody = tbody_tags[1]

    # 두 번째 tbody에서 모든 tr 태그를 선택하여 태그 리스트를 만듦
    tags = []
    tr_tags = second_tbody.find_all('tr')

    for tr in tr_tags:
        td_tags = tr.find_all('td')
        if td_tags:
            tag_text = td_tags[0].get_text(strip=True)
            tags.append(tag_text[1:])  # 첫 글자 제거 후 추가

    # 상위 3개 태그와 하위 3개 태그 선택
    top_3_tags = tags[:3]
    bottom_3_tags = tags[-3:]

    return top_3_tags, bottom_3_tags


async def get_solved_list(boj_username: str) -> list[str]:
    url = f'https://acmicpc.net/user/{boj_username}'  # HTTPS로 수정

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Failed to retrieve the page, status code: {response.status_code}')

    soup = BeautifulSoup(response.text, 'html.parser')

    # 문제 리스트가 있는 div를 찾기
    problem_list_div = soup.select_one('body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div.panel-body > div.problem-list')

    if not problem_list_div:
        raise Exception('Problem list not found')

    # 문제 리스트를 리스트 자료구조로 담기
    problems = [problem.get_text(strip=True) for problem in problem_list_div.find_all('a')]

    return problems