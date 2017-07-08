import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";
import {
  CHART_HOVER_BORDER_COLOR,
  CHART_HOVER_COLOR,
  CHARTS_BACKGROUND_COLOR,
  DataAnalyticsRow,
  DefaultLineChartDataset
} from "../constants/charts";
import { POSITIVELY_CORRELATED_LABEL } from "../constants";
import { BaseAnalyticsView } from "./base";

const SleepHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

const SupplementsCorrelationsChart = {
  labels: [],
  datasets: [
    {
      label: "Sleep Correlation",
      backgroundColor: CHARTS_BACKGROUND_COLOR,
      borderColor: CHARTS_BACKGROUND_COLOR,
      borderWidth: 1,
      hoverBackgroundColor: CHART_HOVER_COLOR,
      hoverBorderColor: CHART_HOVER_BORDER_COLOR,
      data: []
    }
  ]
};

const ActivitiesCorrelationsChart = {
  labels: [],
  datasets: [
    {
      label: "Sleep Correlation",
      backgroundColor: CHARTS_BACKGROUND_COLOR,
      borderColor: CHARTS_BACKGROUND_COLOR,
      borderWidth: 1,
      hoverBackgroundColor: CHART_HOVER_COLOR,
      hoverBorderColor: CHART_HOVER_BORDER_COLOR,
      data: []
    }
  ]
};

class SleepAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();
    const updateState = {
      sleepHistory: SleepHistoryChart
    };
    // Update state (from base class) with the above
    this.state = Object.assign(this.state, updateState);
    this.state.sleepHistory.datasets[0].label = "Sleep Time (Hours)";

    this.selectSupplementsCorrelationsTab = this.selectSupplementsCorrelationsTab.bind(
      this
    );
    this.selectUserActivitiesCorrelationsTab = this.selectUserActivitiesCorrelationsTab.bind(
      this
    );

    this.supplementCorrelationsURL =
      "api/v1/sleep_activities/supplements/correlations";
    this.supplementsCorrelationsChartLabel =
      "Supplements and Sleep Correlation";
    this.userActivitiesCorrelationsURL =
      "api/v1/sleep_activities/user_activities/correlations";
  }

  componentDidMount() {
    this.getHistory();
    this.getSupplementsCorrelations();
    this.getUserActivitiesCorrelations();
  }

  // selectSupplementsCorrelationsTab(event) {
  //   event.preventDefault();
  //
  //   const target = event.target;
  //   const name = target.name;
  //
  //   if (name === "Positively Correlated") {
  //     this.setState({
  //       selectedSupplementsCorrelations: this.state
  //         .positiveSupplementsCorrelations
  //     });
  //   } else if (name === "Negatively Correlated") {
  //     this.setState({
  //       selectedSupplementsCorrelations: this.state
  //         .negativeSupplementsCorrelations
  //     });
  //   }
  //
  //   this.setState({
  //     selectedSupplementsCorrelationsTab: name
  //   });
  // }

  //
  // API Calls
  //
  // getSupplementsCorrelations() {
  //   fetch(`api/v1/sleep_activities/supplements/correlations`, {
  //     method: "GET",
  //     headers: JSON_AUTHORIZATION_HEADERS
  //   })
  //     .then(response => {
  //       return response.json();
  //     })
  //     .then(responseData => {
  //       const labels = responseData.map(data => {
  //         return data[0];
  //       });
  //       const dataValues = responseData.map(data => {
  //         return data[1];
  //       });
  //
  //       this.state.supplementsCorrelationsChart.labels = labels;
  //       this.state.supplementsCorrelationsChart.datasets[0].data = dataValues;
  //
  //       const positivelyCorrelatedSupplements = responseData.filter(data => {
  //         return data[1] > 0;
  //       });
  //       const negativelyCorrelatedSupplements = responseData.filter(data => {
  //         return data[1] < 0;
  //       });
  //
  //       // Finally update state after we've done so much magic
  //       this.setState({
  //         supplementsCorrelationsChart: this.state.supplementsCorrelationsChart,
  //         selectedSupplementsCorrelations: positivelyCorrelatedSupplements,
  //         positiveSupplementsCorrelations: positivelyCorrelatedSupplements,
  //         negativeSupplementsCorrelations: negativelyCorrelatedSupplements
  //       });
  //     });
  // }

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

  // renderSupplementsCorrelationSelectionTab(tabName) {
  //   if (this.state.selectedSupplementsCorrelationsTab === tabName) {
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
  //       <NavLink onClick={this.selectSupplementsCorrelationsTab} name={tabName}>
  //         {tabName}
  //       </NavLink>
  //     </NavItem>
  //   );
  // }

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
          <span className="font-2xl">Sleep History</span>
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
                data={this.state.selectedUserActivityCorrelationsChart}
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
                    <DataAnalyticsRow key={key} object={key} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // renderSupplementsCorrelations() {
  //   return (
  //     <div className="card-columns cols-2">
  //       <div className="card">
  //         <div className="card-header analytics-text-box-label">
  //           {this.supplementsCorrelationsChartLabel}
  //         </div>
  //         <div className="card-block">
  //           <div className="chart-wrapper">
  //             <Bar
  //               data={SupplementsCorrelationsChart}
  //               options={{
  //                 maintainAspectRatio: true
  //               }}
  //             />
  //           </div>
  //         </div>
  //       </div>
  //       <div className="float">
  //         <div className="card">
  //           <Nav tabs>
  //             {this.renderSupplementsCorrelationSelectionTab(
  //               POSITIVELY_CORRELATED_LABEL
  //             )}
  //             {this.renderSupplementsCorrelationSelectionTab(
  //               "Negatively Correlated"
  //             )}
  //           </Nav>
  //           <div className="card-block">
  //             <table className="table">
  //               <thead>
  //                 <tr>
  //                   <th>Supplement</th>
  //                   <th>Correlation</th>
  //                 </tr>
  //               </thead>
  //               <tbody>
  //                 {this.state.selectedSupplementsCorrelations.map(key => (
  //                   <DataAnalyticsRow key={key} object={key} />
  //                 ))}
  //               </tbody>
  //             </table>
  //           </div>
  //         </div>
  //       </div>
  //     </div>
  //   );
  // }

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
//       backgroundColor: CHARTS_BACKGROUND_COLOR,
//       borderColor: "rgb(74, 86, 104)",
//       borderWidth: 1,
//       hoverBackgroundColor: CHART_HOVER_COLOR,
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
