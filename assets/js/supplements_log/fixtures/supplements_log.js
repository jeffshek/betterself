import React, { PropTypes, Component } from "react";
const supplementHistory = {
  data: [
    {
      supplement_name: "Caffeine",
      quantity: 5,
      time: Date.now(),
      duration: 0,
      source: "Excel"
    },
    {
      supplement_name: "Piracetam",
      quantity: 10,
      time: moment(Date.now()).subtract(6, "days"),
      duration: 0,
      source: "Web"
    },
    {
      supplement_name: "Piracetam",
      quantity: 2,
      time: Date.now(),
      duration: 0,
      source: "Web"
    },
    {
      supplement_name: "Oxiracetam",
      quantity: 5,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Piracetam",
      quantity: 1,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Theanine",
      quantity: 10,
      time: Date.now(),
      duration: 11,
      source: "Web"
    },
    {
      supplement_name: "Alpha GPC",
      quantity: 2,
      duration: 30,
      time: Date.now(),
      source: "Web"
    }
  ]
};
