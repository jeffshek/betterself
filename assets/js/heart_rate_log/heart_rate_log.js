import React, {Component} from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from 'react-chartjs-2';
import SupplementsLogView from '../supplements_log/supplements_log'

const heartRateHistory = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  datasets: [
    {
      label: 'Average Heart Rate (Monthly)',
      fill: false,
      lineTension: 0.4,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'rgba(25,52,65,1)',
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: 'rgba(1,1,1,1)',
      pointBackgroundColor: '#fff',
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: 'rgba(1,1,1,1)',
      pointHoverBorderColor: 'rgba(220,220,220,1)',
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [65, 59, 80, 81, 56, 55, 63, 65, 66, 82, 72, 52]
    }
  ]
}

class HeartRateLogView extends Component {
  render() {
    return (
      <div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Line data={heartRateHistory}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
        <SupplementsLogView/>
      </div>
    )
  }
}

export default HeartRateLogView;
