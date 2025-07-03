import httpx
from core.config import settings


ENDPOINT_URL = settings.AI_URL
THRESHHOLD = settings.NSFW_THRESHHOLD

def calculate_result(result: dict) -> dict:
    '''Тут по ключам нейронку прогнал, так как в этом API параметры NSFW мне не известны. 
    Результат проверил на относительную достоверность.'''
    nsfw_detected = False
    reasons = []

    # 1. Nudity — используем обратное значение `none`
    nudity = result.get("nudity", {})
    if nudity:
        nsfw_score = 1.0 - nudity.get("none", 1.0)
        if nsfw_score > THRESHHOLD:
            nsfw_detected = True
            reasons.append("nudity")

    # 2. Weapon
    weapon_probs = result.get("weapon", {}).get("classes", {})
    if any(prob > THRESHHOLD for prob in weapon_probs.values()):
        nsfw_detected = True
        reasons.append("weapon")

    # 3. Drugs
    if result.get("recreational_drug", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("recreational_drug")

    # 4. Medical (может означать таблетки, шприцы)
    if result.get("medical", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("medical")

    # 5. Offensive
    offensive = result.get("offensive", {})
    if any(prob > THRESHHOLD for prob in offensive.values()):
        nsfw_detected = True
        reasons.append("offensive")

    # 6. Scam
    if result.get("scam", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("scam")

    # 7. Gore
    if result.get("gore", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("gore")

    # 8. Tobacco
    if result.get("tobacco", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("tobacco")

    # 9. Violence
    if result.get("violence", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("violence")

    # 10. Self-harm
    if result.get("self-harm", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("self-harm")

    # 11. Money (потенциальный фрод или реклама)
    if result.get("money", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("money")

    # 12. Gambling
    if result.get("gambling", {}).get("prob", 0) > THRESHHOLD:
        nsfw_detected = True
        reasons.append("gambling")

    return nsfw_detected


async def moderate_image(file_bytes: bytes, filename: str) -> dict:
    '''Для расширяемости приложения определения заголовков
    можно вынести в отдельный декоратор или создать middleware'''
    headers = {
        "models": settings.MODELS,
        "api_secret": settings.API_KEY,
        "api_user": settings.API_USER
    }
    files = {
        "media": (filename, file_bytes, "image/jpeg")
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ENDPOINT_URL, data=headers, files=files)
        response.raise_for_status()
        result = response.json()

    nsfw_content = calculate_result(result)

    if nsfw_content:
        return {
            "status": "REJECTED",
            "reason": "NSFW content"
        }

    return {
        "status": "OK"
    }
