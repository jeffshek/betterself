import React from "react";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import { Bar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { DefaultChartDataset } from "../constants/charts";
import {
  DISTRACTING_MINUTES_LABEL,
  DISTRACTING_MINUTES_VARIABLE,
  NEUTRAL_MINUTES_LABEL,
  NEUTRAL_MINUTES_VARIABLE,
  PRODUCTIVE_MINUTES_LABEL,
  PRODUCTIVE_MINUTES_VARIABLE,
  VERY_DISTRACTING_MINUTES_LABEL,
  VERY_DISTRACTING_MINUTES_VARIABLE,
  VERY_PRODUCTIVE_MINUTES_LABEL,
  VERY_PRODUCTIVE_MINUTES_VARIABLE
} from "../constants/productivity";
import { BaseAnalyticsView } from "./base";
import moment from "moment";
import {
  ABBREVIATED_CHART_DATE,
  DATE_REQUEST_FORMAT,
  minutesToHours,
  YEAR_MONTH_DAY_FORMAT
} from "../constants/dates_and_times";

const ProductivityColumnMappingToKey = {
  "Very Productive Minutes": VERY_PRODUCTIVE_MINUTES_VARIABLE,
  "Productive Minutes": PRODUCTIVE_MINUTES_VARIABLE,
  "Neutral Minutes": NEUTRAL_MINUTES_VARIABLE,
  "Distracting Minutes": DISTRACTING_MINUTES_VARIABLE,
  "Very Distracting Minutes": VERY_DISTRACTING_MINUTES_VARIABLE
};

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultChartDataset)]
};

export class ProductivityAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();

    const analyticsSettings = {
      periodsLookback: 60,
      updatePeriodsLookback: 60,
      rollingWindow: 1,
      updateRollingWindow: 1,
      startDate: moment(),
      endDate: moment()
    };

    const updateState = {
      productivityHistoryChart: ProductivityHistoryChart,
      selectedProductivityHistoryChartData: [],
      selectedProductivityHistoryType: VERY_PRODUCTIVE_MINUTES_LABEL,
      modal: false
    };

    // Update state (from base class) with the above
    this.state = Object.assign(this.state, updateState, analyticsSettings);

    this.state.productivityHistoryChart.datasets[
      0
    ].label = `${this.state.selectedProductivityHistoryType}/Hours`;

    this.supplementCorrelationsURL =
      "api/v1/productivity_log/supplements/correlations";
    this.supplementsCorrelationsChartLabel =
      "Supplements and Productivity Correlation";
    this.userActivitiesCorrelationsURL =
      "api/v1/productivity_log/user_activities/correlations";
    this.userActivitiesCorrelationsChartLabel =
      "User Activities and Productivity Correlation";
  }

  componentDidMount() {
    this.updateData();
  }

  updateData() {
    this.getHistory();
    this.getSupplementsCorrelations();
    this.getUserActivitiesCorrelations();
  }

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };

  submitUpdate = () => {
    // Set the new state and then fetch the correlations, use a callback to call after updating
    this.setState(
      {
        periodsLookback: this.state.updatePeriodsLookback,
        rollingWindow: this.state.updateRollingWindow
      },
      this.updateData
    );

    this.toggle();
  };

  // Choose between "Very Productive Minutes", "Neutral Minutes", "Negative Minutes" etc
  handleSelectedProductivityHistoryType = event => {
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
    ].label = `${this.state.selectedProductivityHistoryType}/Hours`;

    this.setState({
      productivityHistoryChart: this.state.productivityHistoryChart
    });
  };

  getHistory() {
    const startDate = moment()
      .subtract(this.state.periodsLookback, "days")
      .format(DATE_REQUEST_FORMAT);

    const url = `/api/v1/productivity_log/aggregates/?start_date=${startDate}&cumulative_window=${this.state.rollingWindow}`;

    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const labelDates = Object.keys(responseData);
        labelDates.sort();

        const labelDatesFormatted = labelDates.map(e => {
          return moment(e).format(ABBREVIATED_CHART_DATE);
        });

        const selectedHistoryVariable =
          ProductivityColumnMappingToKey[
            this.state.selectedProductivityHistoryType
          ];

        const responseValues = labelDates.map(e => {
          const selectedVariableData = responseData[e][selectedHistoryVariable];
          return minutesToHours(selectedVariableData);
        });

        this.state.productivityHistoryChart.labels = labelDatesFormatted;
        this.state.productivityHistoryChart.datasets[0].data = responseValues;

        this.setState({
          startDate: moment(labelDates[0]),
          productivityHistoryChart: this.state.productivityHistoryChart,
          selectedProductivityHistoryChartData: responseValues
        });
      });
  }

  handleSettingsChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    const intValue = parseInt(value);

    this.setState({
      [name]: intValue
    });
  };

  renderPageTitleBlock() {
    const title = `Productivity Analytics | ${this.state.startDate.format(YEAR_MONTH_DAY_FORMAT)} - ${this.state.endDate.format(YEAR_MONTH_DAY_FORMAT)} | ${this.state.rollingWindow} Day Aggregate`;
    return (
      <span className="font-1xl productivity-analytics-margin-left">
        {title}
      </span>
    );
  }

  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          {this.renderPageTitleBlock()}
          <span className="float-right">
            <button
              type="submit"
              id="add-new-object-button"
              className="btn btn-sm btn-success"
              onClick={this.toggle}
            >
              <span id="white-text">
                <i className="fa fa-dot-circle-o" /> Settings
              </span>
            </button>
          </span>
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Bar
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

  renderSettingsModal() {
    if (!this.state.modal) {
      return <div />;
    }

    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>
          Productivity Analytics Settings
        </ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Chart Productivity Type
          </label>
          <br />
          <select
            className="form-control chart-selector"
            onChange={this.handleSelectedProductivityHistoryType}
            value={this.state.selectedProductivityHistoryType}
            size="1"
          >
            <option>{VERY_PRODUCTIVE_MINUTES_LABEL}</option>
            <option>{PRODUCTIVE_MINUTES_LABEL}</option>
            <option>{NEUTRAL_MINUTES_LABEL}</option>
            <option>{DISTRACTING_MINUTES_LABEL}</option>
            <option>{VERY_DISTRACTING_MINUTES_LABEL}</option>
          </select>
          <br />
          <label className="form-control-label add-event-label">
            Correlation Cutoff (Days, Integer)
          </label>
          <div>
            Specify how far back the correlation should be run against current date. Longer lookbacks are more likely to tell you what's working or not. Shorter lookbacks are useful to tell if a particular supplement is useful with your current regimen.
          </div>
          <br />
          <input
            name="updatePeriodsLookback"
            type="number"
            className="form-control"
            defaultValue={this.state.updatePeriodsLookback}
            onChange={this.handleSettingsChange}
          />
          <br />
          <label className="form-control-label add-event-label">
            Sum Cumulative Lookback (Days, Integer)
          </label>
          <div>
            Instead of performing analytics on a single day, sum consecutive days together by summing total supplement quantity with total productivity. IE. Instead of correlating a single input of Tea on a given date, correlate a week's worth of cumulative supplements taken against other weeks. Useful for supplements taken at odd hours (1-2AM) or if productivity has a high variance. Default of one means no aggregation.
          </div>
          <br />
          <input
            name="updateRollingWindow"
            type="number"
            className="form-control"
            defaultValue={this.state.updateRollingWindow}
            onChange={this.handleSettingsChange}
          />
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitUpdate}>
            Update
          </Button>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
  }

  render() {
    return (
      <div className="animated fadeIn">
        {this.renderHistoryChart()}
        {this.renderSupplementsCorrelations()}
        {this.renderUserActivitiesCorrelations()}
        {this.renderSettingsModal()}
      </div>
    );
  }
}
