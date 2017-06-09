import React, { Component } from "react";
import { Redirect } from "react-router-dom";

export class CreateDemoUserView extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <div className="row approve-modal">
          <br />
          <div className="col-md-6 offset-sm-1">
            <br /><br /><br />
            <div className="card">
              <div className="card-header">
                <h3><strong>Create Demo User</strong></h3>
              </div>
              <div className="card-block">
                <form method="post" className="form-horizontal ">
                  <div className="col-md-11 form-group row">
                    <label className="form-control-label">
                      Hitting CREATE generates a demo user with randomly generated data to illustrate analytics.
                      {" "}
                      <br />
                      {" "}
                      <p>
                        {" "}
                        Demo users are temporary and will be deleted by the end of day.
                        {" "}
                      </p>
                    </label>
                  </div>
                </form>
              </div>
              <div className="card-footer">
                <button
                  type="submit"
                  className="btn btn-sm btn-success float-right"
                  id="create-username"
                  onClick={this.handleSubmit}
                >
                  <i className="fa fa-dot-circle-o" /> CREATE DEMO USER
                </button>&nbsp;
              </div>
            </div>
          </div>
        </div>
        <div id="special-signup-footer" />
      </div>
    );
  }
}
