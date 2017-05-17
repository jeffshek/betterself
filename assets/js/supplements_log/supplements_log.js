import React, { Component } from "react";
import moment from "moment";
import Datetime from "react-datetime";

const supplementHistory = {
  data: [
    {
      supplement_name: "Caffeine",
      quantity: 5,
      time: Date.now(),
      duration: 0,
      source: "Excel"
    },
    {
      supplement_name: "Piracetam",
      quantity: 10,
      time: moment(Date.now()).subtract(6, "days"),
      duration: 0,
      source: "Web"
    },
    {
      supplement_name: "Piracetam",
      quantity: 2,
      time: Date.now(),
      duration: 0,
      source: "Web"
    },
    {
      supplement_name: "Oxiracetam",
      quantity: 5,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Piracetam",
      quantity: 1,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Theanine",
      quantity: 10,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Alpha GPC",
      quantity: 2,
      duration: 30,
      time: Date.now(),
      source: "Web"
    }
  ]
};

const SupplementRowHistory = props => {
  const data = props.object;

  const supplementName = data.supplement_name;
  const servingSize = data.quantity;
  const source = data.source;
  const supplementTime = data.time;
  const duration = 0;
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

const JSON_AUTHORIZATION_HEADERS = {
  Authorization: `Token ${localStorage.token}`
};

class SupplementsHistoryTableList extends Component {
  constructor() {
    super();
    this.state = {
      supplementHistory: [
        {
          supplement_name: "Loading ... ",
          quantity: "Loading ... ",
          duration: "Loading ... ",
          time: null,
          source: "Loading ... "
        }
      ]
    };
  }

  componentDidMount() {
    this.getSupplementHistory();
  }

  getSupplementHistory() {
    fetch("api/v1/supplement_events", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ supplementHistory: responseData });
      });
  }

  render() {
    const historicalData = this.state.supplementHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplement History</strong>
        </div>
        <div className="card-block">
          <table className="table table-bordered table-striped table-condensed">
            <thead>
              <tr>
                <th>Supplement</th>
                <th>Serving Size</th>
                <th>Supplement Time</th>
                <th>Duration (Minutes)</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {historicalDataKeys.map(key => (
                <SupplementRowHistory key={key} object={historicalData[key]} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

class AddSupplementLog extends Component {
  constructor(props) {
    super(props);
    this.state = {
      supplementNames: []
    };
  }

  getPossibleSupplements() {
    fetch("/api/v1/supplements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const supplementNames = responseData.map(object => object.name);
        this.setState({ supplementNames: supplementNames });
      });
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Add Supplement Entry</strong>
        </div>

        <div className="card-block">
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label>Supplement</label>
                <select className="form-control">
                  {this.state.supplementNames.map(object => (
                    <option key={object}>{object}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="form-group col-sm-4">
              <label>Quantity (Serving Size)</label>
              <input type="text" className="form-control" placeholder="1" />
            </div>
            <div className="form-group col-sm-4">
              <label>Date / Time of Ingestion</label>
              <Datetime />
            </div>
            <div className="col-sm-4">
              <div className="form-group">
                <label>Duration (Minutes)</label>
                <input type="text" className="form-control" placeholder="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

class SupplementsLogView extends Component {
  render() {
    return (
      <div>
        <AddSupplementLog />
        <SupplementsHistoryTableList />
      </div>
    );
  }
}

export default SupplementsLogView;
