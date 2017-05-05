import React, { PropTypes, Component } from "react";
import { DASHBOARD_EXAMPLE_PATH } from "../fragments/image_paths";
import { DASHBOARD_INDEX_URL } from "../urls/constants";
import { Link } from "react-router-dom";
import styles from "./home.css"
import featureBox from "./feature_box.css"

export const FontAwesomeIconBox = props => {
  return (
    <div className="col-md-3 col-sm-6 col-xs-12">
      {/*<div className = { featureBox.feature }>*/}
      <div className="feature-box">
        <div className="icon">
          {/*Don't know how to style this correctly, putting a space is good enough, slightly embarrassed. */}
          &nbsp;
          <span className={props.icon} />
          &nbsp;
        </div>
        <h3>{props.header}</h3>
        <p>{props.description}</p>
      </div>
    </div>
  );
};

export const HomePageDescriptionSection = () => {
  return (
    <section id="content-1-4" className="content-block-nopad content-1-4">
      <div className="image-container col-md-5 col-sm-3 pull-left">
        <div className="background-image-holder" />
      </div>
      <div className="container">
        <div className="row">
          <div className="col-md-6 col-md-offset-6 col-sm-8 col-sm-offset-4 content clearfix">
            <h1>Your body's dashboard</h1>
            <p className="lead">
              Track supplements, sleep, productivity, heart rate, exercise, and happiness across fifteen integrations.
              <br />
            </p>
            <Link
              to={DASHBOARD_INDEX_URL}
              className="btn btn-outline btn-outline-lg outline-dark"
            >
              Try the demo
            </Link>
            <div className="row pad45">
              <div className="col-sm-6">
                <h5>Compound Improvements.</h5>
                <p>
                  Small improvements move glaciers. Track what's working for you (and what's not). We can text or email reminders to keep your medications and supplements on track. Comes with beautiful personalized analytics from best-in-class algorithms.
                </p>
              </div>
              <div className="col-sm-6">
                <h5>Privacy First.</h5>
                <p>
                  We're not here to sell your contact info to anyone else. We don't want your name or address. All we care about is improving health and productivity for our anonymous users. Open-sourced on GitHub.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

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
      <HomePageDescriptionSection />
      <HomePageAnalyticsDescriptionSection />
      <HomePageFeaturesShortDescriptionSection />
      <OpenSourceAndApplicationSupport />
    </div>
  );
};
