import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";

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

    return <div>Hello</div>;
  }
}
