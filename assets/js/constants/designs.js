import React, { Component } from "react";

export const TrueCheckBox = () => {
  return (
    <div className="true-icon">
      <i className="fa fa-check-circle" />
    </div>
  );
};

export const RenderTrueFalseCheckBox = boolFlag => {
  if (boolFlag) {
    return (
      <div className="true-icon">
        <i className="fa fa-check-circle" />
      </div>
    );
  } else {
    return (
      <div className="center-icon">
        <div className="remove-icon">
          <i className="fa fa-remove fa-1x" />
        </div>
      </div>
    );
  }
};
