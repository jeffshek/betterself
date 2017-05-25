import React, { Component } from "react";

import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { AddSupplementEvent } from "./add_supplement_event";
import { SupplementsHistoryTable } from "./supplement_event_table";

class SupplementsLogView extends Component {
  constructor() {
    super();
    this.state = {
      loadedHistory: false
    };
    this.addEventEntry = this.addEventEntry.bind(this);
    this.getEventHistory = this.getEventHistory.bind(this);
  }

  componentDidMount() {
    this.getEventHistory();
  }

  getEventHistory(page = 1) {
    this.setState({ loadedHistory: false });

    // Fetch the specific page we want, defaulting at 1
    fetch(`api/v1/supplement_events/?page=${page}`, {
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
    this.setState({
      eventHistory: updatedEventHistory
    });
  }

  render() {
    return (
      <div>
        <AddSupplementEvent addSupplementEntry={this.addEventEntry} />
        <SupplementsHistoryTable
          eventHistory={this.state.eventHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory}
          getSupplementHistory={this.getEventHistory}
        />
      </div>
    );
  }
}

export default SupplementsLogView;
