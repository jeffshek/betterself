import React, { PropTypes, Component } from "react";
import CSSModules from "react-css-modules";

import styles from "../css/OpenSourceAndApplicationSupport.css";

class OpenSourceAndApplicationSupport extends React.Component {
  render() {
    return (
      <section styleName="content-deep-ocean">
        <div className="container text-center">

          <h1 className="font-weight-bold">
            TL;DR—we got frustrated at tracking supplements and habits, so we made an app.
          </h1>
          <h4>
            So stop wondering whether you’re doing things right, and start seeing results. Track what you’re putting into your body, and the decisions you make, and see what really matters. Make better decisions. Make a better you.
          </h4>

          <a
            href="https://github.com/jeffshek/betterself"
            className="btn btn-outline btn-outline-xl outline-light"
          >
            Made with <span className="fa fa-heart pomegranate" /> on GitHUb
          </a>
        </div>
      </section>
    );
  }
}

export default CSSModules(OpenSourceAndApplicationSupport, styles);
