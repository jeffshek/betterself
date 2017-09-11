import React, { Component } from "react";
import { Bar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { GenerateChartTemplate } from "../constants/charts";
import {
  NEGATIVELY_CORRELATED_LABEL,
  NOT_CORRELATED_LABEL,
  POSITIVELY_CORRELATED_LABEL
} from "../constants/productivity";
import {
  UserActivitiesCorrelationTableRow,
  SupplementCorrelationTableRow
} from "./constants";

const SupplementsCorrelationsChart = GenerateChartTemplate(
  "Supplements Correlation"
);
const UserActivitiesCorrelationsChart = GenerateChartTemplate(
  "Productivity Correlation"
);

// TODO - Refactor this file completely to the multitab format

export class BaseAnalyticsView extends Component {
  constructor() {
    super();

    this.state = {
      supplementNameUUIDMapping: null,
      // Supplements Correlations
      supplementsCorrelationsChart: SupplementsCorrelationsChart,
      selectedSupplementsCorrelations: [],
      selectedSupplementsCorrelationsTab: POSITIVELY_CORRELATED_LABEL,
      positiveSupplementsCorrelations: [],
      negativeSupplementsCorrelations: [],
      neutralSupplementsCorrelations: [],
      // User Activities
      selectedUserActivitiesCorrelationsChart: UserActivitiesCorrelationsChart,
      selectedUserActivitiesCorrelations: [],
      selectedUserActivitiesCorrelationsTab: POSITIVELY_CORRELATED_LABEL,
      positiveUserActivitiesCorrelations: [],
      negativeUserActivitiesCorrelations: [],
      neutralUserActivitiesCorrelations: []
    };
  }

  getCorrelatedData(responseData) {
    // Some of the supplements might have no correlation, so a filter
    // at the first pass to only return correlatedData
    const correlatedData = responseData.filter(data => {
      if (data[1]) {
        return data;
      }
    });
    return correlatedData;
  }

  getChartLabels(correlatedData) {
    const labels = correlatedData.map(data => {
      // Very Productive Minutes is way too long of a label
      return data[0].replace("Minutes", "");
    });
    return labels;
  }

  getChartData(correlatedData) {
    const dataValues = correlatedData.map(data => {
      return data[1];
    });
    return dataValues;
  }

  getSupplementMapping() {
    fetch("/api/v1/supplements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        let supplementNameUUIDMapping = {};
        responseData.map(e => {
          supplementNameUUIDMapping[e.name] = e.uuid;
        });
        this.setState({ supplementNameUUIDMapping: supplementNameUUIDMapping });
      });
  }

  getPositivelyCorrelatedData(responseData) {
    const positivelyCorrelated = responseData.filter(data => {
      return data[1] > 0;
    });
    return positivelyCorrelated;
  }

  getNegativelyCorrelatedData(responseData) {
    const negativelyCorrelated = responseData.filter(data => {
      return data[1] < 0;
    });
    return negativelyCorrelated;
  }

  getNoCorrelatedData(responseData) {
    const notCorrelatedData = responseData.filter(data => {
      if (!data[1]) {
        return true;
      }
    });
    return notCorrelatedData;
  }

  getSupplementsCorrelations() {
    const url = `${this.supplementCorrelationsURL}?correlation_lookback=${this.state.periodsLookback}&cumulative_lookback=${this.state.rollingWindow}`;
    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const correlatedData = this.getCorrelatedData(responseData);
        const labels = this.getChartLabels(correlatedData);
        const dataValues = this.getChartData(correlatedData);

        this.state.supplementsCorrelationsChart.labels = labels;
        this.state.supplementsCorrelationsChart.datasets[0].data = dataValues;

        const positiveSupplementCorrelations = this.getPositivelyCorrelatedData(
          responseData
        );
        const negativeSupplementCorrelations = this.getNegativelyCorrelatedData(
          responseData
        );
        const neutralSupplementsCorrelations = this.getNoCorrelatedData(
          responseData
        );

        this.setState({
          supplementsCorrelationsChart: this.state.supplementsCorrelationsChart,
          selectedSupplementsCorrelations: positiveSupplementCorrelations,
          positiveSupplementsCorrelations: positiveSupplementCorrelations,
          negativeSupplementsCorrelations: negativeSupplementCorrelations,
          neutralSupplementsCorrelations: neutralSupplementsCorrelations
        });
      });
  }

  getUserActivitiesCorrelations() {
    const url = `${this.userActivitiesCorrelationsURL}?correlation_lookback=${this.state.periodsLookback}&cumulative_lookback=${this.state.rollingWindow}`;

    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const correlatedData = this.getCorrelatedData(responseData);
        const labels = this.getChartLabels(correlatedData);
        const dataValues = this.getChartData(correlatedData);

        this.state.selectedUserActivitiesCorrelationsChart.labels = labels;
        this.state.selectedUserActivitiesCorrelationsChart.datasets[
          0
        ].data = dataValues;

        const positiveUserActivityCorrelations = this.getPositivelyCorrelatedData(
          responseData
        );
        const negativeUserActivitiesCorrelations = this.getNegativelyCorrelatedData(
          responseData
        );
        const neutralUserActivitiesCorrelations = this.getNoCorrelatedData(
          responseData
        );

        this.setState({
          selectedUserActivitiesCorrelationsChart: this.state
            .selectedUserActivitiesCorrelationsChart,
          selectedUserActivitiesCorrelations: positiveUserActivityCorrelations,
          positiveUserActivitiesCorrelations: positiveUserActivityCorrelations,
          negativeUserActivitiesCorrelations: negativeUserActivitiesCorrelations,
          neutralUserActivitiesCorrelations: neutralUserActivitiesCorrelations
        });
      });
  }

  selectSupplementsCorrelationsTab = event => {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    let selectedSupplementsCorrelations;
    if (name === POSITIVELY_CORRELATED_LABEL) {
      selectedSupplementsCorrelations = this.state
        .positiveSupplementsCorrelations;
    } else if (name === NEGATIVELY_CORRELATED_LABEL) {
      selectedSupplementsCorrelations = this.state
        .negativeSupplementsCorrelations;
    } else if (name === NOT_CORRELATED_LABEL) {
      selectedSupplementsCorrelations = this.state
        .neutralSupplementsCorrelations;
    }

    this.setState({
      // Say either Positive Correlated, Negatively Correlated or Neutral
      selectedSupplementsCorrelationsTab: name,
      selectedSupplementsCorrelations: selectedSupplementsCorrelations
    });
  };

  selectUserActivitiesCorrelationsTab = event => {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    let selectedUserActivitiesCorrelations;
    if (name === POSITIVELY_CORRELATED_LABEL) {
      selectedUserActivitiesCorrelations = this.state
        .positiveUserActivitiesCorrelations;
    } else if (name === NEGATIVELY_CORRELATED_LABEL) {
      selectedUserActivitiesCorrelations = this.state
        .negativeUserActivitiesCorrelations;
    } else if (name === NOT_CORRELATED_LABEL) {
      selectedUserActivitiesCorrelations = this.state
        .neutralUserActivitiesCorrelations;
    }

    this.setState({
      // Say either Positive Correlated or Negatively Correlated
      selectedUserActivitiesCorrelationsTab: name,
      selectedUserActivitiesCorrelations: selectedUserActivitiesCorrelations
    });
  };

  renderActivitiesCorrelationsSelectionTab(tabName) {
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

  renderSupplementsCorrelationsSelectionTab(tabName) {
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

  renderUserActivitiesChart() {
    const userActivitiesCorrelationsChartLabel = `${this.userActivitiesCorrelationsChartLabel} (Last ${this.state.periodsLookback} Days)`;

    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          {userActivitiesCorrelationsChartLabel}
        </div>
        <div className="chart-wrapper">
          <Bar
            data={this.state.selectedUserActivitiesCorrelationsChart}
            options={{
              maintainAspectRatio: true
            }}
          />
        </div>
      </div>
    );
  }

  renderUserActivitiesData() {
    return (
      <div className="float">
        <div className="card">
          <Nav tabs>
            {this.renderActivitiesCorrelationsSelectionTab(
              POSITIVELY_CORRELATED_LABEL
            )}
            {this.renderActivitiesCorrelationsSelectionTab(
              NEGATIVELY_CORRELATED_LABEL
            )}
            {this.renderActivitiesCorrelationsSelectionTab(
              NOT_CORRELATED_LABEL
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
                  <UserActivitiesCorrelationTableRow key={key} object={key} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  renderUserActivitiesCorrelations() {
    return (
      <div className="card-columns cols-2">
        {this.renderUserActivitiesChart()}
        {this.renderUserActivitiesData()}
      </div>
    );
  }

  renderSupplementsCorrelationsChart() {
    const supplementsCorrelationsChartLabel = `${this.supplementsCorrelationsChartLabel} (Last ${this.state.periodsLookback} Days)`;

    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          {supplementsCorrelationsChartLabel}
        </div>
        <div className="chart-wrapper">
          <Bar
            data={this.state.supplementsCorrelationsChart}
            options={{
              maintainAspectRatio: true
            }}
          />
        </div>
      </div>
    );
  }

  renderSupplementsCorrelationsData() {
    if (!this.state.supplementNameUUIDMapping) {
      return <div />;
    }

    return (
      <div className="float">
        <div className="card">
          <Nav tabs>
            {this.renderSupplementsCorrelationsSelectionTab(
              POSITIVELY_CORRELATED_LABEL
            )}
            {this.renderSupplementsCorrelationsSelectionTab(
              NEGATIVELY_CORRELATED_LABEL
            )}
            {this.renderSupplementsCorrelationsSelectionTab(
              NOT_CORRELATED_LABEL
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
                  <SupplementCorrelationTableRow
                    key={key}
                    object={key}
                    supplementUUID={
                      this.state.supplementNameUUIDMapping[key[0]]
                    }
                  />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  renderSupplementsCorrelations() {
    return (
      <div className="card-columns cols-2">
        {this.renderSupplementsCorrelationsChart()}
        {this.renderSupplementsCorrelationsData()}
      </div>
    );
  }
}
