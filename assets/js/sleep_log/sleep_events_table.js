import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { SleepHistoryRow, SleepHistoryTableHeader } from "./constants";

export class SleepEntryLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/sleep_activities/";
  }

  confirmDelete(uuid, startTime, endTime) {
    const answer = confirm(
      `WARNING: This will delete the following Sleep Log \n\nStart: ${startTime} \nEnd: ${endTime} \n\nConfirm?`
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SleepHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SleepHistoryRow
              key={key}
              object={historicalData[key]}
              confirmDelete={this.confirmDelete}
            />
          ))}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Sleep History</strong>
        </div>
        {/*Conditional loading if ready to review or not yet*/}
        {!this.props.renderReady
          ? <CubeLoadingStyle />
          : <div className="card-block">
              <div className="float-right">
                {this.getNavPaginationControlRender()}
              </div>
              {this.getTableRender()}
              {this.getNavPaginationControlRender()}
            </div>}
      </div>
    );
  }
}
