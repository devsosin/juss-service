import random
import time
from datetime import datetime

banks = [
    "KB국민은행",
    "신한은행",
    "하나은행",
    "우리은행",
    "NH농협은행",
    "기업은행",
    "SC제일은행",
    "한국씨티은행",
    "부산은행",
    "대구은행",
    "광주은행",
    "전북은행",
    "제주은행"
]

deposit_names = {'KB국민': ['KB마이핏통장', 'KB스타클럽통장', 'KB골든라이프통장', 'KB굿잡통장'],
 '신한': ['신한 쏠(SOL)', '신한 마이카 통장', '신한 미래설계통장'],
 '하나': ['하나 원큐통장', '하나머니세상통장', '하나골드클럽통장'],
 '우리': ['우리 WON통장', '우리사랑통장', '우리WON멤버스통장'],
 'NH농협': ['NH올원통장', 'NH멤버스통장', 'NH행복채움통장'],
 '기업': ['기업 i-ONE통장', '기업 BIZ통장', '기업 법인통장'],
 'SC제일': ['SC제일 마이플러스통장', 'SC제일 다이렉트통장', 'SC제일 유니통장'],
 '한국씨티': ['씨티 클리어통장', '씨티 글로벌통장', '씨티 우대통장'],
 '대구': ['대구 스마트통장', '대구 i-ONE통장', '대구 해피투게더통장'],
 '부산': ['부산 썸통장', '부산 해피드림통장', '부산 BNK퍼스트통장']}

saving_names = {
    "KB국민": ["KB마이핏적금", "KB특★한적금", "KB청년내일저축계좌", "KB플러스정기적금"],
    "신한": ["신한 쏠(SOL)적금", "신한카드연계적금", "신한 미래설계적금", "신한 S드림적금"],
    "하나": ["하나 원큐적금", "하나머니세상적금", "하나골드클럽적금", "하나 청년희망적금"],
    "우리": ["우리 WON적금", "우리사랑적금", "우리WON멤버스적금", "우리 청년적금"],
    "NH농협": ["NH올원적금", "NH멤버스적금", "NH행복채움적금", "NH농협청년희망적금"],
    "기업": ["기업 i-ONE적금", "기업 BIZ적금", "기업 법인적금", "기업 성공노하우적금"],
    "SC제일": ["SC제일 마이플러스적금", "SC제일 다이렉트적금", "SC제일 유니적금", "SC제일 플러스적금"],
    "한국씨티": ["씨티 클리어적금", "씨티 글로벌적금", "씨티 우대적금", "씨티 목돈마련적금"],
    "대구": ["대구 스마트적금", "대구 i-ONE적금", "대구 해피투게더적금", "대구 청년우대적금"],
    "부산": ["부산 썸적금", "부산 해피드림적금", "부산 BNK퍼스트적금", "부산 목돈만들기적금"]
}
# Define the banks and their respective card names, ensuring they seem realistic
card_names = {
    "KB국민": ["KB국민 청춘대로 카드", "KB국민 스마트페이 카드", "KB국민 해피라이프 카드"],
    "신한": ["신한 더 클래식 카드", "신한 올댓 쇼핑 카드", "신한 러브 플러스 카드"],
    "하나": ["하나 1Q Pay 카드", "하나 머니세상 체크카드", "하나 Gold Rush 카드"],
    "우리": ["우리 WON카드", "우리 V-클럽 카드", "우리 The Best 카드"],
    "NH농협": ["NH농협 올원 체크카드", "NH농협 행복스토리 카드", "NH농협 하나로 클럽카드"],
    "기업": ["기업 IBK ONE 카드", "기업 디지털 포인트 카드", "기업 The Premier 카드"],
    "SC제일": ["SC제일 프리미어 다이빙 카드", "SC제일 마일리지 적립 카드", "SC제일 우수고객 전용 카드"],
    "한국씨티": ["한국씨티 프리미엄 마일 카드", "한국씨티 클리어 포인트 카드", "한국씨티 글로벌 월렛 카드"],
    "대구": ["대구은행 IM 체크카드", "대구은행 드림스타트 카드", "대구은행 스마트플러스 카드"],
    "부산": ["부산은행 B-First 카드", "부산은행 해양스포츠 카드", "부산은행 Young 파워 체크카드"]
}


# Function to generate random account number
def generate_account_number():
    return f"{random.randint(100, 999):03}-{random.randint(0, 99):02}-{random.randint(10000, 99999):05}"

# Function to generate random phone number
def generate_phone_number():
    return f"010-{random.randint(1000, 9999):04}-{random.randint(1000, 9999):04}"

# Define Korean first (given) name syllables
first_syllables = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
middle_syllables = ["민", "서", "은", "지", "현", "영", "우", "수", "미", "태"]
last_syllables = ["준", "아", "호", "유", "린", "하", "영", "우", "빈", "도"]

# Function to generate a random Korean name with three syllables
def generate_korean_name():
    first = random.choice(first_syllables)
    middle = random.choice(middle_syllables)
    last = random.choice(last_syllables)
    return first + middle + last

def make_accounts():
    # Generate 10 random accounts
    random_accounts = []

    for _ in range(9):
        account_type = random.randint(0, 1) 
        while True:
            try:
                bank_index = random.randint(0, len(banks) - 1)
                bank_name = banks[bank_index]
                if account_type == 0:
                    account_name = random.choice(deposit_names[bank_name[:-2]])
                else:
                    account_name = random.choice(saving_names[bank_name[:-2]])
                break
            except:...
            
        account_number = generate_account_number()
        
        balance = random.randint(100000, 100000000)  # Balance between 십만 ~ 1억

        random_accounts.append({
            'account_type': account_type,
            'bank_name': bank_name,
            'account_name': account_name,
            'account_number': account_number,
            'balance': balance,
        })
    
    # 해당 유저의 phone 번호로 된 계좌 생성 1개 - 잔액 X 은행이름 X
    account_name = generate_korean_name()
    account_number = generate_phone_number()
    random_accounts.append({
        'account_type': 2,
        'bank_name': '',
        'account_name': account_name,
        'account_number': account_number,
        'balance': 0,
    })

    return random_accounts

# Function to generate min_usage either as 0 or within the range 200,000 to 300,000 in 50,000 steps
def generate_min_usage():
    return random.choice([0, 200000, 250000, 300000])

def make_cards():
    # Select 3 random banks and their cards for the example
    selected_banks = random.sample(list(card_names.keys()), 3)

    # Generate 3 cards based on the selected banks
    cards = []

    for bank in selected_banks:
        card_name = random.choice(card_names[bank])
        cards.append({
            'card_name': card_name,
            'min_usage': generate_min_usage(),
        })

    return cards

def make_transaction(receiver, sender):    
    # Memo options for different account types
    memos = {
        0: ["식비 결제", "교통비 결제", "쇼핑 결제", "유틸리티 비용 결제", "온라인 구독료 결제",
            "카페 결제", "도서 구매", "영화 티켓 구매", "외식 비용", "휴대폰 요금 결제"],
        1: ["정기 저축", "목돈 마련 저축", "비상금 적립", "휴가비 저축", "자동차 구매 저축",
            "주택 구입 저축", "노후 대비 저축", "자녀 교육비 저축", "투자 목적 저축", "결혼자금 저축"],
        2: ["생일 선물 송금", "결혼 축하금 송금", "돌잔치 축하금", "장학금 지원", "생활비 지원",
            "부모님 용돈", "친구 빚 상환", "여행 경비 분담", "공동 구매 비용", "기부금 송금"]
    }
    amount = random.randint(1000, 5000000)
    memo = random.choice(memos[sender.account_type])
    card_id = None
    if not sender.account_type and sender.card_id:
        card_id = sender.card_id
    # Placeholder logic for 'is_fill'
    is_fill = False # This should be determined by your application logic
    
    # Create and return the transaction
    rd_time = datetime.fromtimestamp(time.time() - float(random.random() * (60*60*24*60)))
    
    transaction = {
        'receiver_id': receiver,
        'sender_id': sender.id,
        'amount': amount,
        'memo': memo,
        'card_id': card_id,
        'is_fill': is_fill, # receiver가 내 계좌인 경우 근데 이건 만들때는 상관없을듯?
        'created_at': rd_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return transaction


def make_transactions(accounts, others):
    transaction_list = []
    for account in accounts:
        transaction_list.extend( [make_transaction(random.choice(others), account) for _ in range(9)] )

    return transaction_list