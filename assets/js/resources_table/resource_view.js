import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";

export class EventLogView extends Component {
  constructor() {
    super();
    this.state = {
      loadedHistory: false
    };

    this.addEventEntry = this.addEventEntry.bind(this);
    this.getEventHistory = this.getEventHistory.bind(this);

    // This gets set by inheriting classes
    this.resourceName = null;
  }

  componentDidMount() {
    this.getEventHistory();
  }

  getEventHistory(page = 1) {
    // Fetch the specific page we want, defaulting at 1
    fetch(`api/v1/${this.resourceName}/?page=${page}`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ eventHistory: responseData.results });
        this.setState({ currentPageNumber: responseData.current_page });
        this.setState({ lastPageNumber: responseData.last_page });

        // After we've gotten the data, now safe to render
        this.setState({ loadedHistory: true });
      });
  }

  addEventEntry(entry) {
    let updatedEventHistory = [entry, ...this.state.eventHistory.slice()];
    this.setState({ eventHistory: updatedEventHistory });
  }
}
