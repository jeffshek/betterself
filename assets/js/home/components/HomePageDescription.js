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
                Ever wondered how your body is impacted by the supplements you take, your diet, or your personal habits? Ever thought about if sleep impacts your decision making?
                <br />
              </p>
              <p styleName="content-1-4-lead">
                The BetterSelf dashboard lets you track supplements, sleep patterns, productivity, heart rate, exercise, and happiness, across multiple integrations. See what’s working, what’s not, and whether you’re just pissing your money away on supplements you don’t need.
              </p>
              <p styleName="content-1-4-lead">
                Available on both iOS and Android devices, BetterSelf tracks your input and gives you measurable data that you can use to make real change in your life.
              </p>
              {/*Force redirect to take a different CSS, aka why we don't use Link*/}
              <div className="text-center">
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
              </div>

              <div className="row pad45">
                <div className="col-sm-6">
                  <h5>Compound Improvements.</h5>
                  <p>
                    Small improvements move glaciers. Track what's working for you (and what's not), and see where you can improve, with beautiful personalized analytics from historical data.
                  </p>
                </div>
                <div className="col-sm-6">
                  <h5>Privacy First.</h5>
                  <p>
                    We don't want your name or address. We're not here to sell your contact info. All we care about is improving your health and productivity anonymously. Open-sourced on GitHub.
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
