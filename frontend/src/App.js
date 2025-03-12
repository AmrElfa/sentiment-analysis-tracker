import React, { useState } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import 'chart.js/auto';
import './App.css';

function getScoreColor(score) {
  if (score < 4) return 'red';
  if (score < 7) return 'yellow';
  return 'green';
}

function getBarColors() {
  // Positive: Green, Neutral: Yellow, Negative: Red
  return ['#28a745', '#ffc107', '#dc3545'];
}

function App() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [recentSearches, setRecentSearches] = useState([]);

  const handleAnalyze = async () => {
    if (!company) return;
    setIsLoading(true);
    try {
      const analyzeRes = await fetch(`http://localhost:8000/analyze?company=${company}`);
      if (!analyzeRes.ok) {
        throw new Error(`Server error: ${analyzeRes.statusText}`);
      }
      const analyzeData = await analyzeRes.json();
      setData(analyzeData);

      const histRes = await fetch(`http://localhost:8000/history?company=${company}`);
      if (!histRes.ok) {
        throw new Error(`Server error: ${histRes.statusText}`);
      }
      const histData = await histRes.json();
      setHistory(histData.history);

      setRecentSearches(prev => {
        if (prev.includes(company)) return prev;
        return [...prev, company];
      });
    } catch (err) {
      console.error("Fetch error:", err);
      alert("An error occurred while fetching data. Check the console for details.");
    } finally {
      setIsLoading(false);
    }
  };

  const barData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
      label: 'Sentiment Breakdown',
      data: data ? [data.positive, data.neutral, data.negative] : [0, 0, 0],
      backgroundColor: getBarColors()
    }]
  };

  // limit the number of ticks on x-axis for historical trend
  const historyOptions = {
    scales: {
      x: {
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10
        }
      }
    }
  };

  const historyData = {
    labels: history.map(h => {
      const d = new Date(h.timestamp);
      return d.toLocaleString(); // shows date and time with minutes
    }),
    datasets: [{
      label: 'Historical Overall Score',
      data: history.map(h => h.score),
      borderColor: '#007bff',
      fill: false,
      tension: 0.1
    }]
  };

  const handleSelectSearch = (e) => {
    setCompany(e.target.value);
  };

  const scoreColor = data ? getScoreColor(data.overall) : 'black';

  return (
    <div className="main-container">
      <header className="header">
        <div className="left-menu">
          <select onChange={handleSelectSearch} defaultValue="">
            <option value="" disabled>Recent Searches</option>
            {recentSearches.map((item, idx) => (
              <option key={idx} value={item}>{item}</option>
            ))}
          </select>
        </div>
        <h1>Sentiment Analysis</h1>
      </header>

      <div className="top-section">
        <input
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="Enter a company or product"
          className="company-input"
        />
        <button onClick={handleAnalyze} className="analyze-button">Analyze</button>
      </div>

      {isLoading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Fetching data, please wait...</p>
        </div>
      )}

      {!isLoading && data && (
        <div className="content">
          <h2 className="company-name">{company}</h2>
          <div className="score-box">
            Score: <span 
              className="score-value" 
              style={{
                color: scoreColor,
                textShadow: scoreColor === 'yellow' ? '1px 1px 2px black' : 'none'
              }}
            >
              {data.overall}
            </span>
          </div>

          <div className="chart-row">
            <div className="chart-box">
              <h3>Sentiment Breakdown</h3>
              <Bar data={barData} />
            </div>
            {history && history.length > 0 && (
              <div className="chart-box">
                <h3>Historical Trend</h3>
                <Line data={historyData} options={historyOptions} />
              </div>
            )}
          </div>

          <div className="summary-section">
            <h3>Summary of Reviews</h3>
            <p className="summary-text">
              {data.summary && data.summary !== "" ? data.summary : "No summary available."}
            </p>
          </div>

          <div className="reviews-section">
            <h3>Raw Reviews</h3>
            {data.reviews && data.reviews.length > 0 ? (
              <ul>
                {data.reviews.map((review, idx) => (
                  <li key={idx} className="review-item">
                    {review}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No reviews found.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
