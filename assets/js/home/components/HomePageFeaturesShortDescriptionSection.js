import React, { PropTypes, Component } from "react";
import CSSModules from "react-css-modules";
import FontAwesomeIconBox from "./FontAwesomeIconBox";

import styles from "../css/HomePageFeaturesShortDescriptionSection.css";

class HomePageFeaturesShortDescriptionSection extends React.Component {
  render() {
    return (
      <section styleName="content-format">
        <div className="container">
          <div className="row">
            <FontAwesomeIconBox
              icon="fa fa-pencil"
              header="Simple"
              description="BetterSelf accepts data in Excel files, and integrates with all major fitness trackers, syncing seamlessly to give the most accurate snapshot of you."
            />
            <FontAwesomeIconBox
              icon="fa fa-code"
              header="Privacy"
              description="We respect your privacy. Your data is confidential, and we don't store names or emails. BetterSelf even comes with a purge data option, so you can really make sure your information is secure."
            />
            <FontAwesomeIconBox
              icon="fa fa-search"
              header="Analytics"
              description="How many hours of sleep do you really need? Does fish oil actually help? BetterSelf helps you differentiate truth from placebo with real, measurable information."
            />
            <FontAwesomeIconBox
              icon="fa fa-mobile"
              header="Integrations"
              description="Track supplement or medication usage in seven seconds or less. Available (soon) on iOS and Android."
            />
          </div>
        </div>
      </section>
    );
  }
}

export default CSSModules(HomePageFeaturesShortDescriptionSection, styles);
