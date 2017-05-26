import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";

const confirmDelete = (uuid, supplementName, supplementTime) => {
  const answer = confirm(
    `WARNING: THIS WILL DELETE THE FOLLOWING EVENT \n\n${supplementName} at ${supplementTime}!\n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/supplement_events/", {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(
      // After deleting, just refresh the entire page. In the future, remove
      // from the array and setState
      location.reload()
    );
  }
};

const SupplementHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  const uuid = data.uuid;
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
        <div onClick={e => confirmDelete(uuid, supplementName, timeFormatted)}>
          <div className="remove-icon">
            <i className="fa fa-remove" />
          </div>
        </div>
      </td>
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
      <th><center>Action</center></th>
      <th>Source</th>
    </tr>
  </thead>
);

export class SupplementsHistoryTable extends Component {
  constructor() {
    super();
    this.getPageResults = this.getPageResults.bind(this);
  }

  getPageResults(page) {
    if (page === 0 || page > this.props.lastPageNumber) {
      return;
    }

    this.props.getEventHistory(page);
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
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

  getPaginationPageLinkRender(page, page_link_verbose_title) {
    // page_link_verbose_title might be "Last", "First" or just a number
    return (
      <li className="page-item">
        <a
          className="page-link"
          onClick={e => {
            this.getPageResults(page);
          }}
        >
          {page_link_verbose_title}
        </a>
      </li>
    );
  }

  getPaginationActivePageLinkRender() {
    const currentPageNumber = this.props.currentPageNumber;

    return (
      <li className="page-item active">
        <a className="page-link">{currentPageNumber}</a>
      </li>
    );
  }

  checkCurrentPageIsLastName() {
    const currentPageNumber = this.props.currentPageNumber;
    const lastPageNumber = this.props.lastPageNumber;

    if (currentPageNumber === lastPageNumber) {
      return true;
    }
  }

  getNavPaginationControlRender() {
    const currentPageNumber = this.props.currentPageNumber;
    const lastPageNumber = this.props.lastPageNumber;

    return (
      <nav>
        <ul className="pagination">
          {this.getPaginationPageLinkRender(1, "First")}
          {this.getPaginationPageLinkRender(currentPageNumber - 1, "Prev")}
          {this.getPaginationActivePageLinkRender()}
          {this.checkCurrentPageIsLastName()
            ? ""
            : this.getPaginationPageLinkRender(
                currentPageNumber + 1,
                currentPageNumber + 1
              )}
          <li className="page-item">
            <a className="page-link">...</a>
          </li>
          {this.getPaginationPageLinkRender(currentPageNumber + 1, "Next")}
          {this.getPaginationPageLinkRender(lastPageNumber, "Last")}
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
