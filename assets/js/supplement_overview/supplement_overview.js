import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { GenerateHistoryChartTemplate } from "../constants/charts";

const SupplementsAndProductivityChart = GenerateHistoryChartTemplate(
  "Total Quantity Taken"
);

class SupplementsAndProductivityChartView extends Component {
  constructor(props) {
    super(props);

    const { supplement } = props;

    // console.log(supplement)
    this.state = {
      supplementsAndProductivityChart: SupplementsAndProductivityChart
    };
  }

  componentDidMount() {
    this.updateDailySupplementData();
  }

  updateDailySupplementData() {
    const url = `/api/v1/supplements/${this.props.supplement.uuid}/log`;

    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // const supplement = responseData[0];
        // this.setState({
        //   supplement: supplement
        // });
        console.log(responseData);
      });
  }

  render() {
    return <div />;
  }
}

export class SupplementsOverview extends Component {
  constructor(props) {
    super(props);

    const { match } = props;

    let supplementUUID = match.params.supplementUUID;

    // psuedo code
    supplementUUID = "474dfd14-391d-42c9-afb3-b2d6693dd6b6";

    this.state = {
      supplement: null
    };

    fetch(`/api/v1/supplements/?uuid=${supplementUUID}`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const supplement = responseData[0];
        this.setState({
          supplement: supplement
        });
      });

    // TODO - How do you raise a 404
  }

  render() {
    if (!this.state.supplement) {
      return <div />;
    }

    return (
      <div>
        <SupplementsAndProductivityChartView
          supplement={this.state.supplement}
        />
      </div>
    );
  }
}
