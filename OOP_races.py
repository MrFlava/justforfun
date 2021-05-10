from schema import Schema, And, Use, SchemaError


class Car:
    engine_conf = {'turnovers': 200, 'fuel_supply': 200}
    electronics_conf = {'OK': True}

    def __init__(self, driver: dict, driver_conf: Schema, wheels: list,
                 wheel_conf: Schema, engine: dict, engine_conf: Schema,
                 electronics: dict, electronics_conf: Schema) -> None:

        if len(wheels) != 4:
            raise ValueError
        if self._driver_data_validator(data=driver, conf=driver_conf) is True:
            self.driver = driver
        else:
            raise AttributeError

        if self._wheels_data_validator(lst=wheels, conf=wheel_conf) is True:
            self.wheels = wheels
        else:
            raise AttributeError

        if self._engine_data_validator(data=engine, conf=engine_conf) is True:
            self.engine = engine
        else:
            raise AttributeError

        if self._electronics_data_validator(data=electronics, conf=electronics_conf) is True:
            self.electronics = electronics
        else:
            raise AttributeError

    def _driver_data_validator(self, data: dict, conf: Schema) -> bool:
        try:
            conf.validate(data)
            return True
        except SchemaError:
            return False

    def _engine_data_validator(self, data: dict, conf: Schema) -> bool:
        try:
            conf.validate(data)
            return True
        except SchemaError:
            return False

    def _electronics_data_validator(self, data: dict, conf: Schema) -> bool:
        try:
            conf.validate(data)
            return True
        except SchemaError:
            return False

    def _wheels_data_validator(self, lst: list, conf: Schema) -> bool:
        for wheel in lst:
            try:
                conf.validate(wheel)
                return True
            except SchemaError:
                return False

    def show_driver_info(self) -> str:
        return f" Driver's card\n " \
               f"Name: {self.driver.get('name')} , " \
               f"Skills rate: {self.driver.get('skills')} ," \
               f"Age: {self.driver.get('age')}"

    def show_wheels_info(self) -> str:
        s = "Wheels data \n"
        for wheel in self.wheels:
            s += f"Wheel brand: {wheel.get('wheel_brand')} ," \
                 f" Diameter: {wheel.get('diameter')} ," \
                 f" Quality: {wheel.get('quality')} \n"

        return s

    def show_engine_info(self) -> str:
        return f" Engine data\n " \
               f"Turnovers: {self.engine.get('turnovers')} ," \
               f"Fuel supply: {self.engine.get('fuel_supply')}/1000"

    def show_electronics_info(self) -> str:
        return f" Electronics data\n " \
               f"OK: {self.electronics.get('OK')} "


c = Car(driver={'skills': 0, 'name': 'John Johnson', 'age': 18},
        driver_conf=Schema({'skills': And(Use(int)), 'name': And(Use(str)), 'age': And(Use(int))}), wheels=[
                                                                      {'wheel_brand': 'Michelin',
                                                                       'diameter': 20, 'quality': 1},
                                                                      {'wheel_brand': 'Michelin',
                                                                       'diameter': 20, 'quality': 1},
                                                                      {'wheel_brand': 'Michelin',
                                                                       'diameter': 20, 'quality': 1},
                                                                      {'wheel_brand': 'Michelin',
                                                                       'diameter': 20, 'quality': 1}],
        wheel_conf=Schema({'wheel_brand': And(Use(str)), 'diameter': And(Use(int)), 'quality': And(Use(int))}),
        engine={'turnovers': 200, 'fuel_supply': 200}, engine_conf=Schema({'turnovers': And(Use(int)),
                                                                           'fuel_supply': And(Use(int))}),
        electronics={'OK': True}, electronics_conf=Schema({'OK': And(Use(bool))}))


print(c.show_driver_info())
print(c.show_wheels_info())
print(c.show_engine_info())
print(c.show_electronics_info())

"""
stuff for the  future
"""
# class Road