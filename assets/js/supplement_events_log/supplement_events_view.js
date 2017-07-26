import React, { Component } from "react";

import { AddSupplementEvent } from "./add_supplement_event";
import { SupplementEntryLogTable } from "./supplement_events_table";
import { EventLogView } from "../resources_table/resource_view";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";

export class SupplementEventsLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "supplement_events";
    this.state.loadedSupplements = false;
  }

  componentDidMount() {
    // Override base class of componentDidMount
    this.getEventHistory();
    this.getPossibleSupplements();
  }

  getPossibleSupplements() {
    fetch("/api/v1/supplements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ supplements: responseData });
        this.setState({ loadedSupplements: true });
      });
  }

  render() {
    return (
      <div>
        <AddSupplementEvent addEventEntry={this.addEventEntry} />
        <SupplementEntryLogTable
          eventHistory={this.state.eventHistory}
          supplements={this.state.supplements}
          loadedSupplements={this.state.loadedSupplements}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory && this.state.loadedSupplements}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}
