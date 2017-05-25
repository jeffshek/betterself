import React, { Component } from "react";

import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { AddProductivityEvent } from "./add_productivity_event";
import { ProductivityLogTable } from "./productivity_table";

class ProductivityLogView extends Component {
  constructor() {
    super();
    this.state = {
      eventHistory: [
        {
          supplement_name: "Loading ... ",
          quantity: "Loading ... ",
          duration: "Loading ... ",
          time: null,
          source: "Loading ... "
        }
      ],
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
    fetch(`api/v1/productivity_log/?page=${page}`, {
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
        <AddProductivityEvent addSupplementEntry={this.addEventEntry} />
        <ProductivityLogTable
          supplementHistory={this.state.eventHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory}
          getSupplementHistory={this.getEventHistory}
        />
      </div>
    );
  }
}

export default ProductivityLogView;
