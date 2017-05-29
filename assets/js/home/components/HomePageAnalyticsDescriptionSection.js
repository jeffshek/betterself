import React, { PropTypes, Component } from "react";
import CSSModules from "react-css-modules";
import styles from "../css/HomePageAnalyticsDescriptionSection.css";

import { DASHBOARD_EXAMPLE_PATH } from "../../constants/image_paths";

class HomePageAnalyticsDescriptionSection extends React.Component {
  render() {
    return (
      <section styleName="description-block">
        <div className="container">
          <div className="row">
            <div className="col-lg-6 col-md-6 col-sm-12">
              <h1>Your Personalized Analytics</h1>
              <p styleName="lead-white">
                Have you ever wondered how your body is being impacted by your habits and diet? How sleep impacts decision making?
                {" "}
                <div />
              </p>
              <p styleName="lead-white">
                Track your decisions, activities, and supplements to see what's really impacting you. Want to see what all your most productive days and weeks have in common? You've come to the right place.
              </p>
              <p styleName="lead-white">
                Fully open-sourced to give you the peace of mind that your data isn't being manipulated. All of your data can be safely exported in one easy click. You can also safely delete all your data in the control panel.
              </p>
            </div>
            <div className="col-lg-5 col-lg-offset-1 col-md-6 col-sm-12">
              <br />
              <img className="img-responsive" src={DASHBOARD_EXAMPLE_PATH} />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageAnalyticsDescriptionSection, styles);
