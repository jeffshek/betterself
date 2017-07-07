import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";

// Have a default seems kind of stupid if you're only going to use it once
const DefaultLineDataset = {
  label: "Sleep Time (Hours)",
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

const ActivitiesAndSleepCorrelationChart = {
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

const SupplementRow = data => {
  // Pretty sure this is not the right way to do this
  const details = data.object;

  return (
    <tr>
      <td>{details[0]}</td>
      <td>{details[1]}</td>
    </tr>
  );
};

class SleepChartsView extends Component {
  constructor() {
    super();
    this.state = {
      sleepHistory: SleepHistoryChart,
      //
      supplementsCorrelationChart: SupplementsAndSleepCorrelationChart,
      selectedCorrelatedSupplements: [],
      selectedCorrelationsSupplementsTab: "Positively Correlated",
      positivelyCorrelatedSupplements: [],
      negativelyCorrelatedSupplements: [],
      //
      selectedCorrelatedUserActivitiesChart: ActivitiesAndSleepCorrelationChart,
      selectedCorrelatedUserActivities: [],
      selectedUserActivitiesCorrelationTab: "Positively Correlated",
      positivelyCorrelatedUserActivities: [],
      negativelyCorrelatedUserActivities: []
    };
    this.selectSupplementsCorrelationTab = this.selectSupplementsCorrelationTab.bind(
      this
    );
    this.selectUserActivitiesCorrelationTab = this.selectUserActivitiesCorrelationTab.bind(
      this
    );
  }

  componentDidMount() {
    this.getHistoricalSleep();
    this.getSupplementsSleepCorrelations();
    this.getActivitiesSleepCorrelations();
  }

  selectSupplementsCorrelationTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    if (name === "Positively Correlated") {
      this.setState({
        selectedCorrelatedSupplements: this.state
          .positivelyCorrelatedSupplements
      });
    } else if (name === "Negatively Correlated") {
      this.setState({
        selectedCorrelatedSupplements: this.state
          .negativelyCorrelatedSupplements
      });
    }

    this.setState({
      selectedCorrelationsSupplementsTab: name
    });
  }

  selectUserActivitiesCorrelationTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    if (name === "Positively Correlated") {
      this.setState({
        selectedCorrelatedUserActivitiesChart: this.state
          .positivelyCorrelatedUserActivities
      });
    } else if (name === "Negatively Correlated") {
      this.setState({
        selectedCorrelatedUserActivitiesChart: this.state
          .negativelyCorrelatedUserActivities
      });
    }

    this.setState({
      selectedUserActivitiesCorrelationTab: name
    });
  }

  //
  // API Calls
  //
  getSupplementsSleepCorrelations() {
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

        this.state.supplementsCorrelationChart.labels = labels;
        this.state.supplementsCorrelationChart.datasets[0].data = dataValues;

        const positivelyCorrelatedSupplements = responseData.filter(data => {
          return data[1] > 0;
        });
        const negativelyCorrelatedSupplements = responseData.filter(data => {
          return data[1] < 0;
        });

        // Finally update state after we've done so much magic
        this.setState({
          supplementsCorrelationChart: this.state.supplementsCorrelationChart,
          selectedCorrelatedSupplements: positivelyCorrelatedSupplements,
          positivelyCorrelatedSupplements: positivelyCorrelatedSupplements,
          negativelyCorrelatedSupplements: negativelyCorrelatedSupplements
        });
      });
  }

  getActivitiesSleepCorrelations() {
    fetch(`api/v1/sleep_activities/user_activities/correlations`, {
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

        this.state.selectedCorrelatedUserActivitiesChart.labels = labels;
        this.state.selectedCorrelatedUserActivitiesChart.datasets[
          0
        ].data = dataValues;

        const positivelyCorrelatedActivities = responseData.filter(data => {
          return data[1] > 0;
        });
        const negativelyCorrelatedActivities = responseData.filter(data => {
          return data[1] < 0;
        });

        // Finally update state after we've done so much magic
        this.setState({
          selectedCorrelatedUserActivitiesChart: this.state
            .supplementsCorrelationChart,
          selectedCorrelatedUserActivities: positivelyCorrelatedActivities,
          positivelyCorrelatedUserActivities: positivelyCorrelatedActivities,
          negativelyCorrelatedUserActivities: negativelyCorrelatedActivities
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

        const dataParsed = sleepDates.map(key => responseData[key] / 60);

        this.state.sleepHistory.labels = sleepDatesFormatted;
        this.state.sleepHistory.datasets[0].data = dataParsed;

        // Reset the historicalState of the graph after the data has been grabbed.
        this.setState({ sleepHistory: this.state.sleepHistory });
      });
  }

  renderSupplementsCorrelationSelectionTab(tabName) {
    if (this.state.selectedCorrelationsSupplementsTab === tabName) {
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
        <NavLink onClick={this.selectSupplementsCorrelationTab} name={tabName}>
          {tabName}
        </NavLink>
      </NavItem>
    );
  }

  renderActivitiesCorrelationSelectionTab(tabName) {
    if (this.state.selectedUserActivitiesCorrelationTab === tabName) {
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
        <NavLink
          onClick={this.selectUserActivitiesCorrelationTab}
          name={tabName}
        >
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

  renderUserActivitiesSleepCorrelation() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Activities and Sleep Correlation
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Bar
                data={ActivitiesAndSleepCorrelationChart}
                options={{
                  maintainAspectRatio: true
                }}
              />
            </div>
          </div>
        </div>
        <div className="float">
          <Nav tabs>
            {this.renderActivitiesCorrelationSelectionTab(
              "Positively Correlated"
            )}
            {this.renderActivitiesCorrelationSelectionTab(
              "Negatively Correlated"
            )}
          </Nav>
          <div className="card">
            <div className="card-block">
              <table className="table">
                <thead>
                  <tr>
                    <th>Activity</th>
                    <th>Correlation</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.selectedCorrelatedUserActivities.map(key => (
                    <SupplementRow key={key} object={key} />
                  ))}
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
            {this.renderSupplementsCorrelationSelectionTab(
              "Positively Correlated"
            )}
            {this.renderSupplementsCorrelationSelectionTab(
              "Negatively Correlated"
            )}
          </Nav>
          <div className="card">
            <div className="card-block">
              <table className="table">
                <thead>
                  <tr>
                    <th>Supplement</th>
                    <th>Correlation</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.selectedCorrelatedSupplements.map(key => (
                    <SupplementRow key={key} object={key} />
                  ))}
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
        {this.renderSupplementsSleepCorrelation()}
        {this.renderUserActivitiesSleepCorrelation()}
        {/*Hold off on Historical Sleep Analytics, No one has 90 Days of History Yet*/}
        {/*{this.renderHistoricalSleepAnalytics()}*/}
      </div>
    );
  }
}

export default SleepChartsView;

// const AverageSleepHistoryChart = {
//   labels: [],
//   datasets: [
//     {
//       label: "Average Sleep (Hours)",
//       backgroundColor: "#193441",
//       borderColor: "rgb(74, 86, 104)",
//       borderWidth: 1,
//       hoverBackgroundColor: "rgba(255,99,132,0.4)",
//       hoverBorderColor: "rgba(255,99,132,1)",
//       data: []
//     }
//   ]
// };

// renderHistoricalSleepAnalytics() {
//   return (
//     <div className="card-columns cols-2">
//       <div className="card">
//         <div className="card-header analytics-text-box-label">
//           Daily Sleep Analytics
//           <div className="card-actions" />
//         </div>
//         <div className="card-block">
//           <div className="chart-wrapper">
//             <Bar
//               data={AverageSleepHistoryChart}
//               options={{
//                 maintainAspectRatio: false
//               }}
//             />
//           </div>
//         </div>
//       </div>
//       <div className="float">
//         <div className="card">
//           <Nav tabs>
//             {this.renderAnalyticsHistorySelectionTab(
//               "Full Historical Lookback"
//             )}
//             {this.renderAnalyticsHistorySelectionTab("7 Day")}
//             {this.renderAnalyticsHistorySelectionTab("14 Day")}
//             {this.renderAnalyticsHistorySelectionTab("30 Day")}
//             {this.renderAnalyticsHistorySelectionTab("90 Day")}
//           </Nav>
//           <div className="card-block">
//             <table className="table">
//               <thead>
//                 <tr>
//                   <th>Weekday</th>
//                   <th>Average Sleep</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 <tr>
//                   <td>Monday</td>
//                   <td>6 hours 53 minutes</td>
//                 </tr>
//               </tbody>
//             </table>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// renderAnalyticsHistorySelectionTab(tabName) {
//   if (this.state.selectedAnalyticsTab === tabName) {
//     return (
//       <NavItem className="selected-modal">
//         <NavLink>
//           {tabName}
//         </NavLink>
//       </NavItem>
//     );
//   }
//   return (
//     <NavItem className="default-background">
//       <NavLink
//         onClick={this.selectAnalyticsHistoryLookbackTab}
//         name={tabName}
//       >
//         {tabName}
//       </NavLink>
//     </NavItem>
//   );
// }

// selectAnalyticsHistoryLookbackTab(event) {
//   event.preventDefault();
//
//   const target = event.target;
//   const name = target.name;
//
//   this.setState({
//     selectedAnalyticsTab: name
//   });
// }
