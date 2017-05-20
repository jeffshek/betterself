import React, { Component, PropTypes } from "react";
import moment from "moment";
import { LoadingStyle } from "../animations/LoadingStyle";

const SupplementHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  const supplementName = data.supplement_name;
  const servingSize = data.quantity;
  const source = data.source;
  const supplementTime = data.time;
  const duration = data.duration;
  const timeFormatted = moment(supplementTime).format(
    "dddd, MMMM Do YYYY, h:mm:ss a"
  );

  return (
    <tr>
      <td>{supplementName}</td>
      <td>{servingSize}</td>
      <td>{timeFormatted}</td>
      <td>{duration}</td>
      <td>
        <span className="badge badge-success">{source}</span>
      </td>
    </tr>
  );
};

const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Supplement</th>
      <th>Serving Size</th>
      <th>Supplement Time</th>
      <th>Duration (Minutes)</th>
      <th>Source</th>
    </tr>
  </thead>
);

export class SupplementsHistoryTableList extends Component {
  constructor() {
    super();
    this.getPageResults = this.getPageResults.bind(this);
  }

  getPageResults(page) {
    if (page === 0 || page > this.props.lastPageNumber) {
      return;
    }

    this.props.getSupplementHistory(page);
  }

  getTableRender() {
    const historicalData = this.props.supplementHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SupplementHistoryRow key={key} object={historicalData[key]} />
          ))}
        </tbody>
      </table>
    );
  }

  getNavPaginationControlRender() {
    const currentPageNumber = this.props.currentPageNumber;
    const lastPageNumber = this.props.lastPageNumber;

    return (
      <nav>
        <ul className="pagination">
          <li className="page-item">
            <a
              className="page-link"
              onClick={e => {
                this.getPageResults(1);
              }}
            >
              First
            </a>
          </li>
          <li className="page-item">
            <a
              className="page-link"
              onClick={e => {
                this.getPageResults(currentPageNumber - 1);
              }}
            >
              Prev
            </a>
          </li>
          <li className="page-item active">
            <a className="page-link">{currentPageNumber}</a>
          </li>
          <li className="page-item">
            <a
              className="page-link"
              onClick={e => {
                this.getPageResults(currentPageNumber + 1);
              }}
            >
              {currentPageNumber + 1}
            </a>
          </li>
          <li className="page-item">
            <a className="page-link">...</a>
          </li>
          <li className="page-item">
            <a
              className="page-link"
              onClick={e => {
                this.getPageResults(lastPageNumber);
              }}
            >
              Last
            </a>
          </li>
        </ul>
      </nav>
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
          ? <LoadingStyle />
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
