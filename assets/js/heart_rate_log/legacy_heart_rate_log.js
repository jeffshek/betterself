import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/datesAndTimes";

const heartRateHistory = {
  labels: [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ],
  datasets: [
    {
      label: "Average Heart Rate (Monthly)",
      fill: false,
      lineTension: 0.4,
      backgroundColor: "rgba(75,192,192,0.4)",
      borderColor: "rgba(25,52,65,1)",
      borderCapStyle: "butt",
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: "miter",
      pointBorderColor: "rgba(1,1,1,1)",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(1,1,1,1)",
      pointHoverBorderColor: "rgba(220,220,220,1)",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [65, 59, 80, 81, 56, 55, 63, 65, 66, 82, 72, 52]
    }
  ]
};

const heartRateData = [
  {
    time: Date.now(),
    heart_rate: 60,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 60,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 60,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 50,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 45,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 72,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 90,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 100,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 60,
    input: "FitBit"
  },
  {
    time: Date.now(),
    heart_rate: 60,
    input: "FitBit"
  }
];

const HeartRateRowHistory = props => {
  const { time, input } = props.object;
  const heartRate = props.object.heart_rate;
  const timeFormatted = moment(time).format(READABLE_DATE_TIME_FORMAT);

  return (
    <tr>
      <td>{timeFormatted}</td>
      <td>{heartRate}</td>
      <td>{input}</td>
    </tr>
  );
};

class HeartRateLogTableView extends Component {
  render() {
    const heartRateDataKeys = Object.keys(heartRateData);

    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Heart Rate History</strong>
        </div>
        <div className="card-block">
          <table className="table table-bordered table-striped table-condensed">
            <thead>
              <tr>
                <th>Time</th>
                <th>Heart Rate</th>
                <th>Input</th>
              </tr>
            </thead>
            <tbody>
              {heartRateDataKeys.map(key => (
                <HeartRateRowHistory key={key} object={heartRateData[key]} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}
const AddHeartRateLog = () => {
  return (
    <div className="card">
      <div className="card-header">
        <strong>Add Heart Rate Log</strong>
      </div>
      <div className="card-block">
        <div className="row">
          <div className="col-sm-12">
            <div className="form-group">
              <label>Heart Rate</label>
              <input
                type="text"
                className="form-control"
                placeholder="Heart Rate (BPM)"
              />
            </div>
          </div>
        </div>

        <div className="row">
          <div className="form-group col-sm-4">
            <label>Heart Rate</label>
            <select className="form-control">
              <option>1</option>
            </select>
          </div>

          <div className="form-group col-sm-4">
            <label>Time</label>
            <select className="form-control">
              <option>2014</option>
            </select>
          </div>

          <div className="col-sm-4">
            <div className="form-group">
              <label>Input Source</label>
              <input type="text" className="form-control" placeholder="123" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export class HeartRateLogView extends Component {
  render() {
    return (
      <div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Line
              data={heartRateHistory}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
        <AddHeartRateLog />
        <HeartRateLogTableView />
      </div>
    );
  }
}
