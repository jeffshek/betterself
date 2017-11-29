import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { VERY_PRODUCTIVE_MINUTES_VARIABLE } from "../constants/productivity";
import {
  ABBREVIATED_CHART_DATE,
  minutesToHours
} from "../constants/dates_and_times";
import {
  GenerateHistoryChartTemplate,
  LineDefaultChartDataset
} from "../constants/charts";
import moment from "moment";
import { Bar } from "react-chartjs-2";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class SupplementsAndProductivityChartView extends Component {
  constructor(props) {
    super(props);

    this.state = {
      supplementsAndProductivityChart: GenerateHistoryChartTemplate(
        "Supplements & Productivity"
      )
    };
  }

  componentDidMount() {
    this.updateDailySupplementData();
    this.updateDailyProductivityData();
  }

  // Add start dates, we only need to go 3 months back!
  updateDailyProductivityData() {
    const url =
      "/api/v1/productivity_log/aggregates/?complete_date_range_in_daily_frequency=True";

    getFetchJSONAPI(url).then(responseData => {
      const labelDates = Object.keys(responseData);
      labelDates.sort();

      const responseValues = labelDates.map(e => {
        const selectedVariableData =
          responseData[e][VERY_PRODUCTIVE_MINUTES_VARIABLE];
        return minutesToHours(selectedVariableData);
      });

      this.state.supplementsAndProductivityChart.datasets.push(
        Object.assign({}, LineDefaultChartDataset)
      );
      this.state.supplementsAndProductivityChart.datasets[1].label =
        "Very Productivity Time (Hours)";
      this.state.supplementsAndProductivityChart.datasets[
        1
      ].data = responseValues;

      this.setState({
        supplementsAndProductivityChart: this.state
          .supplementsAndProductivityChart
      });
    });
  }

  updateDailySupplementData() {
    const url = `/api/v1/supplements/${this.props.supplement.uuid}/log/?frequency=daily&complete_date_range_in_daily_frequency=True`;

    getFetchJSONAPI(url).then(responseData => {
      const responseDataDates = Object.keys(responseData);
      responseDataDates.sort();

      const supplementDatesFormatted = responseDataDates.map(key =>
        moment(key).format(ABBREVIATED_CHART_DATE)
      );

      const dataParsed = responseDataDates.map(key => {
        return responseData[key];
      });

      this.state.supplementsAndProductivityChart.labels = supplementDatesFormatted;
      this.state.supplementsAndProductivityChart.datasets[
        0
      ].label = `${this.props.supplement.name} (Quantity)`;
      this.state.supplementsAndProductivityChart.datasets[0].data = dataParsed;

      // Reset the historicalState of the graph after the data has been grabbed.
      this.setState({
        supplementsAndProductivityChart: this.state
          .supplementsAndProductivityChart
      });
    });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">
            {this.props.supplement.name} Overview
          </span>
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Bar
              data={this.state.supplementsAndProductivityChart}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      </div>
    );
  }
}
