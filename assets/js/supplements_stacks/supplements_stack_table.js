import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseLogTable } from "../resources_table/resource_table";
import { SupplementsStackRow, SupplementStackTableHeader } from "./constants";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class SupplementsStackTable extends BaseLogTable {
  constructor() {
    super();

    this.state = {
      supplementsStacks: [],
      renderReady: false
    };

    this.resourceURL = "/api/v1/supplements_stacks/";
  }

  componentDidMount() {
    this.getSupplementsStacks();
  }

  //getReminders() {
  //  const url = "api/v1/supplement_reminders/";
  //  getFetchJSONAPI(url).then(responseData => {
  //    this.setState({ supplementReminders: responseData });
  //  });
  //}

  getSupplementsStacks() {
    const url = "api/v1/supplements_stacks";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({
        supplementsStacks: responseData,
        renderReady: true
      });
    });
  }

  getTableRender() {
    const historicalData = this.state.supplementsStacks;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementStackTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SupplementsStackRow key={key} object={historicalData[key]} />
          ))}
        </tbody>
      </table>
    );
  }

  renderReady() {
    if (!this.state.renderReady) {
      return <CubeLoadingStyle />;
    }
    return (
      <div className="card-block">
        {this.getTableRender()}
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplement Stacks</strong>
        </div>
        {this.renderReady()}
      </div>
    );
  }
}
