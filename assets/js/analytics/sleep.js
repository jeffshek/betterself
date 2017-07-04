import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";

// Have a default seems kind of stupid if you're only going to use it once
const DefaultLineDataset = {
  label: "Sleep Time (Minutes)",
  fill: false,
  lineTension: 0.1,
  backgroundColor: "#193441",
  borderColor: "#193441",
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
  data: []
};

const SleepHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineDataset)]
};

const AverageSleepHistoryChart = {
  labels: [],
  datasets: [
    {
      label: "Average Sleep (Hours)",
      backgroundColor: "#193441",
      borderColor: "rgb(74, 86, 104)",
      borderWidth: 1,
      hoverBackgroundColor: "rgba(255,99,132,0.4)",
      hoverBorderColor: "rgba(255,99,132,1)",
      data: []
    }
  ]
};

const SupplementsAndSleepCorrelationChart = {
  labels: [],
  datasets: [
    {
      label: "Sleep Correlation",
      backgroundColor: "#193441",
      borderColor: "#193441",
      borderWidth: 1,
      hoverBackgroundColor: "rgba(255,99,132,0.4)",
      hoverBorderColor: "rgba(255,99,132,1)",
      data: []
    }
  ]
};

class ChartsView extends Component {
  constructor() {
    super();
    this.state = {
      sleepHistory: SleepHistoryChart,
      supplementsCorrelation: SupplementsAndSleepCorrelationChart,
      selectedAnalyticsTab: "Full Historical Lookback"
    };
    this.selectAnalyticsHistoryLookback = this.selectAnalyticsHistoryLookback.bind(
      this
    );
    this.renderAnalyticsHistorySelectionTab = this.renderAnalyticsHistorySelectionTab.bind(
      this
    );
  }

  selectAnalyticsHistoryLookback(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    this.setState({
      selectedAnalyticsTab: name
    });
  }

  getActivitiesSleepCorrelations() {
    fetch(`api/v1/sleep_activities/supplements/correlations`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const labels = responseData.map(data => {
          return data[0];
        });
        const dataValues = responseData.map(data => {
          return data[1];
        });

        this.state.supplementsCorrelation.labels = labels;
        this.state.supplementsCorrelation.datasets[0].data = dataValues;

        this.setState({
          supplementsCorrelation: this.state.supplementsCorrelation
        });
      });
  }

  getHistoricalSleep() {
    fetch(`api/v1/sleep_activities/aggregates`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // Sort by datetime
        const sleepDates = Object.keys(responseData);
        sleepDates.sort();

        const sleepDatesFormatted = sleepDates.map(key =>
          moment(key).format("MMMM D YYYY")
        );

        const dataParsed = sleepDates.map(key => responseData[key]);

        this.state.sleepHistory.labels = sleepDatesFormatted;
        this.state.sleepHistory.datasets[0].data = dataParsed;

        // Reset the historicalState of the graph after the data has been grabbed.
        this.setState({ sleepHistory: this.state.sleepHistory });
      });
  }

  componentDidMount() {
    this.getHistoricalSleep();
    this.getActivitiesSleepCorrelations();
  }

  renderAnalyticsHistorySelectionTab(tabName) {
    if (this.state.selectedAnalyticsTab === tabName) {
      return (
        <NavItem className="selected-modal">
          <NavLink>
            {tabName}
          </NavLink>
        </NavItem>
      );
    }
    return (
      <NavItem className="default-background">
        <NavLink onClick={this.selectAnalyticsHistoryLookback} name={tabName}>
          {tabName}
        </NavLink>
      </NavItem>
    );
  }

  renderSleepHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          Sleep History
          <div className="card-actions" />
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Line
              data={this.state.sleepHistory}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  renderHistoricalSleepAnalytics() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Daily Sleep Analytics
            <div className="card-actions" />
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Bar
                data={AverageSleepHistoryChart}
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
              {this.renderAnalyticsHistorySelectionTab(
                "Full Historical Lookback"
              )}
              {this.renderAnalyticsHistorySelectionTab("7 Day")}
              {this.renderAnalyticsHistorySelectionTab("14 Day")}
              {this.renderAnalyticsHistorySelectionTab("30 Day")}
              {this.renderAnalyticsHistorySelectionTab("90 Day")}
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
    );
  }

  renderSupplementsSleepCorrelation() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Supplements and Sleep Correlation
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Bar
                data={SupplementsAndSleepCorrelationChart}
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
    );
  }

  render() {
    return (
      <div className="animated fadeIn">
        {this.renderSleepHistoryChart()}
        {this.renderHistoricalSleepAnalytics()}
        {this.renderSupplementsSleepCorrelation()}
      </div>
    );
  }
}

export default ChartsView;
