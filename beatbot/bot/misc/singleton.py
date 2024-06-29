class SingletonMeta(type):
    """
    Метакласс Singleton используется для обеспечения того, что класс имеет только один экземпляр.
    Это обеспечивает глобальную точку доступа к этому экземпляру, что может быть полезно для вещей,
    которые должны быть глобально доступны, как подключение к базе данных.
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
