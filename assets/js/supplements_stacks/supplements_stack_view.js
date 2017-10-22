import React from "react";

import { AddSupplementsStack } from "./add_supplements_stack";
import { SupplementsStackTable } from "./supplements_stack_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";

export class SupplementsStackView extends BasePaginatedLogView {
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
        <AddSupplementsStack
          addEventEntry={this.addEventEntry}
          supplements={this.state.supplements}
        />
        <SupplementsStackTable
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
