import React from "react";

import { AddSupplementLog } from "./add_supplement_log";
import { SupplementLogTable } from "./supplement_log_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class SupplementLogView extends BasePaginatedLogView {
  constructor() {
    super();
    this.resourceName = "supplement_events";
  }

  componentDidMount() {
    this.getEventHistory();
    this.getSupplements();
  }

  getSupplements() {
    const url = "/api/v1/supplements/";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ supplements: responseData });
    });
  }

  render() {
    return (
      <div>
        <AddSupplementLog
          addEventEntry={this.addEventEntry}
          supplements={this.state.supplements}
        />
        <SupplementLogTable
          eventHistory={this.state.eventHistory}
          supplements={this.state.supplements}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory && this.state.supplements}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}
