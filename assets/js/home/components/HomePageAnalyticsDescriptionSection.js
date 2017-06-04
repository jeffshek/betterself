import React, { Component, PropTypes } from "react";
import CSSModules from "react-css-modules";
import styles from "../css/HomePageAnalyticsDescriptionSection.css";
import { DASHBOARD_EXAMPLE_PATH } from "../../constants/image_paths";

class HomePageAnalyticsDescriptionSection extends React.Component {
  render() {
    return (
      <section styleName="description-block">
        <div className="container">
          <div className="row">
            <div className="col-lg-4 col-md-3 col-sm-12">
              <h1>Personalized Analytics</h1>
              <p styleName="lead-white">
                Ever wonder how your body is being impacted by supplements, diet or habits? How sleep impacts decision making?
                {" "}
              </p>
              <p styleName="lead-white">
                Track decisions, activities, and supplements to see what's really impacting you. What do your most creative days and weeks have in common? You've come to the right place.
              </p>
            </div>
            <div className="col-lg-8">
              <img
                className="img-responsive dashboard-example"
                src={DASHBOARD_EXAMPLE_PATH}
              />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageAnalyticsDescriptionSection, styles);
