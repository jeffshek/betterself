import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseLogTable } from "../resources_table/resource_table";
import { MoodHistoryRow, MoodHistoryTableHeader } from "./constants";

export class MoodEntryLogTable extends BaseLogTable {
  constructor() {
    super();
    this.resourceURL = "/api/v1/mood_logs/";
  }

  confirmDelete = (uuid, time, value, notes) => {
    const answer = confirm(
      `WARNING: This will delete the following Mood Log \n\nTime: ${time} \nMood Value: ${value} \nNotes: ${notes} \n\nConfirm?`
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  };

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <MoodHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <MoodHistoryRow
              key={key}
              object={historicalData[key]}
              confirmDelete={this.confirmDelete}
            />
          ))}
        </tbody>
      </table>
    );
  }

  renderReady() {
    if (!this.props.renderReady) {
      return <CubeLoadingStyle />;
    }

    return (
      <div className="card-block">
        <div className="float-right">
          {this.getNavPaginationControlRender()}
        </div>
        {this.getTableRender()}
        {this.getNavPaginationControlRender()}
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Mood History</strong>
        </div>
        {this.renderReady()}
      </div>
    );
  }
}
