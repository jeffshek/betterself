import React from "react";

import { AddSupplementLog } from "./add_supplement_log";
import { SupplementLogTable } from "./supplement_log_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import {
  SUPPLEMENT_RESOURCE_URL,
  SUPPLEMENT_STACKS_RESOURCE_URL
} from "../constants/api_urls";

export class SupplementLogView extends BasePaginatedLogView {
  constructor() {
    super();
    this.resourceName = "supplement_events";
  }

  componentDidMount() {
    this.getEventHistory();
    this.getSupplements();
    this.getSupplementStacks();
  }

  getSupplements() {
    getFetchJSONAPI(SUPPLEMENT_RESOURCE_URL).then(responseData => {
      this.setState({ supplements: responseData });
    });
  }

  getSupplementStacks() {
    getFetchJSONAPI(SUPPLEMENT_STACKS_RESOURCE_URL).then(responseData => {
      this.setState({ supplementStacks: responseData });
    });
  }

  render() {
    return (
      <div>
        <AddSupplementLog
          addEventEntry={this.addEventEntry}
          supplements={this.state.supplements}
          supplementStacks={this.state.supplementStacks}
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
