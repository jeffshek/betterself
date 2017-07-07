import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";

// Have a default seems kind of stupid if you're only going to use it once
const DefaultLineDataset = {
  label: "",
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

const SupplementsCorrelationsChart = {
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

const ActivitiesCorrelationsChart = {
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
      <td>{details[1].toFixed(3)}</td>
    </tr>
  );
};

class SleepAnalyticsView extends Component {
  constructor() {
    super();
    this.state = {
      sleepHistory: SleepHistoryChart,
      //
      supplementsCorrelationsChart: SupplementsCorrelationsChart,
      selectedSupplementsCorrelations: [],
      selectedSupplementsCorrelationsTab: "Positively Correlated",
      positiveSupplementsCorrelations: [],
      negativeSupplementsCorrelations: [],
      //
      selectedUserActivityCorrelationsChart: ActivitiesCorrelationsChart,
      selectedUserActivitiesCorrelations: [],
      selectedUserActivitiesCorrelationsTab: "Positively Correlated",
      positiveUserActivitiesCorrelations: [],
      negativeUserActivitiesCorrelations: []
    };
    this.selectSupplementsCorrelationsTab = this.selectSupplementsCorrelationsTab.bind(
      this
    );
    this.selectUserActivitiesCorrelationsTab = this.selectUserActivitiesCorrelationsTab.bind(
      this
    );
  }

  componentDidMount() {
    this.getHistory();
    this.getSupplementsCorrelations();
    this.getUserActivitiesCorrelations();
  }

  selectSupplementsCorrelationsTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    if (name === "Positively Correlated") {
      this.setState({
        selectedSupplementsCorrelations: this.state
          .positiveSupplementsCorrelations
      });
    } else if (name === "Negatively Correlated") {
      this.setState({
        selectedSupplementsCorrelations: this.state
          .negativeSupplementsCorrelations
      });
    }

    this.setState({
      selectedSupplementsCorrelationsTab: name
    });
  }

  selectUserActivitiesCorrelationsTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    if (name === "Positively Correlated") {
      this.setState({
        selectedUserActivitiesCorrelations: this.state
          .positiveUserActivitiesCorrelations
      });
    } else if (name === "Negatively Correlated") {
      this.setState({
        selectedUserActivitiesCorrelations: this.state
          .negativeUserActivitiesCorrelations
      });
    }

    this.setState({
      selectedUserActivitiesCorrelationsTab: name
    });
  }

  //
  // API Calls
  //
  getSupplementsCorrelations() {
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

        this.state.supplementsCorrelationsChart.labels = labels;
        this.state.supplementsCorrelationsChart.datasets[0].data = dataValues;

        const positivelyCorrelatedSupplements = responseData.filter(data => {
          return data[1] > 0;
        });
        const negativelyCorrelatedSupplements = responseData.filter(data => {
          return data[1] < 0;
        });

        // Finally update state after we've done so much magic
        this.setState({
          supplementsCorrelationsChart: this.state.supplementsCorrelationsChart,
          selectedSupplementsCorrelations: positivelyCorrelatedSupplements,
          positiveSupplementsCorrelations: positivelyCorrelatedSupplements,
          negativeSupplementsCorrelations: negativelyCorrelatedSupplements
        });
      });
  }

  getUserActivitiesCorrelations() {
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

        this.state.selectedUserActivityCorrelationsChart.labels = labels;
        this.state.selectedUserActivityCorrelationsChart.datasets[
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
          selectedUserActivityCorrelationsChart: this.state
            .supplementsCorrelationsChart,
          selectedUserActivitiesCorrelations: positivelyCorrelatedActivities,
          positiveUserActivitiesCorrelations: positivelyCorrelatedActivities,
          negativeUserActivitiesCorrelations: negativelyCorrelatedActivities
        });
      });
  }

  getHistory() {
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
    if (this.state.selectedSupplementsCorrelationsTab === tabName) {
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
        <NavLink onClick={this.selectSupplementsCorrelationsTab} name={tabName}>
          {tabName}
        </NavLink>
      </NavItem>
    );
  }

  renderActivitiesCorrelationSelectionTab(tabName) {
    if (this.state.selectedUserActivitiesCorrelationsTab === tabName) {
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
          onClick={this.selectUserActivitiesCorrelationsTab}
          name={tabName}
        >
          {tabName}
        </NavLink>
      </NavItem>
    );
  }

  renderHistoryChart() {
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

  renderUserActivitiesCorrelations() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Activities and Sleep Correlation
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Bar
                data={ActivitiesCorrelationsChart}
                options={{
                  maintainAspectRatio: true
                }}
              />
            </div>
          </div>
        </div>
        <div className="float">
          <div className="card">
            <Nav tabs>
              {this.renderActivitiesCorrelationSelectionTab(
                "Positively Correlated"
              )}
              {this.renderActivitiesCorrelationSelectionTab(
                "Negatively Correlated"
              )}
            </Nav>
            <div className="card-block">
              <table className="table">
                <thead>
                  <tr>
                    <th>Activity</th>
                    <th>Correlation</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.selectedUserActivitiesCorrelations.map(key => (
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

  renderSupplementsCorrelations() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Supplements and Sleep Correlation
          </div>
          <div className="card-block">
            <div className="chart-wrapper">
              <Bar
                data={SupplementsCorrelationsChart}
                options={{
                  maintainAspectRatio: true
                }}
              />
            </div>
          </div>
        </div>
        <div className="float">
          <div className="card">
            <Nav tabs>
              {this.renderSupplementsCorrelationSelectionTab(
                "Positively Correlated"
              )}
              {this.renderSupplementsCorrelationSelectionTab(
                "Negatively Correlated"
              )}
            </Nav>
            <div className="card-block">
              <table className="table">
                <thead>
                  <tr>
                    <th>Supplement</th>
                    <th>Correlation</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.selectedSupplementsCorrelations.map(key => (
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
        {this.renderHistoryChart()}
        {this.renderSupplementsCorrelations()}
        {this.renderUserActivitiesCorrelations()}
        {/*Hold off on Historical Sleep Analytics, No one has 90 Days of History Yet*/}
        {/*{this.renderHistoricalSleepAnalytics()}*/}
      </div>
    );
  }
}

export default SleepAnalyticsView;

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
