import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  ProductivityHistoryRow,
  ProductivityHistoryTableHeader
} from "./constants";

export class ProductivityLogTable extends BaseEventLogTable {
  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <ProductivityHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <ProductivityHistoryRow key={key} object={historicalData[key]} />
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
          <strong>Productivity History</strong>
        </div>
        {this.renderReady()}
      </div>
    );
  }
}
