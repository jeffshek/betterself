import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import {
  CHART_HOVER_BORDER_COLOR,
  CHART_HOVER_COLOR,
  CHARTS_BACKGROUND_COLOR,
  DataAnalyticsRow
} from "../constants/charts";
import {
  NEGATIVELY_CORRELATED_LABEL,
  POSITIVELY_CORRELATED_LABEL
} from "../constants";

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

export class BaseAnalyticsView extends Component {
  constructor() {
    super();

    this.state = {
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

    this.selectSupplementsCorrelationsTab = this.selectSupplementsCorrelationsTab.bind(
      this
    );
    this.handleSelectedProductivityHistoryType = this.handleSelectedProductivityHistoryType.bind(
      this
    );
  }

  getSupplementsCorrelations() {
    fetch(this.supplementCorrelationsURL, {
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

  renderSupplementsCorrelations() {
    return (
      <div className="card-columns cols-2">
        <div className="card">
          <div className="card-header analytics-text-box-label">
            {this.supplementsCorrelationsChartLabel}
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
}
