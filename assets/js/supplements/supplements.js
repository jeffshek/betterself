import React, { Component } from 'react';
import moment from 'moment';

const supplementHistory = {
  data: [
    {
      name: 'Caffeine',
      serving_size: 5,
      supplement_time: Date.now(),
      duration: 0,
      source: 'Excel'
    },
    {
      name: 'Piracetam',
      serving_size: 10,
      supplement_time: moment(Date.now()).subtract(6, 'days'),
      duration: 0,
      source: 'Web'
    },
    {
      name: 'Piracetam',
      serving_size: 2,
      supplement_time: Date.now(),
      duration: 0,
      source: 'Web'
    },
    {
      name: 'Oxiracetam',
      serving_size: 5,
      supplement_time: Date.now(),
      duration: 11,
      source: 'Web'
    },
    {
      name: 'Piracetam',
      serving_size: 1,
      supplement_time: Date.now(),
      duration: 11,
      source: 'Web'
    },
    {
      name: 'Theanine',
      serving_size: 10,
      supplement_time: Date.now(),
      duration: 11,
      source: 'Web'
    },
    {
      name: 'Alpha GPC',
      serving_size: 2,
      duration: 30,
      supplement_time: Date.now(),
      source: 'Web'
    },
  ]
}

const SupplementRowHistory = props => {
  const {name, source, duration} = props.object
  // Remap this from backend style to frontend
  const servingSize = props.object.serving_size
  const supplementTime = props.object.supplement_time
  const timeFormatted = moment(supplementTime).format("dddd, MMMM Do YYYY, h:mm:ss a")

  return (
    <tr>
      <td>{name}</td>
      <td>{servingSize}</td>
      <td>{timeFormatted}</td>
      <td>{duration}</td>
      <td>
        <span className="badge badge-success">{source}</span>
      </td>
    </tr>
  )
}

class SupplementsTableList extends Component {

  render() {
    const historicalData = supplementHistory.data
    const historicalDataKeys = Object.keys(historicalData)

    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplement History</strong>
        </div>
        <div className="card-block">
          <table className="table table-bordered table-striped table-condensed">
            <thead>
              <tr>
                <th>Supplement</th>
                <th>Serving Size</th>
                <th>Supplement Time</th>
                <th>Duration (Minutes)</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {
                historicalDataKeys.map(key =>
                  <SupplementRowHistory key={key} object={historicalData[key]}/>
                )
              }
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}
class SupplementsLogView extends Component {
  render() {
    return (
      <div>
        <div className="card">
        <div className="card-header">
          <strong>Add Supplement Entry</strong>
        </div>
        <div className="card-block">
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label>Supplement</label>
                <input type="text" className="form-control" id="name" placeholder="Select Supplement"/>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="form-group col-sm-4">
              <label>Serving Size</label>
              <select className="form-control" id="ccmonth">
                <option>1</option>
              </select>
            </div>

            <div className="form-group col-sm-4">
              <label>Time</label>
              <select className="form-control" id="ccyear">
                <option>2014</option>
              </select>
            </div>

            <div className="col-sm-4">
              <div className="form-group">
                <label>Duration (Minutes)</label>
                <input type="text" className="form-control" id="cvv" placeholder="123"/>
              </div>
            </div>

          </div>
        </div>

        </div>
        <SupplementsTableList/>
      </div>
    )
  }
}

export default SupplementsLogView;
