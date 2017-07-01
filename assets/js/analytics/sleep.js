import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";

const DefaultLineChartParameters = {
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
  data: [195, 2, 5, 65, 33, 62]
};

const line = {
  labels: ["3/31/17", "3/31/27", "3/31/37"],
  datasets: [Object.assign({}, DefaultLineChartParameters)]
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
  constructor() {
    super();
    this.state = {
      line: line
    };
    this.state.line.labels = ["January", "Feb", 3, 4, 5, 6];
  }

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
                data={this.state.line}
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
          <div className="float">

            <div className="card">
              <Nav tabs>
                <NavItem className="selected-modal">
                  <NavLink>
                    Full Historical Lookback
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink>
                    7 Day
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink>
                    14 Day
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink>
                    30 Day
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink>
                    90 Day
                  </NavLink>
                </NavItem>
              </Nav>
              <div className="card-block">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Weekday</th>
                      <th>Average Sleep</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Monday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Tuesday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Wednesday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Thursday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Friday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Saturday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                    <tr>
                      <td>Sunday</td>
                      <td>6 hours 53 minutes</td>
                    </tr>
                  </tbody>
                </table>
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
          <div className="float">
            <Nav tabs>
              <div className="selected-modal">
                <NavItem>
                  <NavLink>
                    Positively Correlated Activities
                  </NavLink>
                </NavItem>
              </div>
              <div className="default-background">
                <NavItem>
                  <NavLink>
                    Negatively Correlated Activities
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
