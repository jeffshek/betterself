import React, { Component } from "react";

export class SignupView extends Component {
  render() {
    return (
      <div>
        <div className="row approve-modal">
          <br />

          <div className="col-md-6 offset-sm-1">
            <br /><br /><br />
            <div className="card">
              <div className="card-header">
                <strong>Sign Up</strong>
              </div>
              <div className="card-block">
                <form action="" method="post" className="form-horizontal ">
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label">
                      Username
                    </label>
                    <div className="col-md-9">
                      <input
                        type="username"
                        className="form-control"
                        placeholder="Create Username .."
                      />
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label">
                      Password
                    </label>
                    <div className="col-md-9">
                      <input
                        type="password"
                        id="hf-password"
                        name="hf-password"
                        className="form-control"
                        placeholder="Enter Password.."
                      />
                    </div>
                  </div>
                </form>
              </div>
              <div className="card-footer">
                <button
                  type="submit"
                  className="btn btn-sm btn-success float-right"
                  id="create-username"
                >
                  <i className="fa fa-dot-circle-o" /> Submit
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
