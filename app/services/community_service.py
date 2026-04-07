from datetime import datetime

# In-memory mock DB for Community Posts
mock_db = [
    {
        "id": 1,
        "author": "분리수거왕",
        "title": "투명 페트병 라벨 떼기 꿀팁",
        "content": "페트병 라벨은 물에 살짝 불리면 훨씬 잘 떼어집니다! 다들 참고하세요.",
        "category": "PLASTIC",
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "author": "자취생A",
        "title": "깨진 유리잔 어떻게 버려야 하나요?",
        "content": "어제 컵을 깼는데, 일반 쓰레기로 버리는게 맞나요?",
        "category": "GLASS",
        "created_at": datetime.now()
    }
]
_current_id = 3

class CommunityService:
    @staticmethod
    def get_all_posts() -> list[dict]:
        return sorted(mock_db, key=lambda x: x["created_at"], reverse=True)
        
    @staticmethod
    def create_post(post_data: dict) -> dict:
        global _current_id
        new_post = {
            "id": _current_id,
            **post_data,
            "created_at": datetime.now()
        }
        mock_db.append(new_post)
        _current_id += 1
        return new_post
