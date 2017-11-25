import React, { Component } from "react";
import qs from "query-string";
import { postFetchJSONAPI } from "../utils/fetch_utils";
import { FITBIT_BACKEND_API_CALLBACK_URL } from "../constants/urls";

export class FitBitCompleteCallbackView extends Component {
  constructor(props) {
    super(props);

    const { location } = props;
    const fitbitCodeDetails = qs.parse(location.search);
    const { code } = fitbitCodeDetails;

    const params = {
      code: code
    };

    postFetchJSONAPI(
      FITBIT_BACKEND_API_CALLBACK_URL,
      params
    ).then(responseData => {
      const { next_url } = responseData;
      this.props.history.push(next_url);
    });
  }

  render() {
    return <div />;
  }
}
