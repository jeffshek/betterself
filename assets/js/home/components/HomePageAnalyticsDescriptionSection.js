import React, { PropTypes, Component } from "react";
import CSSModules from "react-css-modules";
import styles from "../css/HomePageAnalyticsDescriptionSection.css";
import {
  DASHBOARD_EXAMPLE_PATH,
  DASHBOARD_HEART_RATE,
  DASHBOARD_SUPPLEMENTS_HISTORY
} from "../../constants/image_paths";
import Slider from "react-slick";

class SimpleSlider extends React.Component {
  render() {
    const settings = {
      infinite: true,
      accessibility: true,
      adaptiveHeight: false,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1
    };
    return (
      <Slider {...settings}>
        <div>
          <img
            className="img-responsive dashboard-example"
            src={DASHBOARD_EXAMPLE_PATH}
          />
        </div>
        <div>
          <img
            className="img-responsive dashboard-example"
            src={DASHBOARD_HEART_RATE}
          />
        </div>
        <div>
          <img
            className="img-responsive dashboard-example"
            src={DASHBOARD_SUPPLEMENTS_HISTORY}
          />
        </div>
      </Slider>
    );
  }
}

class HomePageAnalyticsDescriptionSection extends React.Component {
  render() {
    return (
      <section styleName="description-block">
        <div className="container">
          <div className="row">
            <div className="col-lg-5 col-md-6 col-sm-12">
              <h1>Personalized Analytics</h1>
              <p styleName="lead-white">
                Ever wonder how your body is being impacted by your habits and diet? How sleep impacts decision making?
                {" "}
              </p>
              <p styleName="lead-white">
                Track your decisions, activities, and supplements to see what's really impacting you. What do your most creative days and weeks have in common? You've come to the right place.
              </p>
              <p styleName="lead-white">
                We collect no personal info. Open-sourced to give you the peace of mind that your data isn't being manipulated. All of your data can be safely exported in one easy click. You can also safely delete all your data in the control panel.
              </p>
            </div>
            <SimpleSlider />
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageAnalyticsDescriptionSection, styles);
