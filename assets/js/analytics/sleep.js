import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";

const line = {
  labels: [
    "3/31/17",
    "(S) 4/1/17",
    "4/2/17",
    "4/3/17",
    "4/4/17",
    "4/5/17",
    "4/6/17",
    "(S) 4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17",
    "4/6/17"
  ],
  datasets: [
    {
      label: "Sleep Time (Hours)",
      fill: false,
      lineTension: 0.1,
      backgroundColor: "rgb(74, 86, 104)",
      borderColor: "rgb(74, 86, 104)",
      borderCapStyle: "butt",
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: "miter",
      pointBorderColor: "black",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(75,192,192,1)",
      pointHoverBorderColor: "black",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40
      ]
    }
  ]
};

const bar = {
  labels: [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
  ],
  datasets: [
    {
      label: "Average Sleep (Hours)",
      // # rgb(66, 134, 244)
      backgroundColor: "rgb(74, 86, 104)",
      borderColor: "rgb(74, 86, 104)",
      borderWidth: 1,
      hoverBackgroundColor: "rgba(255,99,132,0.4)",
      hoverBorderColor: "rgba(255,99,132,1)",
      data: [65, 59, 80, 81, 56, 55, 40]
    }
  ]
};

const bar_2 = {
  labels: [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
  ],
  datasets: [
    {
      label: "Average Sleep (Hours)",
      backgroundColor: "rgb(74, 86, 104)",
      borderColor: "rgb(74, 86, 104)",
      borderWidth: 1,
      hoverBackgroundColor: "rgba(255,99,132,0.4)",
      hoverBorderColor: "rgba(255,99,132,1)",
      data: [65, 59, 80, 81, 56, 55, 40]
    }
  ]
};

class Charts extends Component {
  render() {
    return (
      <div className="animated fadeIn">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Sleep History
            <div className="card-actions" />
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Line
                data={line}
                options={{
                  maintainAspectRatio: false
                }}
              />
            </div>
          </div>
        </div>

        <div className="card-columns cols-2">
          <div className="card">
            <div className="card-header analytics-text-box-label">
              Daily Sleep Analytics
              <div className="card-actions" />
            </div>
            <div className="card-block">
              <div className="chart-wrapper">
                <Bar
                  data={bar}
                  options={{
                    maintainAspectRatio: false
                  }}
                />
              </div>
            </div>
          </div>
          <div className="float-left">
            <div className="card">
              <div className="card-header analytics-text-box">
                Sleep Statistics (Averages)
              </div>
              <div className="card-block">
                <span className="analytics-text-box">Historical :</span>
                {" "}
                7 hours 51 minutes
                <br />
                <span className="analytics-text-box">Last 15 Days : </span>
                {" "}
                6 hours 28 minutes
                <br />
                <span className="analytics-text-box">Last 30 Days : </span>
                {" "}
                6 hours 28 minutes
                <br />
                <span className="analytics-text-box">Last 60 Days : </span>
                {" "}
                6 hours 55 minutes
                <br />
                <span className="analytics-text-box">Weekends :</span>
                {" "}
                6 hours 28 minutes
                <br />
                <span className="analytics-text-box">Weekdays :</span>
                {" "}
                6 hours 28 minutes
              </div>
            </div>
          </div>
        </div>

        <div className="card-columns cols-2">
          <div className="card">
            <div className="card-header analytics-text-box-label">
              Activities and Sleep Correlation
            </div>
            <div className="card-block">
              <div className="chart-wrapper">
                <Bar
                  data={bar_2}
                  options={{
                    maintainAspectRatio: true
                  }}
                />
              </div>
            </div>
          </div>
          <div className="float-left">
            <Nav tabs>
              <div className="selected-modal">
                <NavItem>
                  <NavLink>
                    Positively Correlated
                  </NavLink>
                </NavItem>
              </div>
              <div className="default-background">
                <NavItem>
                  <NavLink>
                    Negatively Correlated
                  </NavLink>
                </NavItem>
              </div>
            </Nav>
            <div className="card">
              <div className="card-block">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Activity</th>
                      <th>Date Created</th>
                      <th>Correlation</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Samppa Nori</td>
                      <td>2012/01/01</td>
                      <td>Member</td>
                    </tr>
                    <tr>
                      <td>Estavan Lykos</td>
                      <td>2012/02/01</td>
                      <td>Staff</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Charts;
