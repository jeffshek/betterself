import React, { PropTypes, Component } from "react";
import { DASHBOARD_EXAMPLE_PATH } from "../fragments/image_paths";

import { Link } from "react-router-dom";
import LoggedOutHeader from "../header/external_header";

import Footer from "../fragments/footer";
import FontAwesomeIconBox from "./FontAwesomeIconBox"
import HomePageDescriptionSection from "./HomePageDescription"
import CSSModules from 'react-css-modules';

import styles from '../../../betterself/static/css/pinegrow/legacy.css'

const HomePageAnalyticsDescriptionSection = () => {
  return (
    <section className="content-1-5 content-block bg-deepocean">
      <div className="container">
        <div className="row">
          <div className="col-lg-6 col-md-6 col-sm-12">
            <h1>Your Personalized Analytics</h1>
            <p className="lead white">
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
};

const HomePageFeaturesShortDescriptionSection = () => {
  return (
    <section id="content-3-5" className="content-block content-3-5">
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
};

const OpenSourceAndApplicationSupport = () => {
  return (
    <section
      id="content-2-1"
      className="content-block content-2-1 bg-deepocean"
    >
      <div className="container text-center">
        <a
          href="https://github.com/jeffshek/betterself"
          className="btn btn-outline btn-outline-xl outline-light"
        >
          Made with <span className="fa fa-heart pomegranate" /> on GitHUb
        </a>
        <h2>
          Track your progress on <b>iOS</b> or <b>Android</b>&nbsp;devices.
        </h2>
      </div>
    </section>
  );
};

export const HomePage = () => {
  return (
    <div>
      <LoggedOutHeader />
      <HomePageDescriptionSection />
      <HomePageAnalyticsDescriptionSection />
      <HomePageFeaturesShortDescriptionSection />
      <OpenSourceAndApplicationSupport />
      <Footer />
    </div>
  );
};
