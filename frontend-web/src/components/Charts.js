import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Charts({ data }) {
  const { equipment_type_distribution, recent_uploads } = data;

  const styles = getComputedStyle(document.documentElement);
  const chartText = (styles.getPropertyValue('--chart-text') || '#64748b').trim();
  const chartGrid = (styles.getPropertyValue('--chart-grid') || 'rgba(148,163,184,0.2)').trim();

  // Data for equipment type distribution
  const typeChartData = {
    labels: Object.keys(equipment_type_distribution).map(t => t.toUpperCase()),
    datasets: [
      {
        label: 'Count',
        data: Object.values(equipment_type_distribution),
        backgroundColor: [
          '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140',
        ],
        borderColor: [
          '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: { font: { size: 12 }, color: chartText },
      },
    },
    scales: {
      x: { ticks: { color: chartText }, grid: { color: chartGrid } },
      y: { ticks: { color: chartText }, grid: { color: chartGrid } },
    },
  };

  // Line chart for recent upload trends
  const uploads = Array.isArray(recent_uploads) ? [...recent_uploads].reverse() : [];
  const lineChartData = {
    labels: uploads.map(u => new Date(u.uploaded_at).toLocaleString()),
    datasets: [
      {
        label: 'Avg Flowrate',
        data: uploads.map(u => Number(u.avg_flowrate ?? 0)),
        borderColor: '#4facfe',
        backgroundColor: 'rgba(79, 172, 254, 0.2)',
        tension: 0.3,
        pointRadius: 3,
        yAxisID: 'yLeft',
      },
      {
        label: 'Avg Pressure',
        data: uploads.map(u => Number(u.avg_pressure ?? 0)),
        borderColor: '#43e97b',
        backgroundColor: 'rgba(67, 233, 123, 0.2)',
        tension: 0.3,
        pointRadius: 3,
        yAxisID: 'yRight',
      },
      {
        label: 'Avg Temperature',
        data: uploads.map(u => Number(u.avg_temperature ?? 0)),
        borderColor: '#fa709a',
        backgroundColor: 'rgba(250, 112, 154, 0.2)',
        tension: 0.3,
        pointRadius: 3,
        yAxisID: 'yLeft',
      }
    ],
  };
  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { color: chartText } },
      title: { display: false },
    },
    scales: {
      x: { ticks: { color: chartText }, grid: { color: chartGrid } },
      yLeft: { type: 'linear', position: 'left', beginAtZero: true, ticks: { color: chartText }, grid: { color: chartGrid } },
      yRight: { type: 'linear', position: 'right', beginAtZero: true, ticks: { color: chartText }, grid: { drawOnChartArea: false, color: chartGrid } },
    },
  };

  return (
    <div className="charts-container">
      <h2>Equipment Analytics</h2>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Recent Uploads Trend (Line)</h3>
          <div style={{ height: '280px' }}>
            <Line data={lineChartData} options={lineOptions} />
          </div>
          {uploads.length < 2 && (
            <p style={{ marginTop: 10, color: 'var(--muted)' }}>
              Add another upload to see a clearer trend line.
            </p>
          )}
        </div>

        <div className="chart-card">
          <h3>Equipment Distribution (Pie)</h3>
          <Pie data={typeChartData} options={chartOptions} />
        </div>

        <div className="chart-card">
          <h3>Equipment Distribution (Bar)</h3>
          <Bar data={typeChartData} options={chartOptions} />
        </div>

        <div className="chart-card">
          <h3>Equipment Distribution (Doughnut)</h3>
          <Doughnut data={typeChartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}

export default Charts;
