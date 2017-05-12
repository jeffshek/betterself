// HomePageFeaturesShortDescriptionSection
import React, { PropTypes, Component } from "react";
import CSSModules from 'react-css-modules';
import FontAwesomeIconBox from "./FontAwesomeIconBox"

import styles from '../css/HomePageFeaturesShortDescriptionSection.css'


class HomePageFeaturesShortDescriptionSection extends React.Component {
  render() {
    return (
      <section styleName="content-format">
        <div className="container">
          <div className="row">
            <FontAwesomeIconBox
              icon="fa fa-pencil"
              header="Simple"
              description="Integrates with all major fitness trackers. Automatically gets data to give the most accurate snapshot of &nbsp;you."
            />
            <FontAwesomeIconBox
              icon="fa fa-code"
              header="Privacy"
              description="We respect privacy. Your data is confidential and we don't store names or emails. Comes with a purge data option. &nbsp;"
            />
            <FontAwesomeIconBox
              icon="fa fa-search"
              header="Analytics"
              description="How many hours of sleep do you really need? Does fish oil actually help? We help you eliminate truth from placebo."
            />
            <FontAwesomeIconBox
              icon="fa fa-mobile"
              header="Integrations"
              description="Track supplement or medication usage in seven seconds or less. Available on iOS and Android."
            />
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageFeaturesShortDescriptionSection, styles)
