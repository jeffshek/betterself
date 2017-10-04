import React from "react";
import { AddProductivityEvent } from "./add_productivity_event";
import { ProductivityLogTable } from "./productivity_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";

export class ProductivityLogView extends BasePaginatedLogView {
  constructor() {
    super();
    this.state = {
      eventHistory: [{}],
      loadedHistory: false
    };
    this.addEventEntry = this.addEventEntry.bind(this);
    this.getEventHistory = this.getEventHistory.bind(this);
    this.resourceName = "productivity_log";
  }

  render() {
    return (
      <div>
        <AddProductivityEvent addEventEntry={this.addEventEntry} />
        <ProductivityLogTable
          eventHistory={this.state.eventHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}
