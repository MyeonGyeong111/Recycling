import io
from PIL import Image
from transformers import pipeline

# Load ML model in global scope so it only loads once
print("Loading HuggingFace ML Model (this may take a moment)...")
try:
    # yangy50/garbage-classification is a lightweight classification model for trash
    classifier = pipeline("image-classification", model="yangy50/garbage-classification")
except Exception as e:
    print(f"Failed to load model: {e}")
    classifier = None

class RecycleService:
    @staticmethod
    async def predict_image(image_bytes: bytes) -> dict:
        if classifier is None:
            return {"category": "ERROR", "confidence": 0.0, "message": "ML 모델을 불러오는 데 실패했습니다."}
            
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            # Hugging Face model prediction
            predictions = classifier(image)
            top_pred = predictions[0] # List sorted by highest score
            
            label_lower = top_pred["label"].lower()
            confidence = float(top_pred["score"])
            
            # Map predictions to internal API categories
            category = "GENERAL"
            if "plastic" in label_lower:
                category = "PLASTIC"
            elif "glass" in label_lower:
                category = "GLASS"
            elif "paper" in label_lower or "cardboard" in label_lower:
                category = "PAPER"
            elif "metal" in label_lower or "can" in label_lower:
                category = "CAN"
            
            accuracy = f"{int(confidence * 100)}%"
            msg = f"AI가 쓰레기를 '{top_pred['label']}'(으)로 인식했습니다! (확신도 {accuracy})"
            return {
                "category": category,
                "confidence": confidence,
                "message": msg
            }
        except Exception as e:
            return {"category": "ERROR", "confidence": 0.0, "message": f"인식 중 오류 발생: {str(e)}"}
        
    @staticmethod
    def get_category_info(category: str) -> dict:
        info_db = {
            "PLASTIC": {
                "category": "PLASTIC",
                "description": "플라스틱류 (생수병, 음료수병 등)",
                "how_to_recycle": "내용물을 비우고 물로 행군 후, 상표 및 뚜껑을 제거하여 압착해서 배출합니다. 투명 페트병은 별도 분리 배출합니다."
            },
            "PAPER": {
                "category": "PAPER",
                "description": "종이류 (신문지, 박스, 책자 등)",
                "how_to_recycle": "물기에 젖지 않게 하고 테이프, 철핀 등의 이물질을 제거한 후 끈으로 묶어 배출합니다."
            },
            "GLASS": {
                "category": "GLASS",
                "description": "유리병류 (음료수병, 기타 병류)",
                "how_to_recycle": "내용물을 비우고 물로 행군 후 배출합니다. 깨진 유리는 전용 포대나 신문지로 싸서 종량제 봉투에 담아 버려야 합니다."
            },
            "VINYL": {
                "category": "VINYL",
                "description": "비닐류 (라면봉지, 과자봉지, 뽁뽁이 등)",
                "how_to_recycle": "내부가 보이도록 투명한 봉투에 담아 분리 배출합니다. 음식물이 묻은 경우 물로 헹궈내야 합니다."
            },
            "CAN": {
                "category": "CAN",
                "description": "캔류 (음료수 캔, 통조림 캔 등)",
                "how_to_recycle": "내용물을 비우고 물로 헹군 후 찌그러뜨려서 배출합니다."
            },
            "GENERAL": {
                "category": "GENERAL",
                "description": "일반쓰레기",
                "how_to_recycle": "종량제 봉투에 담아 배출합니다."
            }
        }
        return info_db.get(category.upper(), info_db["GENERAL"])
        
    @staticmethod
    def get_guidelines_for_location(location_data: dict) -> dict:
        # Mocking external API call / Database Query
        address = location_data.get("address", "")
        # Very basic mock location matching
        if "관악구" in address:
            return {
                "jurisdiction": "서울특별시 관악구",
                "website_url": "https://www.gwanak.go.kr/site/gwanak/ex/bbs/List.do?cbIdx=180",
                "contact_number": "02-879-6200"
            }
        elif "송파구" in address:
            return {
                "jurisdiction": "서울특별시 송파구",
                "website_url": "https://www.songpa.go.kr/www/contents.do?key=2621",
                "contact_number": "02-2147-3800"
            }
        else:
            return {
                "jurisdiction": "서울특별시 강남구 (기본값)",
                "website_url": "https://www.gangnam.go.kr/contents/clean_environ/1/view.do",
                "contact_number": "02-3423-5114"
            }
