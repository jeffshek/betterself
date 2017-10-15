import React, { Component } from "react";
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
                What do your most creative days and weeks have in common? Will a hangover still impact you three days after the binge? Does your productivity really take a hit with only five hours of sleep?
                {" "}
              </p>
              <p styleName="lead-white">
                Track your decisions, activities, and supplements, to see what's really impacting you, in colourful, easy-to-understand graphs and charts.
              </p>
              <p styleName="lead-white">
                If you’ve ever wanted a meaningful way to see how your decisions affect your body, you've come to the right place.
              </p>

            </div>
            <div className="col-lg-8">
              <br />
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
