import React, { PropTypes, Component } from "react";
import CSSModules from "react-css-modules";
import styles from "../css/HomePageDescription.css";

import {
  DASHBOARD_INDEX_URL,
  DEMO_SIGNUP_URL,
  SIGNUP_URL
} from "../../constants/urls";

class HomePageDescriptionSection extends React.Component {
  render() {
    return (
      <section id="content-1-4" styleName="content-block-description">
        <div
          className="col-md-5 col-sm-3 pull-left"
          styleName="image-container"
        >
          <div styleName="background-image-holder" />
        </div>
        <div className="container">
          <div className="row">
            <div className="col-md-6 col-md-offset-6 col-sm-8 col-sm-offset-4 content clearfix">
              <h1>Your Body's Dashboard</h1>
              <p styleName="content-1-4-lead">
                Track supplements, sleep, productivity, heart rate, exercise, and happiness across multiple integrations.
                <br />
              </p>
              {/*Force redirect to take a different CSS, aka why we don't use Link*/}
              <a
                href={DEMO_SIGNUP_URL}
                className="btn btn-outline btn-outline-lg outline-dark"
              >
                Try the demo
              </a>
              &nbsp; or &nbsp;
              <a
                href={SIGNUP_URL}
                className="btn btn-outline btn-outline-lg outline-dark"
              >
                Sign up (free)
              </a>
              <div className="row pad45">
                <div className="col-sm-6">
                  <h5>Compound Improvements.</h5>
                  <p>
                    Small improvements move glaciers. Track what's working for you (and what's not). Beautiful personalized analytics from historical data.
                  </p>
                </div>
                <div className="col-sm-6">
                  <h5>Privacy First.</h5>
                  <p>
                    We're not here to sell your contact info. We don't want your name or address. All we care about is improving health and productivity anonymously. Open-sourced on GitHub.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageDescriptionSection, styles);
