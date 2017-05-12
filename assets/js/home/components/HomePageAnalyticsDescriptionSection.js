import React, { PropTypes, Component } from "react";
import CSSModules from 'react-css-modules';
import styles from '../css/HomePageAnalyticsDescriptionSection.css'

import {DASHBOARD_EXAMPLE_PATH} from "../../fragments/image_paths";

class HomePageAnalyticsDescriptionSection extends React.Component {
  render() {
    return (
    <section styleName="description-block">
      <div className="container">
        <div className="row">
          <div className="col-lg-6 col-md-6 col-sm-12">
            <h1>Your Personalized Analytics</h1>
            <p styleName="lead-white">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec consectetur dui eget massa iaculis placerat. Cras posuere dictum mauris, porta posuere urna elementum id. Donec scelerisque placerat quam sed varius. Phasellus dolor mi, molestie sed lorem at, interdum dapibus sem. Phasellus lorem mauris, eleifend quis metus et, accumsan dapibus elit. Morbi ut nibh eget orci pharetra cursus non eget massa. Morbi sed libero sodales, dignissim elit ac, elementum leo.
            </p>
          </div>
          <div className="col-lg-5 col-lg-offset-1 col-md-6 col-sm-12">
            <br />
            <a href="https://www.betterself.io">
              <img className="img-responsive" src={DASHBOARD_EXAMPLE_PATH} />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
  }
}

export default CSSModules(HomePageAnalyticsDescriptionSection, styles)
