import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  SupplementHistoryRow,
  SupplementHistoryTableHeader
} from "./constants";

export class SupplementEntryLogTable extends BaseEventLogTable {
  constructor() {
    super();

    this.state = {
      modal: false,
      editObject: { name: null }
    };

    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/supplement_events/";
  }

  confirmDelete = (uuid, supplementName, supplementTime) => {
    const answer = confirm(
      `WARNING: THIS WILL DELETE THE FOLLOWING EVENT \n\n${supplementName} at ${supplementTime}!\n\nConfirm? `
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
        <SupplementHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SupplementHistoryRow
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
          <strong>Supplement History</strong>
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
