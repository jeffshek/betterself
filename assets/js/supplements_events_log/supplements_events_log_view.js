import React, { Component } from "react";

import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { AddSupplementEntry } from "./add_supplements_entry";
import { SupplementsHistoryTableList } from "./supplements_history_table";

class SupplementsLogView extends Component {
  constructor() {
    super();
    this.state = {
      supplementHistory: [
        {
          supplement_name: "Loading ... ",
          quantity: "Loading ... ",
          duration: "Loading ... ",
          time: null,
          source: "Loading ... "
        }
      ],
      loadedSupplementHistory: false
    };
    this.addSupplementEntry = this.addSupplementEntry.bind(this);
    this.getSupplementHistory = this.getSupplementHistory.bind(this);
  }

  componentDidMount() {
    this.getSupplementHistory();
  }

  getSupplementHistory(page = 1) {
    this.setState({ loadedSupplementHistory: false });

    // Fetch the specific page we want, defaulting at 1
    fetch(`api/v1/supplement_events/?page=${page}`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ supplementHistory: responseData.results });
        this.setState({ currentPageNumber: responseData.current_page });
        this.setState({ lastPageNumber: responseData.last_page });

        // After we've gotten the data, now safe to render
        this.setState({ loadedSupplementHistory: true });
      });
  }

  addSupplementEntry(entry) {
    let updatedSupplementHistory = [
      entry,
      ...this.state.supplementHistory.slice()
    ];
    this.setState({
      supplementHistory: updatedSupplementHistory
    });
  }

  render() {
    return (
      <div>
        <AddSupplementEntry addSupplementEntry={this.addSupplementEntry} />
        <SupplementsHistoryTableList
          supplementHistory={this.state.supplementHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedSupplementHistory}
          getSupplementHistory={this.getSupplementHistory}
        />
      </div>
    );
  }
}

export default SupplementsLogView;
