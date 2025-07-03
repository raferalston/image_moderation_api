from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    '''
    Конфигурация приложения:
    
    API_KEY: str
        Ключ API для доступа к внешнему сервису модерации.
    API_USER: str
        Имя пользователя или идентификатор для API.
    NSFW_THRESHHOLD: float
        Пороговое значение (от 0 до 1) для определения контента как NSFW (по умолчанию 0.5).
    MODELS: str
        Список моделей, используемых для анализа контента (через запятую).
    AI_URL: str
        URL-адрес внешнего API для проверки контента.
    '''
    API_KEY: str
    API_USER: str
    NSFW_THRESHHOLD: float = 0.5
    MODELS: str = 'nudity-2.1,weapon,recreational_drug,medical,properties,type,quality,offensive-2.0,faces,scam,text-content,face-attributes,gore-2.0,text,qr-content,tobacco,genai,violence,self-harm,money,gambling'
    AI_URL: str = 'https://api.sightengine.com/1.0/check.json'
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()
