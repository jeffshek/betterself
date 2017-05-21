import React, { PropTypes, Component } from "react";

export class AddSupplementView extends Component {
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
