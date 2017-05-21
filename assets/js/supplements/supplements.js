import React, { PropTypes, Component } from "react";

export class SupplementsView extends Component {
  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Add Supplement</strong>
        </div>
        <div className="card-block">
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label>Supplement Name</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Caffeine"
                />
              </div>
            </div>
          </div>

          <div className="row">
            <div className="form-group col-sm-4">
              <label>Vendor</label>
              <select className="form-control">
                <option>1</option>
              </select>
            </div>

          </div>

        </div>
      </div>
    );
  }
}
