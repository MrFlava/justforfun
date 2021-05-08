class Car:

    def __init__(self, driver: dict, wheels: list, engine: dict, electronics: dict) -> None:
        if len(wheels) != 4:
            raise ValueError

        self.driver = driver
        self.wheels = wheels
        self.engine = engine
        self.electronics = electronics

    def show_driver_info(self):
        return f" Driver's card\n " \
               f"Name: {self.driver.get('name')} , " \
               f"Skills rate: {self.driver.get('skills')} ," \
               f"Age: {self.driver.get('age')}"

    def show_wheels_info(self):
        s = "Wheels data \n"
        for wheel in self.wheels:
            s += f"Wheel brand: {wheel.get('wheel_brand')} ," \
                 f" Diameter: {wheel.get('diameter')} ," \
                 f" Quality: {wheel.get('quality')} \n"

        return s

    def show_engine_info(self):
        return f" Engine data\n " \
               f"Turnovers: {self.engine.get('turnovers')} ," \
               f"Fuel supply: {self.engine.get('fuel_supply')}/1000"

    def show_electronics_info(self):
        return f" Electronics data\n " \
               f"OK: {self.electronics.get('OK')} "


c = Car(driver={'skills': 0, 'name': 'John Johnson', 'age': 18}, wheels=[{'wheel_brand': 'Michelin',
                                                                          'diameter': 20, 'quality': 1},
                                                                         {'wheel_brand': 'Michelin',
                                                                          'diameter': 20, 'quality': 1},
                                                                         {'wheel_brand': 'Michelin',
                                                                          'diameter': 20, 'quality': 1},
                                                                         {'wheel_brand': 'Michelin',
                                                                          'diameter': 20, 'quality': 1}],
        engine={'turnovers': 200, 'fuel_supply': 200},
        electronics={'OK': True})

print(c.show_driver_info())
print(c.show_wheels_info())
print(c.show_engine_info())
print(c.show_electronics_info())


"""
stuff for the  future
"""
# if not driver:
#     driver = {'skills': 0, 'name': None, 'age': 18}

# if isinstance(driver, dict) and isinstance(conf, dict):
# struct is a dict of types or other dicts
# return all(k in conf and check_structure(struct[k], conf[k]) for k in struct
