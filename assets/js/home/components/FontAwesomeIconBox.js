import React, { Component } from "react";
import CSSModules from "react-css-modules";
import styles from "../css/FontAwesomeIconBox.css";

class FontAwesomeIconBox extends Component {
  render() {
    return (
      <div className="col-md-3 col-sm-6 col-xs-12">
        <div styleName="feature-box">
          <div styleName="icon">
            &nbsp;
            <span className={this.props.icon} />
            &nbsp;
          </div>
          <h3>{this.props.header}</h3>
          <p>{this.props.description}</p>
        </div>
      </div>
    );
  }
}

export default CSSModules(FontAwesomeIconBox, styles);
