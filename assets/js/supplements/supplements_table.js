import React, { PropTypes, Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";
import { Link } from "react-router-dom";
import { SupplementHistoryTableHeader, SupplementRow } from "./constants";

export class SupplementTable extends Component {
  constructor() {
    super();
    this.state = {
      ready: false
    };
  }

  componentDidMount() {
    this.getSupplements();
  }

  getSupplements() {
    fetch(`api/v1/supplements/`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({
          supplements: responseData
        });
        this.setState({ ready: true });
      });
  }

  renderTable() {
    const supplements = this.state.supplements;
    const supplementsKeys = Object.keys(supplements);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementHistoryTableHeader />
        <tbody>
          {supplementsKeys.map(key => (
            <SupplementRow key={key} object={supplements[key]} />
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
          <strong>Supplements</strong>
        </div>
        {this.state.ready ? this.renderTable() : ""}
      </div>
    );
  }
}
