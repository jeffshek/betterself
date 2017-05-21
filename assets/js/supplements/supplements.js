import React, { PropTypes, Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";

const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Name</th>
      <th>Vendor</th>
      <th>Date Added</th>
      <th>Ingredients</th>
      <th>Actions</th>
    </tr>
  </thead>
);

const SupplementRow = props => {
  const data = props.object;
  console.log(data);

  const name = data.name;
  const vendorName = data.vendor;
  const dateAdded = data.create_date;
  const ingredientsFormatted = data.ingredients;
  const timeFormatted = moment(dateAdded).format(
    "dddd, MMMM Do YYYY, h:mm:ss a"
  );

  return (
    <tr>
      <td>{name}</td>
      <td>{vendorName}</td>
      <td>{timeFormatted}</td>
      <td>{ingredientsFormatted}</td>
    </tr>
  );
};

class SupplementTable extends Component {
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
    // Fetch the specific page we want, defaulting at 1
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
        console.log(this.state.ready);
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
          {this.state.ready ? this.renderTable() : ""}
        </div>
      </div>
    );
  }
}

class AddSupplementView extends Component {
  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Create Supplement</strong> (Per Serving)
        </div>
        <div className="card-block">
          <form onSubmit={e => this.submitSupplementEvent(e)}>
            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Supplement Name</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Black Tea"
                />
              </div>
            </div>

            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Vendor</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Lipton"
                />

              </div>
            </div>

            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Ingredients</strong><sup>1</sup></label>
                <select className="form-control">
                  <option>Caffeine</option>
                </select>
                <select className="form-control">
                  <option>Theanine</option>
                </select>
              </div>
              <div className="form-group col-sm-4">
                <label><strong>Quantity</strong></label>
                <select className="form-control">
                  <option>75</option>
                </select>
                <select className="form-control">
                  <option>150</option>
                </select>

              </div>
              <div className="form-group col-sm-4">
                <label><strong>Measurement</strong></label>
                <select className="form-control">
                  <option>mg</option>
                </select>
                <select className="form-control">
                  <option>mg</option>
                </select>
              </div>

            </div>
            <div className="float-right">
              <button
                type="submit"
                id="supplement-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitSupplementEvent(e)}
              >
                <i className="fa fa-dot-circle-o" /> Add Supplement
              </button>
            </div>
          </form>
          <sup>1. Ingredients are optional inputs.</sup>
        </div>
      </div>
    );
  }
}

export class SupplementView extends Component {
  render() {
    return (
      <div>
        <AddSupplementView />
        <SupplementTable />
      </div>
    );
  }
}
