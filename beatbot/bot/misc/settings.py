from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    WEB_HOST: str
    WEB_PORT: int
    WEB_TIMEOUT: int
    WEB_MAX_CONNECTIONS: int

    WEB_GENERATOR_HOST: str
    WEB_GENERATOR_PORT: int

    YOOKASSA_SHOP_ID: int
    YOOKASSA_SECRET_KEY: str
    YOOKASSA_CLIENT_SECRET: str

    IP_ADDRESS: str

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def bot_token(self) -> str:
        return self.BOT_TOKEN

    @property
    def web_config(self) -> dict:
        return {'host': self.WEB_HOST,
                'port': self.WEB_PORT,
                'timeout': self.WEB_TIMEOUT,
                'max_connections': self.WEB_MAX_CONNECTIONS,

                }

    @property
    def generator_url(self) -> str:
        return f"http://{self.WEB_GENERATOR_HOST}:{self.WEB_GENERATOR_PORT}"

    @property
    def yookassa_data(self):
        return {'shop_id': self.YOOKASSA_SHOP_ID,
                'key': self.YOOKASSA_SECRET_KEY,
                'client_secret': self.YOOKASSA_CLIENT_SECRET}



settings = Settings(_env_file='.env')
