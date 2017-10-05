import React, { Component } from "react";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class BasePaginatedLogView extends Component {
  constructor() {
    super();
    this.state = {
      loadedHistory: false
    };

    // This gets set by inheriting classes
    this.resourceName = null;
  }

  componentDidMount() {
    this.getEventHistory();
  }

  getEventHistory = (page = 1) => {
    // Fetch the specific page we want, defaulting at 1
    const url = `api/v1/${this.resourceName}/?page=${page}`;
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ eventHistory: responseData.results });
      this.setState({ currentPageNumber: responseData.current_page });
      this.setState({ lastPageNumber: responseData.last_page });

      // After we've gotten the data, now safe to render
      this.setState({ loadedHistory: true });
    });
  };

  addEventEntry = entry => {
    let updatedEventHistory = [entry, ...this.state.eventHistory.slice()];
    this.setState({ eventHistory: updatedEventHistory });
  };
}
