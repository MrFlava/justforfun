from schema import Schema, And, Use, SchemaError


class Car:

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

    def wheels_prepared_for_race_checking(self) -> bool:
        prepared = True
        for wheel in self.wheels:
            if wheel.get('quality') == 0:
                prepared = False
        return prepared

    def fuel_tank_prepared_for_race_checking(self) -> bool:
        prepared = True
        if self.engine.get('fuel_supply') < 1:
            prepared = False
        return prepared

    def electronics_prepared_for_race_checking(self) -> bool:
        prepared = True
        if self.electronics.get('OK') is not True:
            prepared = False
        return prepared

    def show_driver_info(self) -> str:
        return f"Driver's card\n " \
               f" Name: {self.driver.get('name')} , " \
               f" Skills rate: {self.driver.get('skills')} ," \
               f" Age: {self.driver.get('age')}"

    def show_wheels_info(self) -> str:
        s = "Wheels data \n"
        for wheel in self.wheels:
            s += f" Wheel brand: {wheel.get('wheel_brand')} ," \
                 f" Diameter: {wheel.get('diameter')} ," \
                 f" Quality: {wheel.get('quality')} \n"

        if self.wheels_prepared_for_race_checking() is False:
            s += "Attention! \n" \
                 " One of the wheels has bad quality. The car isn't prepared for the racing. \n"

        return s

    def show_engine_info(self) -> str:
        s = f"Engine data\n " \
            f"Turnovers: {self.engine.get('turnovers')} ," \
            f"Fuel supply: {self.engine.get('fuel_supply')}/1000 \n"

        if self.fuel_tank_prepared_for_race_checking() is False:
            s += "Attention! \n" \
                 " Fuel tank capacity is not enough for stable engine working. The car isn't prepared for the racing.\n"
        return s

    def show_electronics_info(self) -> str:
        s = f"Electronics data\n " \
               f" OK: {self.electronics.get('OK')} \n"

        if self.electronics_prepared_for_race_checking() is False:
            s += "Attention! \n" \
                 "Electronics is damaged. The car isn't prepared for the racing.\n"

        return s


c = Car(driver={'skills': 50, 'name': 'John Johnson', 'age': 18},
        driver_conf=Schema({'skills': And(Use(int)), 'name': And(Use(str)), 'age': And(Use(int))}), wheels=[
        {'wheel_brand': 'Michelin',
         'diameter': 20, 'quality': 1},
        {'wheel_brand': 'Michelin',
         'diameter': 20, 'quality': 1},
        {'wheel_brand': 'Michelin',
         'diameter': 20, 'quality': 1},
        {'wheel_brand': 'Michelin',
         'diameter': 20, 'quality': 1}],
        wheel_conf=Schema({'wheel_brand': And(Use(str)), 'diameter': And(Use(int)), 'quality': And(Use(float))}),
        engine={'turnovers': 200, 'fuel_supply': 1}, engine_conf=Schema({'turnovers': And(Use(int)),
                                                                         'fuel_supply': And(Use(float))}),
        electronics={'OK': False}, electronics_conf=Schema({'OK': And(Use(bool))}))

print(c.show_driver_info())
print(c.show_wheels_info())
print(c.show_engine_info())
print(c.show_electronics_info())

"""
stuff for the  future
"""
# class Road(Car):
