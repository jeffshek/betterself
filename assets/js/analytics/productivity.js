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
import {
  DISTRACTING_MINUTES_LABEL,
  DISTRACTING_MINUTES_VARIABLE,
  NEGATIVELY_CORRELATED_LABEL,
  NEUTRAL_MINUTES_LABEL,
  NEUTRAL_MINUTES_VARIABLE,
  POSITIVELY_CORRELATED_LABEL,
  PRODUCTIVE_MINUTES_LABEL,
  PRODUCTIVE_MINUTES_VARIABLE,
  VERY_DISTRACTING_MINUTES_LABEL,
  VERY_DISTRACTING_MINUTES_VARIABLE,
  VERY_PRODUCTIVE_MINUTES_LABEL,
  VERY_PRODUCTIVE_MINUTES_VARIABLE
} from "../constants";

const ProductivityColumnMappingToKey = {
  "Very Productive Minutes": VERY_PRODUCTIVE_MINUTES_VARIABLE,
  "Productive Minutes": PRODUCTIVE_MINUTES_VARIABLE,
  "Neutral Minutes": NEUTRAL_MINUTES_VARIABLE,
  "Distracting Minutes": DISTRACTING_MINUTES_VARIABLE,
  "Very Distracting Minutes": VERY_DISTRACTING_MINUTES_VARIABLE
};

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

const SupplementsCorrelationsChart = {
  labels: [],
  datasets: [
    {
      label: "Very Productive Minutes Correlation",
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
      label: "Productivity Correlation",
      backgroundColor: CHARTS_BACKGROUND_COLOR,
      borderColor: CHARTS_BACKGROUND_COLOR,
      borderWidth: 1,
      hoverBackgroundColor: CHART_HOVER_COLOR,
      hoverBorderColor: CHART_HOVER_BORDER_COLOR,
      data: []
    }
  ]
};

export class ProductivityAnalyticsView extends Component {
  constructor() {
    super();
    this.state = {
      productivityHistoryChart: ProductivityHistoryChart,
      //
      selectedProductivityHistoryChartData: [],
      selectedProductivityHistoryType: VERY_PRODUCTIVE_MINUTES_LABEL,
      //
      supplementsCorrelationsChart: SupplementsCorrelationsChart,
      selectedSupplementsCorrelations: [],
      selectedSupplementsCorrelationsTab: POSITIVELY_CORRELATED_LABEL,
      positiveSupplementsCorrelations: [],
      negativeSupplementsCorrelations: [],
      //
      selectedUserActivityCorrelationsChart: ActivitiesCorrelationsChart,
      selectedUserActivitiesCorrelations: [],
      selectedUserActivitiesCorrelationsTab: POSITIVELY_CORRELATED_LABEL,
      positiveUserActivitiesCorrelations: [],
      negativeUserActivitiesCorrelations: []
    };
    this.state.productivityHistoryChart.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;
    this.handleSelectedProductivityHistory = this.handleSelectedProductivityHistory.bind(
      this
    );
    this.selectSupplementsCorrelationsTab = this.selectSupplementsCorrelationsTab.bind(
      this
    );
  }

  componentDidMount() {
    this.getHistory();
    this.getSupplementsCorrelations();
  }

  handleSelectedProductivityHistory(event) {
    const selectedProductivityHistoryType = event.target.value;
    const column_key =
      ProductivityColumnMappingToKey[selectedProductivityHistoryType];

    const arrayValues = this.state.selectedProductivityHistoryChartData.map(
      key => key[column_key]
    );

    this.state.selectedProductivityHistoryType = selectedProductivityHistoryType;
    this.state.productivityHistoryChart.datasets[0].data = arrayValues;
    this.state.productivityHistoryChart.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;

    this.setState({
      productivityHistoryChart: this.state.productivityHistoryChart
    });
  }

  //
  // API Calls
  //
  getSupplementsCorrelations() {
    fetch(`api/v1/productivity_log/supplements/correlations`, {
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

  selectSupplementsCorrelationsTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    if (name === POSITIVELY_CORRELATED_LABEL) {
      this.setState({
        selectedSupplementsCorrelations: this.state
          .positiveSupplementsCorrelations
      });
    } else if (name === NEGATIVELY_CORRELATED_LABEL) {
      this.setState({
        selectedSupplementsCorrelations: this.state
          .negativeSupplementsCorrelations
      });
    }

    this.setState({
      selectedSupplementsCorrelationsTab: name
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

  getHistory() {
    fetch("/api/v1/productivity_log/", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const reverseResponseData = responseData.results.reverse();

        const labelDates = reverseResponseData.map(key => key.date);
        const arrayValues = reverseResponseData.map(
          key => key.very_productive_time_minutes
        );

        this.state.productivityHistoryChart.labels = labelDates;
        this.state.productivityHistoryChart.datasets[0].data = arrayValues;

        this.setState({
          productivityHistoryChart: this.state.productivityHistoryChart,
          selectedProductivityHistoryChartData: reverseResponseData
        });
      });
  }

  renderSupplementsCorrelations() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            Supplements and Productivity Correlation
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
                POSITIVELY_CORRELATED_LABEL
              )}
              {this.renderSupplementsCorrelationSelectionTab(
                NEGATIVELY_CORRELATED_LABEL
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

  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">Productivity History</span>
          <span className="float-right">
            Chart Selection
            <select
              className="form-control chart-selector"
              onChange={this.handleSelectedProductivityHistory}
              value={this.state.selectedProductivityHistoryType}
              size="1"
            >
              <option>{VERY_PRODUCTIVE_MINUTES_LABEL}</option>
              <option>{PRODUCTIVE_MINUTES_LABEL}</option>
              <option>{NEUTRAL_MINUTES_LABEL}</option>
              <option>{DISTRACTING_MINUTES_LABEL}</option>
              <option>{VERY_DISTRACTING_MINUTES_LABEL}</option>
            </select>
          </span>
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Line
              data={this.state.productivityHistoryChart}
              options={{
                maintainAspectRatio: false
              }}
            />
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
      </div>
    );
  }
}
