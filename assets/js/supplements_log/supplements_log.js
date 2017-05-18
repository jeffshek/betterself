import React, { Component } from "react";
import moment from "moment";
import Datetime from "react-datetime";

const JSON_AUTHORIZATION_HEADERS = {
  Authorization: `Token ${localStorage.token}`
};

const LoadingStyle = () => (
  <div>
    <div className="sk-cube-grid">
      <div className="sk-cube sk-cube1" />
      <div className="sk-cube sk-cube2" />
      <div className="sk-cube sk-cube3" />
      <div className="sk-cube sk-cube4" />
      <div className="sk-cube sk-cube5" />
      <div className="sk-cube sk-cube6" />
      <div className="sk-cube sk-cube7" />
      <div className="sk-cube sk-cube8" />
      <div className="sk-cube sk-cube9" />
    </div>
  </div>
);

const SupplementHistoryRow = props => {
  // Set the data point for easier reference
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
      ],
      loadedSupplementHistory: false
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
        // this.setState({ loadedSupplementHistory: true });
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
        {/*This kind of looks like crap with the Loading Style */}
        {!this.state.loadedSupplementHistory
          ? <LoadingStyle />
          : <div className="card-block">
              <table className="table table-bordered table-striped table-condensed">
                <SupplementHistoryTableHeader />
                <tbody>
                  {historicalDataKeys.map(key => (
                    <SupplementHistoryRow
                      key={key}
                      object={historicalData[key]}
                    />
                  ))}
                </tbody>
              </table>
            </div>}
      </div>
    );
  }
}

class AddSupplementLog extends Component {
  constructor(props) {
    super(props);
    this.state = {
      supplementNames: [],
      formSupplementDateTime: moment()
    };

    this.submitSupplementEvent = this.submitSupplementEvent.bind(this);
    this.handleChange = this.handleChange.bind(this);
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

  submitSupplementEvent(e) {
    e.preventDefault();
  }

  handleChange(moment) {
    console.log(moment);
    this.setState({ formSupplementDateTime: moment });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Add Supplement Entry</strong>
        </div>

        <div className="card-block">
          <form onSubmit={e => this.submitSupplementEvent(e)}>
            <div className="row">
              <div className="col-sm-12">
                <div className="form-group">
                  <label>Supplement</label>
                  <select
                    className="form-control"
                    ref={input => this.supplementName = input}
                  >
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
                <input
                  type="text"
                  className="form-control"
                  defaultValue="3"
                  ref={input => this.servingSize = input}
                />
              </div>
              <div className="form-group col-sm-4">
                <label>Date / Time of Ingestion</label>
                <Datetime
                  onChange={this.handleChange}
                  value={this.state.formSupplementDateTime}
                />
              </div>
              <div className="col-sm-4">
                <div className="form-group">
                  <label>Duration (Minutes)</label>
                  <input
                    type="text"
                    className="form-control"
                    defaultValue="0"
                    ref={input => this.durationMinutes = input}
                  />
                </div>
              </div>
            </div>
            <div className="float-right">
              <button
                type="submit"
                id="supplement-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitSupplementEvent(e)}
              >
                <i className="fa fa-dot-circle-o" /> Submit
              </button>
            </div>
          </form>
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
