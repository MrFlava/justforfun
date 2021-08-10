import React from "react";

import Info from "./components/info";
import Form from "./components/form";
import Weather from "./components/weather";

const API_KEY = "e8a16cf3e04b48da54db2d22392ce2b1";

class App extends React.Component {

  state = {
    temp: undefined,
    city: undefined,
    country: undefined,
    sunrise: undefined,
    sunset: undefined,
    error: undefined
  }
  
  gettingWeather = async (event) => {
    event.preventDefault();
    let city = event.target.elements.city.value;
    if (city) {
      const api_url = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`);
      const data = await api_url.json();

      let sunrise = data.sys.sunrise;
      let date_sunrise = new Date();
      date_sunrise.setTime(sunrise);
      let sunrise_date = date_sunrise.getHours() + ":" + date_sunrise.getMinutes() + ":" + date_sunrise.getSeconds();


      let sunset = data.sys.sunset;
      let date_sunset = new Date();
      date_sunset.setTime(sunset);
      let sunset_date = date_sunset.getHours() + ":" + date_sunset.getMinutes() + ":" + date_sunset.getSeconds();

      this.setState({
        temp: data.main.temp,
        city: data.name,
        country: data.sys.country,
        sunrise: sunrise_date,
        sunset: sunset_date,
        error: ""
      });
    }
  }

  render() {
    return (
      <div>
        <Info />
        <Form weatherMethod={this.gettingWeather} />
        <Weather 
          temp={this.state.temp}
          city={this.state.city}
          country={this.state.country}
          sunrise={this.state.sunrise}
          sunset={this.state.sunset}
          error={this.state.error}
        />
      </div>
      );
  }
}

export default App;