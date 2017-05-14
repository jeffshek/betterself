import React, { Component } from "react";
import { Authenticator } from "./auth";
import { Redirect, withRouter } from "react-router-dom";
import { LOGIN_LEDGE_PHOTO_PATH } from "../constants/image_paths";
import LoggedOutHeader from "../header/external_header";
import Footer from "../footer/footer";

const LoginPageSideImage = () => {
  return (
    <div className="col-md-6 col-md-offset-1">
      <img src={LOGIN_LEDGE_PHOTO_PATH} width="100%" />
    </div>
  );
};

export default class LoginView extends Component {
  state = {
    redirectToReferrer: false
  };

  handleSubmit(event) {
    event.preventDefault();

    let username = this.username.value;
    let password = this.password.value;

    Authenticator.login(username, password, loggedIn => {
      if (loggedIn) {
        this.setState({ redirectToReferrer: true });
      }
    });
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    if (redirectToReferrer) {
      return <Redirect to={from} />;
    }

    return (
      <div>
        <LoggedOutHeader />
        <section
          id="promo-1"
          className="content-block promo-2 min-height-600px bg-black"
        >
          <div className="container">
            <div className="row">
              <div className="col-md-5">
                <br />

                <h2>Please Login</h2>

                <p><br /></p>

                <form onSubmit={e => this.handleSubmit(e)}>
                  <div className="row">
                    <div className="col-md-6">
                      <div className="form-group">
                        <input
                          type="text"
                          placeholder="Username"
                          className="form-control"
                          ref={input => {
                            this.username = input;
                          }}
                        />
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="form-group">
                        <input
                          type="password"
                          placeholder="Password"
                          className="form-control"
                          ref={input => {
                            this.password = input;
                          }}
                        />
                      </div>
                    </div>
                  </div>
                  <button className="btn btn-primary btn-block" type="submit">
                    Login
                  </button>
                </form>
              </div>
              <br />
              <LoginPageSideImage />
            </div>
          </div>
        </section>
      </div>
    );
  }
}
